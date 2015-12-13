"""
HT debugging on a simple LeNET-5 convolutional model
"""

import numpy as np
import sys
import tensorflow as tf
import unittest
import tdb
from tdb.examples import mnist, viz


class TestMNIST(unittest.TestCase):
  def test_1(self):
    # single passthrough
    (train_data_node,
    train_labels_node,
    validation_data_node,
    test_data_node,
    # predictions
    train_prediction,
    validation_prediction,
    test_prediction,
    # weights
    conv1_weights,
    conv2_weights,
    fc1_weights,
    fc2_weights,
    # training
    optimizer,
    loss,
    learning_rate,
    summaries) = mnist.build_model()

    with tf.Session() as s:
      tf.initialize_all_variables().run()
      print('Variables initialized')
      step=0
      with np.load("mnist_0.npz") as data:
        feed_dict = {
          train_data_node: data['batch_data'],
          train_labels_node: data['batch_labels']
        }
      evals=[train_prediction]
      status,result=tdb.debug(evals, feed_dict=feed_dict, breakpoints=None, break_immediately=False, session=s)
      self.assertEqual(status,tdb.FINISHED)
  
  def test_2(self):
    """
    mnist with plotting
    """
    (train_data_node,
    train_labels_node,
    validation_data_node,
    test_data_node,
    # predictions
    train_prediction,
    validation_prediction,
    test_prediction,
    # weights
    conv1_weights,
    conv2_weights,
    fc1_weights,
    fc2_weights,
    # training
    optimizer,
    loss,
    learning_rate,
    summaries) = mnist.build_model()
    
    s=tf.InteractiveSession()
    tf.initialize_all_variables().run()

    # use the same input every time for this test
    with np.load("mnist_0.npz") as data:
        a=data['batch_data']
        b=data['batch_labels']
        feed_dict = {
            train_data_node: a,
            train_labels_node: b
        }
    
    # pdb.set_trace()
    # result=s.run(optimizer,feed_dict)
    # pdb.set_trace()
    # tmp
    # return

    evals=[optimizer,loss,train_prediction,conv1_weights,conv2_weights,fc1_weights,fc2_weights]

    # define some plotting functions
    
    # use one debugSession per run
    
    # attach plot nodes
    g=tf.get_default_graph()
    p1=tdb.plot_op(viz.viz_conv_weights,inputs=[g.as_graph_element(conv1_weights)])
    p2=tdb.plot_op(viz.viz_conv_weights,inputs=[g.as_graph_element(conv2_weights)])
    p3=tdb.plot_op(viz.viz_fc_weights,inputs=[g.as_graph_element(fc1_weights)])
    p4=tdb.plot_op(viz.viz_fc_weights,inputs=[g.as_graph_element(fc2_weights)])

    # get the plot op by name and 
    evals=[optimizer, loss, learning_rate, train_prediction, p1,p2,p3,p4]
    status,result=tdb.debug(evals, feed_dict=feed_dict, session=s)
