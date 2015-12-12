// communicates with the corresponding htapp on the python side


define([
	'base/js/namespace',
	'jsx!/nbextensions/tdb_ext/components/ui',
	'base/js/events',
	'dispatcher'
], function(Jupyter,UI,events,dispatcher){
	
	var HTApp=function(comm_manager){
		//
		// MEMBER VARIABLES
		//

		this.ui = new UI()
		this._comm = null
		this.is_connected = true

		//
		// CONSTRUCTOR INITIALIZATION
		//
		var self=this
		comm_manager.register_target('tdb', function(comm,msg){
			dispatcher.dispatch({
				actionType:'user_msg',
				data:'TDB connected: success'
			})

			self._comm=comm
			this.is_connected=true
			comm.on_msg(function(msg){
				var data=msg['content']['data']
								
				var msg_type=data['msg_type']
				if (msg_type == 'action') {
					// if we receive an action, send it to dispatcher
					var action={
			      		actionType: data['action'],
			      		data: data['params']
			    	}
					dispatcher.dispatch(action)
				} else {
					console.log('Unrecognized msg_type ' + msg_type)
					console.log(data)
				}
			})
		})

		events.on('kernel_restarting.Kernel', function() { 
			dispatcher.dispatch({
				actionType: 'clear'
			})
		});
		
	}


	return HTApp
})


