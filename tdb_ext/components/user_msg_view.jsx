/*
 * system messages/errors appear here
*/

define([
	'react',
	'jquery',
	'dispatcher',
], function(React,$,dispatcher){

	var UserMsgView = React.createClass({
		getInitialState: function() {
			return {msg:"Waiting for TDB to connect..."}
		},
		render: function() {
			return (
					<div>
						<p>{this.state.msg}</p>
					</div>
				)
		},
		componentDidMount: function() {
			var self=this
			dispatcher.register(function(action){
				if (action.actionType == 'user_msg')
					self.setState({msg:action.data})
			})
		}
	})

	return UserMsgView
});

 