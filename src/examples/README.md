# Examples <!-- omit in toc -->

This folder contains examples demonstrating the usage and functionality of mPickle, showcasing how to serialize and deserialize data between Python and MicroPython environments while addressing module mapping and compatibility challenges.

- [Basic Data Types](#basic-data-types)
- [Custom classes](#custom-classes)
- [NumPy NDArray](#numpy-ndarray)

## Basic Data Types
This example demonstrates the process of serializing and deserializing various Python data types using the mpickle library. The objective is to ensure compatibility across different Python environments, such as MicroPython and standard Python, while showcasing how diverse data structures—including basic data types, collections, and nested structures—can be efficiently serialized to a byte stream and reconstructed.

## Custom classes

## NumPy NDArray

## How to run <!-- omit in toc -->

Along with this file, there is a number of folders representing the python types and classes that will be pickled/unpickled in the respective example; in each folder, a file named `example.py` can be found. While in the desired folder, running

        $PYTHON -i example.py

will start the python REPL and import the file for you. All you need to do is call the `example()` funciton

in some cases, such as for the [built-in datatypes](builtins-data-types), you can provide a list as an argument to the function, and it will try to pickle the objects in your list rather than the predefined one