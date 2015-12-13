"""
builds a simple mnist model
"""

import gzip
import numpy as np
import re
import sys
import tensorflow as tf

FLAGS = tf.app.flags.FLAGS

tf.app.flags.DEFINE_string('train_dir', '/tmp/cifar10_train',
                           """Directory where to write event logs """
                           """and checkpoint.""")

IMAGE_SIZE = 28
NUM_CHANNELS = 1
PIXEL_DEPTH = 255
NUM_LABELS = 10
VALIDATION_SIZE = 5000  # Size of the validation set.
SEED = 66478  # Set to None for random seed.
BATCH_SIZE = 64
NUM_EPOCHS = 1

TEST_SIZE=55000
TRAIN_SIZE=10000

# DATA PRE-PROCESSING
def extract_data(filename, num_images):
  """
  Extract the images into a 4D tensor [image index, y, x, channels].
  Values are rescaled from [0, 255] down to [-0.5, 0.5].
  """
  print('Extracting', filename)
  with gzip.open(filename) as bytestream:
    bytestream.read(16)
    buf = bytestream.read(IMAGE_SIZE * IMAGE_SIZE * num_images)
    data = np.frombuffer(buf, dtype=np.uint8).astype(np.float32)
    data = (data - (PIXEL_DEPTH / 2.0)) / PIXEL_DEPTH
    data = data.reshape(num_images, IMAGE_SIZE, IMAGE_SIZE, 1)
    return data

def extract_labels(filename, num_images):
  """
  Extract the labels into a 1-hot matrix [image index, label index].
  """
  print('Extracting', filename)
  with gzip.open(filename) as bytestream:
    bytestream.read(8)
    buf = bytestream.read(1 * num_images)
    labels = np.frombuffer(buf, dtype=np.uint8)
    # Convert to dense 1-hot representation.
    return (np.arange(NUM_LABELS) == labels[:, None]).astype(np.float32)

def get_data(data_root):
  train_data_filename = data_root+'train-images-idx3-ubyte.gz'
  train_labels_filename = data_root+'train-labels-idx1-ubyte.gz'
  test_data_filename = data_root+'t10k-images-idx3-ubyte.gz'
  test_labels_filename = data_root+'t10k-labels-idx1-ubyte.gz'

  # Extract it into numpy arrays.
  train_data = extract_data(train_data_filename, 60000)
  train_labels = extract_labels(train_labels_filename, 60000)
  test_data = extract_data(test_data_filename, 10000)
  test_labels = extract_labels(test_labels_filename, 10000)

  validation_data = train_data[:VALIDATION_SIZE, :, :, :]
  validation_labels = train_labels[:VALIDATION_SIZE]
  train_data = train_data[VALIDATION_SIZE:, :, :, :]
  train_labels = train_labels[VALIDATION_SIZE:]

  global TRAIN_SIZE, TEST_SIZE
  TRAIN_SIZE=train_labels.shape[0]
  TEST_SIZE=test_labels.shape[0]

  return train_data, train_labels, validation_data, validation_labels, test_data, test_labels

def _activation_summary(x):
  """Helper to create summaries for activations.
  Creates a summary that provides a histogram of activations.
  Creates a summary that measure the sparsity of activations.
  Args:
    x: Tensor
  Returns:
    nothing
  """
  # Remove 'tower_[0-9]/' from the name in case this is a multi-GPU training
  # session. This helps the clarity of presentation on tensorboard.
  tf.histogram_summary(x.name + '/activations', x)
  tf.scalar_summary(x.name + '/sparsity', tf.nn.zero_fraction(x))

