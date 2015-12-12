// plottable watch variable in HyperTree


var COMPONENTS='/nbextensions/tdb_ext/components/'


define([
	'react',
	'jquery',
	'dispatcher',
	'jsx!' + COMPONENTS + 'plotview.jsx'
], function(React,$,dispatcher,PlotView){

	var PlotListView = React.createClass({
		render: function() {
			var plots=[]

			var allPlots = this.props.plots
			for (var key in allPlots) {
				plots.push(<PlotView key={key} name={key} src={allPlots[key]}/>)
			}

			return (
				<div>
					{plots}
				</div>
			)
		}
	})

	return PlotListView
});
