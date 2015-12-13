
def _tchelper(tc_deps,evals,deps):
	"""
	modifies graph in place
	"""
	for e in evals:
		if e in tc_deps: # we've already included it
			continue
		else:
			if e in deps: # has additional dependnecies
				tc_deps[e]=deps[e]
				# add to tc_deps the dependencies of the dependencies
				_tchelper(tc_deps,deps[e],deps)
	return tc_deps

def transitive_closure(evals,deps):
	"""
	evals = node names we want values for (i.e. we don't care about any other nodes after
		we've evaluated all the eval nodes)
	deps = full dependency graph of all nodes
	"""
	return _tchelper({},evals,deps)
