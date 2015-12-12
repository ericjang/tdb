/*
This is the entry point into HyperTree nbextension
after installing into ~/.jupyter/nbextensions/, do
javascript:require(["nbextensions/tdb_ext"] function(ht){});
*/

var ROOT = '/nbextensions/tdb_ext'
var BOWER = ROOT+'/bower_components'
var STORES = '/nbextensions/tdb_ext/stores'

// easy access to vendor libs

require.config({
  paths: {
    "dispatcher": ROOT + "/dispatcher",
    "flux":BOWER+"/flux/dist/Flux.min",
    "eventemitter2":BOWER + '/eventemitter2/lib/eventemitter2',
    "keyMirror":ROOT+'/keymirror',
    "raphael":BOWER + "/raphael/raphael-min",
    "dispatcher": ROOT + "/dispatcher",
    "react": BOWER + "/react/react-with-addons",
    "JSXTransformer": BOWER + "/react/JSXTransformer",
    "jsx": BOWER + "/requirejs-react-jsx/jsx",
    "text": BOWER + "/requirejs-text/text",
    "plotstore":STORES + "/plotstore"
  },
  shim : {
    "react": {
      "exports": "React"
    },
    "JSXTransformer": "JSXTransformer"
  },
  config: {
    jsx: {
      fileExtension: ".jsx",
      transformOptions: {
        harmony: true,
        stripTypes: false,
        inlineSourceMap: true
      },
      usePragma: false
    }
  }
});

define([
  'base/js/namespace',
   ROOT + '/htapp.js'
], function(Jupyter,HTApp){
	var kernel = Jupyter.notebook.kernel
	var comm_manager=Jupyter.notebook.kernel.comm_manager
	// icky - binding as a global variable
  HT=new HTApp(comm_manager)
  HT.ui.load_ui()
  HT.ui.show_ui()
  console.log('HT nbextension loaded')
})
