# Examples <!-- omit in toc -->

This folder contains examples demonstrating the usage and functionality of mPickle, showcasing how to serialize and deserialize data between Python and MicroPython environments while addressing module mapping and compatibility challenges.

- [Basic Data Types](#basic-data-types)
- [Custom classes](#custom-classes)
- [NumPy NDArray](#numpy-ndarray)
  - [Prerequisites](#prerequisites)

## Basic Data Types
This example demonstrates the process of serializing and deserializing various Python data types using the `mpickle` library. The objective is to ensure compatibility across different Python environments, such as MicroPython and standard Python, while showcasing how diverse data structures—including basic data types, collections, and nested structures—can be efficiently serialized to a byte stream and reconstructed.

## Custom classes
This example demonstrates the process of serializing and deserializing a custom Python class using the `mpickle` library. The objective is to show how `mpickle` can be used to efficiently convert complex Python objects into a byte stream that can be saved, transferred, and reconstructed later. By using `mpickle`, developers gain more flexibility and compatibility for working in environments like MicroPython, which requires efficient memory handling. This approach ensures that the serialized data maintains the structure and behavior of the original class, making it easy to restore the object state when needed.

## NumPy NDArray
This example demonstrates how to serialize and deserialize complex Python objects, like NumPY arrays, using both the `mpickle` library for MicroPython and the standard `pickle` library for CPython. The goal of this demonstration is to illustrate how to preserve the data structure, type information, and values of complex objects when transferring data across different environments, such as from CPython to MicroPython.

### Prerequisites
To run this example it is necessary to properly build MicroPython including both `mpickle` and `ulab` libraries. To include `mpickle`, you can follow [this guide](README.md#setup). However, for `ulab` it is necessary to be included at compilation time of MicroPython with a few specific flags.

1. **Move to the Compilation Tool Directory**

   Change your working directory to the location of `mpy-helper`:
   ```sh
   cd <repo_path>/firmware/dev-scripts/generic
   ```

2. **Add `ulab` to Modules for Firmware**

   Copy the `ulab` code into the `modules/user_c_modules/include/` directory:
   ```sh
   git clone https://github.com/v923z/micropython-ulab.git
   cp -r micropython-ulab/code ./modules/user_mp_modules/include/ulab
   ```

3. **Compile the Firmware**

   Use the `mpy-helper` tool to compile the firmware, specifying your target. For example, to compile for UNIX:

   ```sh
   ./mpy-helper build UNIX ULAB_MAX_DIMS=4 ULAB_HAS_DTYPE_OBJECT=1 MICROPY_FLOAT_IMPL=1
   ```

   The `UNIX` target is just an example; replace it with your desired target board (e.g., `ESP32_GENERIC_S3`, `ESP32_GENERIC`, `RPI_PICO_W`, `ARDUINO_NICLA_VISION`, `STM32L496GDISC`, etc.).

   These flags are important:
   - **`ULAB_MAX_DIMS=4`**: Ensures that `ulab` can handle up to 4-dimensional arrays.
   - **`ULAB_HAS_DTYPE_OBJECT=1`**: Enables support for various data types within `ulab`.  
   - **`MICROPY_FLOAT_IMPL=1`**: Force `float32` support on UNIX, otherwsie it uses system float support (*e.g.,* `flaot64`). This flag can be removed for non-UNIX boards.

   After compiling, you'll have a MicroPython interpreter or firmware image that includes `ulab`.

## How to run <!-- omit in toc -->

Along with this file, there is a number of folders representing the python types and classes that will be pickled/unpickled in the respective example; in each folder, a file named `example.py` can be found. While in the desired folder, running
   ```sh
        $PYTHON -i example.py
   ```