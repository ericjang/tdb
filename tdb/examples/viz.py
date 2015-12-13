# a collection of sample visualization functions
# for binding to plotnode

import matplotlib.pyplot as plt
import numpy as np

def viz_square(data, normalize=True, cmap=plt.cm.gray, padsize=1, padval=0):
    """
    takes a np.ndarray of shape (n, height, width) or (n, height, width, channels)
    visualize each (height, width) thing in a grid of size approx. sqrt(n) by sqrt(n)
    However, this only draws first input channel
    """
    # normalize to 0-1 range
    if normalize:
        data -= data.min()
        data /= data.max()
    n = int(np.ceil(np.sqrt(data.shape[0]))) # force square 
    padding = ((0, n ** 2 - data.shape[0]), (0, padsize), (0, padsize)) + ((0, 0),) * (data.ndim - 3)
    data = np.pad(data, padding, mode='constant', constant_values=(padval, padval))
    # tile the filters into an image
    data = data.reshape((n, n) + data.shape[1:]).transpose((0, 2, 1, 3) + tuple(range(4, data.ndim + 1)))
    data = data.reshape((n * data.shape[1], n * data.shape[3]) + data.shape[4:])
    plt.matshow(data,cmap=cmap)

def viz_conv_weights(ctx, weight):
  # visualize all output filters 
  # for the first input channel
  viz_square(weight.transpose(3,0,1,2)[:,:,:,0])

def viz_activations(ctx, m):
  plt.matshow(m.T,cmap=plt.cm.gray)
  plt.title("LeNet Predictions")
  plt.xlabel("Batch")
  plt.ylabel("Digit Activation")

def viz_weight_hist(ctx, w):
  plt.hist(w.flatten())

def viz_conv_hist(ctx, w):
  n = int(np.ceil(np.sqrt(w.shape[3]))) # force square 
  f, axes = plt.subplots(n,n,sharex=True,sharey=True)
  for i in range(w.shape[3]): # for each output channel
    r,c=i//n,i%n
    axes[r,c].hist(w[:,:,:,i].flatten())
    axes[r,c].get_xaxis().set_visible(False)
    axes[r,c].get_yaxis().set_visible(False)

def viz_fc_weights(ctx, w):
  # visualize fully connected weights
  plt.matshow(w.T,cmap=plt.cm.gray)

def watch_loss(ctx,loss):
  if not hasattr(ctx, 'loss_history'):
    ctx.loss_history=[]
  ctx.loss_history.append(loss)
  plt.plot(ctx.loss_history)
  plt.ylabel('loss')
