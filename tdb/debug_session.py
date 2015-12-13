
from ht_op import HTOp
import op_store
import tensorflow as tf

# debug status codes
INITIALIZED = 'INITIALIZED'
RUNNING = 'RUNNING'
PAUSED = 'PAUSED'
FINISHED = 'FINISHED'

class DebugSession(object):
	
	def __init__(self, session=None):
		super(DebugSession, self).__init__()
		
		if session is None:
			session=tf.InteractiveSession()
		_original_evals=None
		self.step=0 # index into execution order
		self.session=session
		self.state=INITIALIZED
		self._original_evals=[] # evals passed into self.debug, in order
		self._evalset=set() # string names to evaluate
		self._bpset=set() # breakpoint names
		self._cache={} # key: node names in evalset -> np.ndarray
		self._exe_order=[] # list of HTOps, tf.Tensors to be evaluated
	
	### 
	### PUBLIC METHODS
	### 

	def run(self, evals, feed_dict=None, breakpoints=None, break_immediately=False):
		"""
		starts the debug session
		"""
		if not isinstance(evals,list):
			evals=[evals]
		if feed_dict is None:
			feed_dict={}
		if breakpoints is None:
			breakpoints=[]

		self.state=RUNNING
		self._original_evals=evals
		self._original_feed_dict=feed_dict
		self._exe_order=op_store.compute_exe_order(evals)
		self._init_evals_bps(evals, breakpoints)

		# convert cache keys to strings
		for k,v in feed_dict.items():
			if not isinstance(k,str):
				k=k.name
			self._cache[k]=v

		op_store.register_dbsession(self)

		if break_immediately:
			return self._break()
		else:
			return self.c()

	def s(self):
		"""
		step to the next node in the execution order
		"""
		next_node=self._exe_order[self.step]
		self._eval(next_node)
		self.step+=1
		if self.step==len(self._exe_order):
			return self._finish()
		else:
			# if stepping, return the value of the node we just
			# evaled
			return self._break(value=self._cache.get(next_node.name))

	def c(self):
		"""
		continue
		"""
		i,node=self._get_next_eval()
		if node.name in self._bpset:
			if self.state == RUNNING:
				return self._break()
		
		self.state = RUNNING
		self._eval(node)
		# increment to next node
		self.step=i+1
		if self.step < len(self._exe_order):
			return self.c()
		else:
			return self._finish()

	def get_values(self):
		"""
		returns final values (same result as tf.Session.run())
		"""
		return [self._cache.get(i.name,None) for i in self._original_evals]
	
	def get_exe_queue(self):
		return self._exe_order[self.step:]

	def get_value(self, node):
		"""
		retrieve a node value from the cache
		"""
		if isinstance(node,tf.Tensor):
			return self._cache.get(node.name,None)
		elif isinstance(node,tf.Operation):
			return None
		else: # handle ascii, unicode strings
			return self._cache.get(node,None)

	### 
	### PRIVATE METHODS 
	### 

	def _cache_value(self, tensor, ndarray):
		"""
		store tensor ndarray value in cache. this is called by python ops
		"""
		self._cache[tensor.name]=ndarray

	def _init_evals_bps(self, evals, breakpoints):
		# If an eval or bp is the tf.Placeholder output of a tdb.PythonOp, replace it with its respective PythonOp node
		evals2=[op_store.get_op(t) if op_store.is_htop_out(t) else t for t in evals]
		breakpoints2=[op_store.get_op(t) if op_store.is_htop_out(t) else t for t in breakpoints]
		# compute execution order
		self._exe_order=op_store.compute_exe_order(evals2) # list of nodes
		# compute evaluation set
		"""
		HTOps may depend on tf.Tensors that are not in eval. We need to have all inputs to HTOps ready
		upon evaluation. 

		1. all evals that were originally specified are added
		2. each HTOp in the execution closure needs to be in eval (they won't be eval'ed automatically by Session.run)
		3. if an input to an HTOp is a tf.Tensor (not a HT placeholder tensor), it needs to be in eval as well (it's not
			tensorflow so we'll have to manually evaluate it). Remember, we don't track Placeholders because we instead 
			run the HTOps that generate their values.
		"""
		self._evalset=set([e.name for e in evals2])
		for e in self._exe_order:
			if isinstance(e,HTOp):
				self._evalset.add(e.name)
				for t in e.inputs:
					if not op_store.is_htop_out(t):
						self._evalset.add(t.name)

		# compute breakpoint set
		self._bpset=set([bp.name for bp in breakpoints2])

	def _get_next_eval(self):
		n=len(self._exe_order)
		o=self._exe_order
		return next((i,o[i]) for i in range(self.step,n) if (o[i].name in self._evalset or o[i].name in self._bpset))

	def _eval(self, node):
		"""
		node is a TensorFlow Op or Tensor from self._exe_order
		"""
		# if node.name == 'Momentum':
		# 	pdb.set_trace()
		if isinstance(node,HTOp):
			# All Tensors MUST be in the cache.
			feed_dict=dict((t,self._cache[t.name]) for t in node.inputs)
			node.run(feed_dict) # this will populate self._cache on its own
		else: # is a TensorFlow node
			if isinstance(node,tf.Tensor):
				result=self.session.run(node,self._cache)
				self._cache[node.name]=result
			else:
				# is an operation
				if node.type =='Assign' or node.type == 'AssignAdd' or node.type == 'AssignSub':
					# special operation that takes in a tensor ref and mutates it
					# unfortunately, we end up having to execute nearly the full graph?
					# alternatively, find a way to pass the tensor_ref thru the feed_dict
					# rather than the tensor values.
					self.session.run(node,self._original_feed_dict)
					
	def _break(self,value=None):
		self.state=PAUSED
		i,next_node=self._get_next_eval()
		print('Breakpoint triggered. Next Node: ', next_node.name)
		return (self.state,value)

	def _finish(self):
		self.state=FINISHED
		return (self.state, self.get_values())

