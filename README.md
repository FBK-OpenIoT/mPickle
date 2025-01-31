# mPickle - Pickle for MicroPython <!-- omit in toc -->
The **mPickle (microPickle)** library offers a pure-Python implementation of Pickle, compatible with Protocol 5 (except for PickleBuffer), specifically design and adapted for MicroPython. It is adapted by the original CPython library, which can be found [here](https://github.com/python/cpython/blob/main/Lib/pickle.py).

## Table of contents <!-- omit in toc -->
- [Description](#description)
- [Usage](#usage)
  - [Importing the Module](#importing-the-module)
  - [Serializing (Dumping) Data](#serializing-dumping-data)
  - [Deserializing (Loading) Data](#deserializing-loading-data)
  - [**Extending `mpickle` with Non-Standard Objects**](#extending-mpickle-with-non-standard-objects)
  - [**Injecting Fake Modules and Functions with `inject_fake_module_func`**](#injecting-fake-modules-and-functions-with-inject_fake_module_func)
- [Setup](#setup)
  - [Deploy the code using `mpr` (`mpremote`)](#deploy-the-code-using-mpr-mpremote)
    - [Prerequisites](#prerequisites)
    - [Step-by-Step instructions](#step-by-step-instructions)
  - [Build a firmware with frozen module](#build-a-firmware-with-frozen-module)
- [Examples](#examples)
- [License](#license)
- [Reference](#reference)

## Description
mPickle is a pure-Python library for MicroPython that addresses the challenge of serializing and deserializing data on microcontrollers running MicroPython firmware. By enabling the transfer of Python objects in Pickle’s native binary format, it streamlines communication between MicroPython and standard Python environments. mPickle bridges the gap between IoT devices, edge computing, and the data science world, enabling efficient data transfer and analysis. This capability fosters collaboration among engineers, scientists, and data analysts, enabling seamless work on real-time data insights, model deployment, and data-driven solutions across diverse computing environments—all within a unified data language.

## Usage  

The `mpickle` module in MicroPython works similarly to the `pickle` module in CPython, providing the same API for serializing and deserializing Python objects.

### Importing the Module  
To use `mpickle`, simply import it:  
```python
import mpickle
```

### Serializing (Dumping) Data  
Serialization converts a Python object into a binary format for storage or transmission.

---

#### **Method:** <!-- omit in toc -->
```python
serialized_data = mpickle.dump(data)
```
#### **Parameters:** <!-- omit in toc -->
- `data` (*object*) – The Python object to be serialized. This can include built-in types such as integers, floats, strings, lists, tuples, dictionaries, and certain user-defined objects.

#### **Returns:** <!-- omit in toc -->
- `serialized_data` (*bytes*) – A binary representation of the input object, which can be stored or transmitted.

#### **Example:** <!-- omit in toc -->
```python
data = {"name": "Alice", "age": 25, "scores": [90, 85, 88]}
serialized_data = mpickle.dump(data)
print(serialized_data)  # Output: Binary data
```

### Deserializing (Loading) Data  
Deserialization reconstructs a Python object from its binary representation.

---

#### **Method:** <!-- omit in toc -->
```python
deserialized_data = mpickle.load(serialized_data)
```
#### **Parameters:** <!-- omit in toc -->
- `serialized_data` (*bytes*) – A binary representation of a previously serialized Python object.

#### **Returns:** <!-- omit in toc -->
- `deserialized_data` (*object*) – The original Python object before serialization.

#### **Example:** <!-- omit in toc -->
```python
deserialized_data = mpickle.load(serialized_data)
print(deserialized_data)  # Output: {'name': 'Alice', 'age': 25, 'scores': [90, 85, 88]}
```

### **Extending `mpickle` with Non-Standard Objects**  

MicroPython imposes limitations on module and object management, affecting the behavior of pickling libraries. Some objects require explicit serialization and reconstruction definitions. The `register_pickle` function in `mpickle` enables custom mappings to handle such cases.

---

#### **Method:**   <!-- omit in toc -->
```python
mpickle.register_pickle(
    obj_type,
    obj_full_name,
    obj_module,
    obj_reconstructor_func=None,
    reduce_func=None,
    reconstruct_func=None,
    setstate_func=None,
    map_obj_module=None,
    map_obj_full_name=None,
    map_reconstructor_func=None
)
```

#### **Parameters:**   <!-- omit in toc -->
- **`obj_type`** (*type*) – The class or user-defined type that requires custom serialization.  
- **`obj_full_name`** (*str*) – The fully qualified name of the object in MicroPython (e.g., `"ulab.dtype"`).  
- **`obj_module`** (*str*) – The name of the module where the object is originally defined.  
- **`obj_reconstructor_func`** (*str*, optional) – A *dotted path* specifying the function that reconstructs the object.  
- **`reduce_func`** (*callable*, optional) – A function emulating the `__reduce__` method to define how the object is serialized.  
- **`reconstruct_func`** (*callable*, optional) – A function that reconstructs the object from serialized data.  
- **`setstate_func`** (*callable*, optional) – A function emulating `__setstate__`, used to restore object state after reconstruction.  
- **`map_obj_module`** (*str*, optional) – The equivalent module in standard Python (e.g., `"numpy"` for `"ulab"` objects).  
- **`map_obj_full_name`** (*str*, optional) – The fully qualified name of the equivalent Python object (e.g., `"numpy.dtype"`).  
- **`map_reconstructor_func`** (*str*, optional) – The *dotted path* of the function that reconstructs the mapped Python object.  

#### **Returns:**   <!-- omit in toc -->
- `None` – This function registers the serialization and deserialization behavior for the specified object type.

#### **Example:**   <!-- omit in toc -->
Registering `ulab.dtype` as a serializable object, in MicroPython, and mapping it to `numpy.dtype`, in CPython:  

```python
import mpickle
import ulab

reduce_dtype_matrix = {
    str(ulab.dtype('int8')): (ulab.dtype, ('i1', False, True), (3, '|', None, None, None, -1, -1, 0)),
    str(ulab.dtype('int16')): (ulab.dtype, ('i2', False, True), (3, '<', None, None, None, -1, -1, 0))
}

# A dictionary for reconstructing specific data types from reduced representations during deserialization.
# It maps strings representing data types to actual ulab dtype objects.
reconstruct_dtype_matrix = {
    "i1": ulab.dtype('int8'),
    "i2": ulab.dtype('int16')
}

# A dictionary to convert between ulab data types and their NumPy equivalents.
# This helps convert ulab dtypes into standard NumPy dtypes.
dtype_convert_matrix = {
    str(ulab.dtype('int8')): ulab.numpy.int8,
    str(ulab.dtype('int16')): ulab.numpy.int16
}

# Function to reduce a dtype object into a suitable form for serialization.
def reduce_dtype(x):
    return reduce_dtype_matrix[str(x)]

def reconstructor_dtype(*args):
    dtype_str = args[0]
    # print(f"reconstructor_dtype - Type={dtype_str}")
    if dtype_str in reconstruct_dtype_matrix:
        return reconstruct_dtype_matrix[dtype_str]
    else:
        raise ValueError(f"Dtype {dtype_str} is not available")

mpickle.register_pickle(
    obj_type=ulab.dtype,
    obj_full_name="ulab.dtype",
    obj_module="ulab",
    obj_reconstructor_func=None,  # Explicitly using `reconstruct_func`
    reduce_func=reduce_dtype,
    reconstruct_func=reconstructor_dtype,
    setstate_func=None,
    map_obj_module="numpy",
    map_obj_full_name="numpy.dtype",
    map_reconstructor_func="numpy.dtype"
)
```

The complete example on NumPy is available in `examples/numpy-ndarray`.

### **Injecting Fake Modules and Functions with `inject_fake_module_func`**  

MicroPython does not always include all standard Python modules, which can cause issues during deserialization when a module or function is missing. To handle this, `mpickle` provides the `inject_fake_module_func` function.  

This function dynamically creates placeholder modules and functions within the MicroPython environment, replicating the expected module hierarchy. It ensures that `mpickle` can correctly reference these placeholders during deserialization, allowing seamless object reconstruction.  

---

#### **Method:**   <!-- omit in toc -->
```python
fake_func = mpickle.inject_fake_module_func(module_path, func_name)
```

#### **Parameters:**   <!-- omit in toc -->
- **`module_path`** (*str*) – The full dotted path of the module to be injected (e.g., `"numpy.core.multiarray"`).  
- **`func_name`** (*str*) – The name of the function to be injected into the module (e.g., `"_reconstruct"`).  

#### **Returns:**   <!-- omit in toc -->
- `fake_func` (*callable*) – A placeholder function reference corresponding to the injected module and function. This placeholder can be used in serialization to maintain expected deserialization behavior.  


#### **Example:**   <!-- omit in toc -->

Injecting a fake `_reconstruct` function into the `numpy.core.multiarray` module and using it to reduce a NumPy `ndarray` for serialization:  

```python
from mpickle.mpickle import inject_fake_module_func, register_pickle

def reduce_ndarray(x):
    # Injecting a fake function from a non-existent module to ensure compatibility during deserialization
    func = inject_fake_module_func("numpy.core.multiarray", "_reconstruct")
    
    # Returning reconstruction information:
    # - The function reference (`func`) that will be used for deserialization
    # - A tuple containing type, shape, data type, and byte representation
    return (
        func, 
        (type(x), (0,), b'b'),  # Initial reconstruction parameters
        (1, x.shape, x.dtype, False, bytes(x.tobytes()))  # Data needed to reconstruct the ndarray
    )
```
The complete example on NumPy is available in `examples/numpy-ndarray`.

## Setup
To get started with mPickle, you have two options:
1. **Deploy the code directly to your board using `mpremote`.**
2. **Freeze/embed the mPickle code into the firmware installation.**

### Deploy the code using `mpr` (`mpremote`)
An alternative way to deploy mPickle is to use `mpr`, which allows you to upload the mPickle code directly to your board without modifying the firmware.

#### Prerequisites
1. **Install Python**: Make sure Python> 3.9 is installed on your system.
2. **Install mpremote**: Install `mpr` and `mpremote` using `pip`:
   ```sh
   pip install mpr mpremote
   ```
3. **Connect Your Board**: Connect the microcontroller board to your computer via USB.
4. **Identify Board Port**: Determine the serial port used by your board (e.g., `/dev/ttyUSB0` for Linux/macOS or `COM3` for Windows).

#### Step-by-Step instructions
1. **Navigate to the Project Directory**
   Move to the directory that contains the `src` folder:
   ```sh
   cd path/to/mPickle
   ```

2. **Upload Files Using `ampy`**
   Use the following command to upload the `src/mPickle/mpickle` folder to the board. This will create a directory named mpickle on the board:
   ```sh
   mpr -d <PORT> put -r src/mPickle/mpickle /
   ```

   - Replace `<PORT>` with the appropriate port for your board (e.g., `/dev/ttyUSB0` or `COM3`).
   - `src/mPickle/mpickle` is the path to the code folder.
   - `/` is the name of the destination on the board (the root). It will create the mpickle directory.

3. Install dependencies
   `mPickle` depends on `types` and `functools`, thus install them with the command:
   ```sh
   mpr -d <PORT> mip install types functools
   ```

4. **Confirm Upload**
   Once uploaded, you can list the files on your board using:
   ```sh
   mpr -d <PORT> ls
   ```
   You should see the `mpickle` folder in the output.

5. **Verify the deployment**
   If the deployment succeeds, mPickle will be available as module. You can confirm this by connecting to the MicroPython REPL with the command
   ```sh
   mpr -d <PORT> repl
   ```
   and running:
   ```python
   import mpickle
   ```
   or running
   ```sh
   mpr exec 'import mpickle; print(mpickle.__version__)'
   ```
   and it should print the version of the `mPickle` library.

### Build a firmware with frozen module
This repository includes a set of compilation scripts located in `firmware/dev-scripts`, to build a custom MicroPython firmware with mPickle as a frozen module, along with (`ulab`)[https://github.com/v923z/micropython-ulab]. 
These scripts support firmware compilation for ESP32 (and its variants) as well as UNIX.
For detailed compilation steps, refer to (this guide)[/firmware/dev-scripts/README.md].

Once the MicroPython has been compile, and eventually flashed, it is possible to check if everything is working by connecting to the MicroPython REPL and running:
```python
import mpickle
```
Or, if you have installed `mpr`, you can run
```sh
mpr exec 'import mpickle; print(mpickle.__version__)'
```
and it should print the version of the `mPickle` library.

## Examples
The mPickle project comes with a few examples available [here](/src/examples).

## License
You can read the license [HERE](/LICENSE).

## Reference
This library has been described in 
```
Put the citation
```