// plottable watch variable in HyperTree

define([
	'react',
	'jquery',
	'dispatcher',
], function(React,$,dispatcher){


	var PlotView = React.createClass({
		propTypes : {
			name: React.PropTypes.string,
			src: React.PropTypes.string
		},	
		render: function() {
			// need an x close button
			var css ={
				border:"1px solid",
				borderRadius:"5px",
				margin:"10px",
				position: "relative"
			}
			var imgcss = {
				maxWidth: "100%",
				padding:"8px"
			}
			var h3css={
				textAlign: "center"
			}
			var closecss={
				position: "absolute",
		    top: "20px",
		    right: "20px"
			}
			return (
				<div style={css}>
					<h3 style={h3css}>{this.props.name}</h3>
					<button style={closecss} className="btn btn-default" title="Close"  onClick={this._onDestroyClick}>
						<i className="fa-close fa" />
					</button>
					<img style={imgcss} src={this.props.src} />
				</div>
			)
		},
		_onDestroyClick: function() {
			dispatcher.dispatch({
				actionType:'remove_plot',
				name:this.props.name
			})
		}
	})

	return PlotView
});