# MODEL BUILDING
def build_model():
  """
  Builds the computation graph consisting of training/testing LeNet

  train data - used for learning
  validation data - used for printing progress (does not impact learning)
  test data - used for printing final test error
  """
  # training data
  train_data_node = tf.placeholder(tf.float32,shape=(BATCH_SIZE, IMAGE_SIZE, IMAGE_SIZE, NUM_CHANNELS))
  train_labels_node = tf.placeholder(tf.float32,shape=(BATCH_SIZE, NUM_LABELS))

  validation_data_node= tf.placeholder(tf.float32,shape=(VALIDATION_SIZE, IMAGE_SIZE, IMAGE_SIZE, NUM_CHANNELS))
  test_data_node=tf.placeholder(tf.float32,shape=(TEST_SIZE,IMAGE_SIZE,IMAGE_SIZE,NUM_CHANNELS))
  # validation dataset held in a single constant node
  # validation_data_node = tf.constant(validation_data)
  # test_data_node = tf.constant(test_data)

  # LEARNABLE WEIGHT NODES SHARED BETWEEN
  conv1_weights = tf.Variable(tf.truncated_normal([5, 5, NUM_CHANNELS, 32],stddev=0.1,seed=SEED))
  conv1_biases = tf.Variable(tf.zeros([32]))
  conv2_weights = tf.Variable(tf.truncated_normal([5, 5, 32, 64],stddev=0.1,seed=SEED))
  conv2_biases = tf.Variable(tf.constant(0.1, shape=[64]))
  fc1_weights = tf.Variable(tf.truncated_normal([IMAGE_SIZE // 4 * IMAGE_SIZE // 4 * 64, 512],stddev=0.1,seed=SEED))
  fc1_biases = tf.Variable(tf.constant(0.1, shape=[512]))
  fc2_weights = tf.Variable(tf.truncated_normal([512, NUM_LABELS],stddev=0.1,seed=SEED))
  fc2_biases = tf.Variable(tf.constant(0.1, shape=[NUM_LABELS]))

  # LENET
  def build_lenet(data,train=False):
    # subroutine for wiring up nodes and weights to training and evaluation LeNets
    conv1 = tf.nn.conv2d(data,conv1_weights,strides=[1, 1, 1, 1],padding='SAME')
    relu1 = tf.nn.relu(tf.nn.bias_add(conv1, conv1_biases))
    pool1 = tf.nn.max_pool(relu1,ksize=[1, 2, 2, 1],strides=[1, 2, 2, 1],padding='SAME')
    conv2 = tf.nn.conv2d(pool1,conv2_weights,strides=[1, 1, 1, 1],padding='SAME')
    relu2 = tf.nn.relu(tf.nn.bias_add(conv2, conv2_biases))
    pool2 = tf.nn.max_pool(relu2,ksize=[1, 2, 2, 1],strides=[1, 2, 2, 1],padding='SAME')
    # Reshape the feature map cuboid into a 2D matrix to feed it to the
    # fully connected layers.
    pool_shape = pool2.get_shape().as_list()
    reshape = tf.reshape(pool2,[pool_shape[0], pool_shape[1] * pool_shape[2] * pool_shape[3]])
    fc1 = tf.nn.relu(tf.matmul(reshape, fc1_weights) + fc1_biases)
    # Add a 50% dropout during training only. Dropout also scales
    # activations such that no rescaling is needed at evaluation time.
    if train:
      fc1 = tf.nn.dropout(fc1, 0.5, seed=SEED)
      # append summary ops to train
      _activation_summary(conv1)
      _activation_summary(fc1)

    fc2 = tf.matmul(fc1, fc2_weights) + fc2_biases
    return fc2

  # TRAINING LOSS / REGULARIZATION NODES
  logits = build_lenet(train_data_node, True)
  loss = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits, train_labels_node))

  tf.scalar_summary(loss.op.name,loss)

  regularizers = (tf.nn.l2_loss(fc1_weights) + tf.nn.l2_loss(fc1_biases) + tf.nn.l2_loss(fc2_weights) + tf.nn.l2_loss(fc2_biases))
  # Add the regularization term to the loss.
  loss += 5e-4 * regularizers

  # OPTIMIZER NODES
  batch = tf.Variable(0)
  # Decay once per epoch, using an exponential schedule starting at 0.01.
  learning_rate = tf.train.exponential_decay(
    0.01,                # Base learning rate.
    batch * BATCH_SIZE,  # Current index into the dataset.
    TRAIN_SIZE,          # Decay step.
    0.95,                # Decay rate.
    staircase=True)
  # Use simple momentum for the optimization.
  optimizer = tf.train.MomentumOptimizer(learning_rate,0.9).minimize(loss,global_step=batch)

  # # Predictions for the minibatch, validation set and test set.
  train_prediction = tf.nn.softmax(logits)
  # # We'll compute them only once in a while by calling their {eval()} method.
  validation_prediction = tf.nn.softmax(build_lenet(validation_data_node))
  test_prediction = tf.nn.softmax(build_lenet(test_data_node))

  summaries=tf.merge_all_summaries()

  # return input nodes and output nodes
  return (train_data_node,
    train_labels_node,
    validation_data_node,
    test_data_node,
    train_prediction,
    validation_prediction,
    test_prediction,
    conv1_weights,
    conv2_weights,
    fc1_weights,
    fc2_weights,
    optimizer,
    loss,
    learning_rate,
    summaries)

def error_rate(predictions, labels):
  """Return the error rate based on dense predictions and 1-hot labels."""
  return 100.0 - (
      100.0 *
      np.sum(np.argmax(predictions, 1) == np.argmax(labels, 1)) /
      predictions.shape[0])

def main():
  # get dataset as numpy arrays
  train_data, train_labels, validation_data, validation_labels, test_data, test_labels = get_data()
  #pdb.set_trace()

  # build net (return inputs)
  (train_data_node,
  train_labels_node,
  validation_data_node,
  test_data_node,
  optimizer,
  loss,
  learning_rate,
  train_prediction,
  validation_prediction,
  test_prediction,
  summaries) = build_model()

  with tf.Session() as s:
    # Run all the initializers to prepare the trainable parameters.
    tf.initialize_all_variables().run()
    print('Initialized!')
    # Loop through training steps.
    summary_writer=tf.train.SummaryWriter(FLAGS.train_dir, graph_def=s.graph_def)
    for step in xrange(NUM_EPOCHS * TRAIN_SIZE // BATCH_SIZE):
      # Compute the offset of the current minibatch in the data.
      offset = (step * BATCH_SIZE) % (TRAIN_SIZE - BATCH_SIZE)
      batch_data = train_data[offset:(offset + BATCH_SIZE), :, :, :]
      batch_labels = train_labels[offset:(offset + BATCH_SIZE)]
      feed_dict = {
        train_data_node: batch_data,
        train_labels_node: batch_labels
      }
      # Run the graph and fetch some of the nodes.
      _, l, lr, predictions = s.run([optimizer, loss, learning_rate, train_prediction],feed_dict=feed_dict)

      if step % 100 == 0:
          # re-run graph, save summaries
          summary_str = summaries.eval(feed_dict)
          summary_writer.add_summary(summary_str, step)

      if step % 100 == 0:
        print('Epoch %.2f' % (float(step) * BATCH_SIZE / TRAIN_SIZE))
        print('Minibatch loss: %.3f, learning rate: %.6f' % (l, lr))
        print('Minibatch error: %.1f%%' % error_rate(predictions, batch_labels))
        val_predict=validation_prediction.eval(feed_dict={validation_data_node:validation_data})
        print('Validation error: %.1f%%' %error_rate(val_predict, validation_labels))
        sys.stdout.flush()
    # Done training - print the result!
    test_error = error_rate(test_prediction.eval(feed_dict={test_data_node:test_data}), test_labels)
    print('Test error: %.1f%%' % test_error)

if __name__ == "__main__":
    main()
