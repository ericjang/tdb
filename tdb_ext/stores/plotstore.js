
define([
  'dispatcher',
  'eventemitter2'
], function(dispatcher,EventEmitter){

  var CHANGE_EVENT = 'change'

  // key = PlotOp node name
  // value = img src
  var _plots = {}


  var PlotStore = Object.assign({}, EventEmitter.prototype, {
    getPlots: function() {
      return _plots
    },
    update: function(data) {
      _plots[data.name]=data.src
    },
    clear: function() {
      _plots={}
    },
    remove: function(name) {
      if (_plots.hasOwnProperty(name)) {
        delete _plots[name]
      }
    },
    emitChange: function() {
      this.emit(CHANGE_EVENT);
    },
    addChangeListener: function(callback) {
      this.on(CHANGE_EVENT, callback)
    },
    removeChangeListener: function(callback) {
      this.removeListener(CHANGE_EVENT, callback)
    }
  })

  // register store with the dispatcher
  dispatcher.register(function(action){
    switch(action.actionType){
      case 'update_plot':
        // create new plot or update an old one
        PlotStore.update(action.data)
        PlotStore.emitChange()
        break;
      case 'remove_plot':
        PlotStore.remove(action.name)
        PlotStore.emitChange()
        break;
      case 'clear':
        PlotStore.clear()
        PlotStore.emitChange()
        break;
      default:
        // no op
    }
  })

  return PlotStore
})
