# mPickle Examples <!-- omit in toc -->

This folder contains examples demonstrating the usage and functionality of mPickle, showcasing how to serialize and deserialize data between Python and MicroPython environments while addressing module mapping and compatibility challenges.

- [License](#license)
- [Examples](#examples)
  - [Hello World](#hello-world)
  - [Basic Data Types](#basic-data-types)
  - [Custom classes](#custom-classes)
  - [NumPy NDArray](#numpy-ndarray)
  - [NumPy LeNet-5 Neural Network](#numpy-lenet-5-neural-network)
    - [Model Training](#model-training)
  - [IoT Datastream](#iot-datastream)
- [Prerequisites](#prerequisites)
- [Running an Example](#running-an-example)
- [Running Exmaples as Tests](#running-exmaples-as-tests)

## License
You can read the license [HERE](/LICENSE).

## Examples

![mPickle examples workflow](/docs/imgs/examples_workflow.jpg)

Each example follows the workflow shown in the figure above to validate interoperability between **mPickle** running on **MicroPython** and native **Pickle** running on **CPython**.

Starting from a data object in MicroPython (*Input data*), the object is serialized using `mpickle.dump` and then stored or transmitted. On the CPython side, the data are deserialized (*Output data*) using `pickle.load`. The same serialized data can also be loaded back into MicroPython (e.g., when storing a configuration data structure) using `mpickle.load`.

The examples also support the reverse direction: a CPython object that can be serialized with `pickle.dump` can be transferred to MicroPython and reconstructed using `mpickle.load`.

### Hello World
This basic example ([Link](/src/examples/hello-world/)) demonstrates the process of serializing and deserializing simple data structures, such as a string and an integer. It converts a string and an integer into their corresponding binary representations and then converts them back to their original object forms.

### Basic Data Types
This example ([Link](/src/examples/builtins-data-types/)) demonstrates the process of serializing and deserializing various Python data types using the `mpickle` library. The objective is to ensure compatibility across different Python environments, such as MicroPython and standard Python, while showcasing how diverse data structures—including basic data types, collections, and nested structures—can be efficiently serialized to a byte stream and reconstructed.

### Custom classes
This example ([Link](/src/examples/custom-class/)) demonstrates the process of serializing and deserializing a custom Python class using the `mpickle` library. The objective is to show how `mpickle` can be used to efficiently convert complex Python objects into a byte stream that can be saved, transferred, and reconstructed later. By using `mpickle`, developers gain more flexibility and compatibility for working in environments like MicroPython, which requires efficient memory handling. This approach ensures that the serialized data maintains the structure and behavior of the original class, making it easy to restore the object state when needed.

### NumPy NDArray
This example ([Link](/src/examples/numpy-ndarray/)) demonstrates how to serialize and deserialize complex Python objects, like NumPY arrays, using both the `mpickle` library for MicroPython and the standard `pickle` library for CPython. The goal of this demonstration is to illustrate how to preserve the data structure, type information, and values of complex objects when transferring data across different environments, such as from CPython to MicroPython.

### NumPy LeNet-5 Neural Network
This example ([Link](/src/examples/numpy-lenet5/)) demonstrates a complete neural network implementation using `mpickle` for model serialization. The example features a LeNet-5 convolutional neural network that can be trained on both MicroPython and CPython environments, with the trained model weights serializible using `mpickle` for cross-platform compatibility. For better performance, the model should be trained in a CPython environment and then moved to the MicroPython environment. If model is not trained, the example loads pretrained model weights obtained running the training script in CPython.

The example includes:
- **LeNet-5 Model**: Full implementation with forward pass, training, and evaluation capabilities
- **Cross-Platform Training**: Optimized training routines for both MicroPython (memory-efficient, low detection performance) and CPython (full-featured, higher detection performance) environments
- **Model Serialization**: Save and load trained model weights using mPickle
- **Complete Workflow**: Data generation, training, evaluation, and model persistence

This example showcases how `mpickle` can handle complex data structures (dictionary of Numpy NDArrays) like machine learning models, making it possible to train models in resource-rich environments and deploy them to resource-constrained MicroPython devices while maintaining full compatibility.

#### Model Training
The script provided for training (`lenet5_train_model.py`) should be run by a CPython interpreter since it requires a lot of memory to run. However, it may run also inside a MicroPython environment by properly setting the `heapsize` so it can allocate the necessary memory. To do so, the command is
```sh
$MPYTHON -X heapsize=8/16M lenet5_train_model.py
```

### IoT Datastream
This example ([Link](/src/examples/iot-datastream/)) demonstrates how to use `mpickle` for data transmission in IoT applications.

The example includes:
- **MicroPython Client (`client_micropython.py`)**: it simulates an IoT device (runs on MicroPython) that collects sensor data (temperature, humidity, battery) and sends it to a server using both `mpickle` and JSON formats.
- **CPython Client (`client_cpython.py`)**: it simulates an IoT device (runs on CPython) that collects sensor data (temperature, humidity, battery) and sends it to a server using both native `pickle` and JSON formats.
- **CPython Flask Server (`server_cpython.py`)**: it acts a data sink by receiving and processing sensor data, providing endpoints for both `pickle` and JSON formats, and offers statistics.

This example is particularly useful for developers and practitioners working on IoT applications where data interoperability usually plays a critical role.

## Prerequisites
To run these examples, you must first properly build MicroPython, including the `mpickle` library. If you plan to run the NumPy NDArray example or the NumPY LeNet5 example, you will also need to include the `ulab` library. To add `mpickle` to your build, follow [this guide](/README.md#setup).

## Running an Example
To execute an example, navigate to the corresponding example folder and run:
```sh
$MPYTHON -i example.py
```
Here, `$MPYTHON` represents the command used to run MicroPython, assuming it has been compiled for UNIX.
These examples can also be executed on microcontrollers by uploading the code to the device.

## Running Exmaples as Tests
The `builtins-data-types`, `custom-class`, and `numpy-ndarray` examples also serve as tests for the `mpickle` library to ensure its compatibility with the native CPython `pickle` module. To verify this, you first need to compile MicroPython for UNIX and then execute:
```sh
./run_test.sh
```
This script runs three different tests on each example:
1. **Cross-compatibility with CPython:**  
   - Data is dumped using `mpickle` in MicroPython and then loaded using `pickle` in CPython.
2. **Reverse cross-compatibility:**  
   - Data is dumped using `pickle` in CPython and then loaded using `mpickle` in MicroPython.
3. **MicroPython internal consistency:**  
   - Data is both dumped and loaded using `mpickle` within MicroPython.
A successful test run produces an output similar to the following:
```
Testing builtins-data-types
Test Dump: CPython (pickle) -> Load: MicroPython (mpickle): ✅ 16 successful | ❌ 0 failed | 📦 Total: 16
Test Dump: MicroPython (mpickle) -> Load: CPython (pickle): ✅ 16 successful | ❌ 0 failed | 📦 Total: 16
Test Dump: MicroPython (mpickle) -> Load: MicroPython (mpickle): ✅ 16 successful | ❌ 0 failed | 📦 Total: 16
Test passed for builtins-data-types

Testing custom-class
Test Dump: CPython (pickle) -> Load: MicroPython (mpickle): ✅ 4 successful | ❌ 0 failed | 📦 Total: 4
Test Dump: MicroPython (mpickle) -> Load: CPython (pickle): ✅ 4 successful | ❌ 0 failed | 📦 Total: 4
Test Dump: MicroPython (mpickle) -> Load: MicroPython (mpickle): ✅ 4 successful | ❌ 0 failed | 📦 Total: 4
Test passed for custom-class

Testing numpy-ndarray
Test Dump: CPython (pickle) -> Load: MicroPython (mpickle): ✅ 8 successful | ❌ 0 failed | 📦 Total: 8
Test Dump: MicroPython (mpickle) -> Load: CPython (pickle): ✅ 8 successful | ❌ 0 failed | 📦 Total: 8
Test Dump: MicroPython (mpickle) -> Load: MicroPython (mpickle): ✅ 8 successful | ❌ 0 failed | 📦 Total: 8
Test passed for numpy-ndarray
```
