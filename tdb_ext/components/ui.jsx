// class that manages the top-level React component
// handles UI-related methods

var COMPONENTS='/nbextensions/tdb_ext/components/'

define([
	'react',
	'jquery',
	'dispatcher',
	'plotstore',
	'jsx!' + COMPONENTS + 'plotlistview',
	'jsx!' + COMPONENTS + 'user_msg_view'
], function(React,$,dispatcher,PlotStore, PlotListView, UserMsgView){

	var UI=function(){
		this.had_loaded=false
		// starting notebook width
		this._nbw = .65 // width of notebook (percentage) when HT pane is open
		
		this.UIView = React.createClass({
			getInitialState: function() {
				return this._getState()
			},
			render: function() {
				var css={
					'backgroundColor':'#FFFFFF',
				}
				return (
					<div style={css}>
						<UserMsgView />
						<PlotListView plots={this.state.plots} />
					</div>
				)
			},
			componentDidMount: function() {
				// listen to PlotStore 
				PlotStore.addChangeListener(this._onChange)
			},
			_onChange: function() {
				this.setState(this._getState())
			},
			_getState: function() {
				return {
					"plots":PlotStore.getPlots()
				}
			}
		})

	}

	UI.prototype.load_ui = function() {
		// initializes the UI

		$('#site').after('<div id=\"ht_separator\"/>')

		var w=$('#site').width()
		var h=$('#site').height()
		
		$('#ht_separator').css({
			height: "100%",
			width: "1%",
			float: "left",
			backgroundColor: "grey"
		})

		$('#ht_separator').after('<div id=\"ht_main\" />')
		
		
		$('#ht_main').width((1-this._nbw-.02)*w)

		$('#ht_main').css({
			float:'left',
			height:'100%',
			overflow:'scroll'
		})

		var self=this
		$('#ht_separator').draggable({
	    axis: 'x', 
	    containment: 'parent',
	    helper: 'clone', 
	    start: function(event, ui) {
	    	self.ow=$(window).width()
	    },
	    drag: function (event, ui) {
	    	//console.log(ui)
	    	var width=ui.offset.left
	    	$(this).prev().width(width)
	    	//console.log(self.ow)
	    	$(this).next().width(self.ow-width-0.01*self.ow)
	    } 
		});

		React.render(<this.UIView />,document.getElementById("ht_main"))
		this.has_loaded=true
	}

	UI.prototype.show_ui = function(){
		// load the split view
	  	// slide notebook to left and inject ui
	  	
	  	// something weird going on - has show_ui and hide_ui in prototype
	  	// but missing load_ui and test()
	  	// for now, manually access the global object
			
	  $('#site').width(this._nbw*100+'%')
		$('#notebook-container').width(this._nbw*100+'%')
		$('#site').css('float','left');
		
	  $('#ht_main').show()
	}

	UI.prototype.hide_ui = function() {
		// hide the split view
		$('#ht_main').hide()
		$('#site').width('')
		$('#notebook-container').width('')
	}

	return UI
})



