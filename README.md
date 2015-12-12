# TDB

TensorDebugger (TDB) is a visual debugger for TensorFlow. 

It is the combination of a Python library and a Jupyter notebook extension, built around Google's TensorFlow framework. Together, these extend TensorFlow with run-time visualization capabilities.

<!-- GIF Screenshot here! -->

## FAQ

### Is TDB affiliated with TensorFlow?

No, but it is built on top of it.

### What is TDB good for?

TDB is especially useful at the model prototyping stage and verifying correctness in an intuitive manner. It is also useful for high-level visualization of hidden layers during training.

### How is TDB different from TensorBoard?

TensorBoard is a suite of visualization tools included with Tensorflow. Both TDB and TensorBoard attach auxiliary nodes to the TensorFlow graph in order to inspect data.

TensorBoard cannot be used concurrently with running a TensorFlow graph; log files must be written first. TDB interfaces directly with the execution of a TensorFlow graph, and allows for stepping through execution one node at a time.

Out of the box, TensorBoard currently only supports logging for a few predefined data formats. 

TDB is to TensorBoard as GDB is to printf. Both are useful in different contexts.



License: Apache 2.0



Current problem:
- Optimizer node not running.
