# mPickle Examples <!-- omit in toc -->

This folder contains examples demonstrating the usage and functionality of mPickle, showcasing how to serialize and deserialize data between Python and MicroPython environments while addressing module mapping and compatibility challenges.

- [Examples](#examples)
  - [Basic Data Types](#basic-data-types)
  - [Custom classes](#custom-classes)
  - [NumPy NDArray](#numpy-ndarray)
- [Prerequisites](#prerequisites)
- [Running an Example](#running-an-example)
- [Running Tests](#running-tests)

## Examples

### Basic Data Types
This example demonstrates the process of serializing and deserializing various Python data types using the `mpickle` library. The objective is to ensure compatibility across different Python environments, such as MicroPython and standard Python, while showcasing how diverse data structures—including basic data types, collections, and nested structures—can be efficiently serialized to a byte stream and reconstructed.

### Custom classes
This example demonstrates the process of serializing and deserializing a custom Python class using the `mpickle` library. The objective is to show how `mpickle` can be used to efficiently convert complex Python objects into a byte stream that can be saved, transferred, and reconstructed later. By using `mpickle`, developers gain more flexibility and compatibility for working in environments like MicroPython, which requires efficient memory handling. This approach ensures that the serialized data maintains the structure and behavior of the original class, making it easy to restore the object state when needed.

### NumPy NDArray
This example demonstrates how to serialize and deserialize complex Python objects, like NumPY arrays, using both the `mpickle` library for MicroPython and the standard `pickle` library for CPython. The goal of this demonstration is to illustrate how to preserve the data structure, type information, and values of complex objects when transferring data across different environments, such as from CPython to MicroPython.

## Prerequisites
To run this example, you must first properly build MicroPython, including the `mpickle` library. If you plan to run the NumPy NDArray example, you will also need to include the `ulab` library. To add `mpickle` to your build, follow [this guide](README.md#setup).

## Running an Example
To execute an example, navigate to the corresponding example folder and run:
```sh
$MPYTHON -i example.py
```
Here, `$MPYTHON` represents the command used to run MicroPython, assuming it has been compiled for UNIX.
These examples can also be executed on microcontrollers by uploading the code to the device.

## Running Tests
The provided examples also serve as tests for the `mpickle` library to ensure its compatibility with the native CPython `pickle` module. To verify this, you first need to compile MicroPython for UNIX and then execute:
```sh
./test.sh
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
Test Dump: CPython (pickle) -> Load: MicroPython (mpickle): ✅ 15 successful | ❌ 0 failed | 📦 Total: 15
Test Dump: MicroPython (mpickle) -> Load: CPython (pickle): ✅ 15 successful | ❌ 0 failed | 📦 Total: 15
Test Dump: MicroPython (mpickle) -> Load: MicroPython (mpickle): ✅ 15 successful | ❌ 0 failed | 📦 Total: 15
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
