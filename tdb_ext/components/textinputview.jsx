// plottable watch variable in HyperTree

define([
	'react',
	'jquery',
	'dispatcher',
], function(React,$,dispatcher){


	var TextInputView = React.createClass({
		propTypes : {
			name: React.PropTypes.string,
			src: React.PropTypes.string
		},	
		render: function() {
			// need an x close button
			var css ={
				border:"1px solid",
				borderRadius:"5px",
				margin:"10px"
			}
			var imgcss = {
				maxWidth: "100%",
				margin:"5px"
			}
			return (
				<div style={css}>
					<h3>{this.props.name}</h3>
					<img style={imgcss} src={this.props.src} />
				</div>
			)
		}
	})

	return TextInputView
});
