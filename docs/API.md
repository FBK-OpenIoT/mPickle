# mPickle API Documentation <!-- omit in toc -->

This document provides a comprehensive overview of the public APIs exposed by the mPickle library, which is a MicroPython-compatible implementation of Python's pickle module. mPickle enables serialization and deserialization of Python objects with special adaptations for MicroPython environments.

## Table of Contents <!-- omit in toc -->

- [Introduction](#introduction)
- [Version Information](#version-information)
- [Functions](#functions)
  - [dump()](#dump)
  - [dumps()](#dumps)
  - [load()](#load)
  - [loads()](#loads)
  - [register\_pickle()](#register_pickle)
  - [inject\_dummy\_module\_func()](#inject_dummy_module_func)
  - [revert\_dummy\_module\_func()](#revert_dummy_module_func)
- [Classes](#classes)
  - [Pickler](#pickler)
  - [Unpickler](#unpickler)
- [Exceptions](#exceptions)
  - [PickleError](#pickleerror)
  - [PicklingError](#picklingerror)
  - [UnpicklingError](#unpicklingerror)

## Introduction

mPickle is a modified version of Python's standard `pickle` module designed to work seamlessly with MicroPython while maintaining compatibility with standard Python (CPython). It provides the same core functionality for object serialization and deserialization but includes special adaptations for:

- Limited module availability in MicroPython
- Memory constraints in embedded environments
- Cross-environment data exchange between CPython and MicroPython

## Version Information

- **`__version__`**: A string containing the current version of the mPickle library (e.g., "0.2.0").

## Functions

### dump()

Pickles an object to a file.

**Signature:**
```python
dump(obj, file, protocol=None, fix_imports=True)
```

**Parameters:**
- `obj`: The object to be pickled.
- `file`: A file-like object with a `write()` method where the pickled data will be written.
- `protocol`: The protocol version to use for pickling. If `None`, the highest protocol version will be used.
- `fix_imports`: If `True`, pickle will try to map the new Python 3 names to the old module names used in Python 2.

**Example:**
```python
import mpickle

data = {'name': 'Alice', 'age': 30, 'hobbies': ['reading', 'hiking']}
with open('user_data.pkl', 'wb') as f:
    mpickle.dump(data, f)
```

### dumps()

Pickles an object to a bytes object.

**Signature:**
```python
dumps(obj, protocol=None, fix_imports=True)
```

**Parameters:**
- `obj`: The object to be pickled.
- `protocol`: The protocol version to use for pickling. If `None`, the highest protocol version will be used.
- `fix_imports`: If `True`, pickle will try to map the new Python 3 names to the old module names used in Python 2.

**Returns:**
- A bytes object containing the pickled representation of the object.

**Example:**
```python
import mpickle

# Serialize to bytes for network transmission or storage
data = {'sensor_id': 'temp_001', 'readings': [23.5, 24.1, 23.8]}
pickled_data = mpickle.dumps(data)
print(f"Pickled data size: {len(pickled_data)} bytes")
```

### load()

Unpickles an object from a file.

**Signature:**
```python
load(file, fix_imports=True, encoding="ASCII", errors="strict")
```

**Parameters:**
- `file`: A file-like object with a `readline()` and `read()` method from which the pickled data will be read.
- `fix_imports`: If `True`, pickle will try to map the old Python 2 names to the new module names used in Python 3.
- `encoding`: Tells pickle how to decode any instances of `str` objects from the pickle data stream.
- `errors`: Tells pickle how to deal with errors when decoding `str` objects.

**Returns:**
- The unpickled object.

**Example:**
```python
import mpickle

# Load data from file
with open('user_data.pkl', 'rb') as f:
    loaded_data = mpickle.load(f)
    print(f"Loaded user: {loaded_data['name']}")
```

### loads()

Unpickles an object from a bytes object.

**Signature:**
```python
loads(data, fix_imports=True, encoding="ASCII", errors="strict")
```

**Parameters:**
- `data`: A bytes object containing the pickled representation of the object.
- `fix_imports`: If `True`, pickle will try to map the old Python 2 names to the new module names used in Python 3.
- `encoding`: Tells pickle how to decode any instances of `str` objects from the pickle data stream.
- `errors`: Tells pickle how to deal with errors when decoding `str` objects.

**Returns:**
- The unpickled object.

**Example:**
```python
import mpickle

# Deserialize from bytes received over network
pickled_data = b'...'  # Received from network
loaded_data = mpickle.loads(pickled_data)
print(f"Received data: {loaded_data}")
```

### register_pickle()

Registers custom serialization and deserialization functions for a specific object type.

**Signature:**
```python
register_pickle(obj_type=None, obj_full_name=None, obj_module=None,
                obj_reconstructor_func=None, reduce_func=None,
                reconstruct_func=None, setstate_func=None,
                map_obj_module=None, map_obj_full_name=None,
                map_reconstructor_func=None)
```

**Parameters:**
- `obj_type`: The type of the object to be registered.
- `obj_full_name`: The fully qualified name of the object (e.g., 'module.submodule.ClassName').
- `obj_module`: The module name where the object is defined.
- `obj_reconstructor_func`: The fully qualified name of the reconstruction function.
- `reduce_func`: A function that takes an object and returns a tuple representing how the object should be serialized.
- `reconstruct_func`: A function that takes the serialized data and reconstructs the original object.
- `setstate_func`: A function that takes the reconstructed object and its state, and sets the object's state.
- `map_obj_module`: The module name to map to during deserialization.
- `map_obj_full_name`: The fully qualified name to map to during deserialization.
- `map_reconstructor_func`: The fully qualified name of the reconstruction function to map to during deserialization.

**Example:**
```python
import mpickle

class SensorReading:
    def __init__(self, sensor_id, timestamp, value):
        self.sensor_id = sensor_id
        self.timestamp = timestamp
        self.value = value

def reduce_sensor(obj):
    # Return a tuple: (constructor, arguments)
    return (SensorReading, (obj.sensor_id, obj.timestamp, obj.value))

def reconstruct_sensor(sensor_id, timestamp, value):
    # Reconstruct the object
    return SensorReading(sensor_id, timestamp, value)

# Register the custom pickling functions
mpickle.register_pickle(
    obj_type=SensorReading,
    obj_full_name='__main__.SensorReading',
    obj_module='__main__',
    reduce_func=reduce_sensor,
    reconstruct_func=reconstruct_sensor
)

# Now SensorReading instances can be pickled and unpickled
reading = SensorReading('temp_001', '2023-01-01T12:00:00', 23.5)
pickled = mpickle.dumps(reading)
unpickled = mpickle.loads(pickled)
```

**Advanced Example with Module Mapping:**
```python
# This example shows how to handle cross-environment compatibility
# where module names differ between serialization and deserialization

mpickle.register_pickle(
    obj_type=MyClass,
    obj_full_name='__main__.MyClass',
    obj_module='__main__',
    map_obj_module='mymodule',
    map_obj_full_name='mymodule.MyClass',
    reduce_func=reduce_myclass,
    reconstruct_func=reconstruct_myclass
)
```

### inject_dummy_module_func()

Injects a dummy module function to handle module-level functions during pickling.

**Signature:**
```python
inject_dummy_module_func(module_name, func_name, func)
```

**Parameters:**
- `module_name`: The name of the module where the dummy function will be injected.
- `func_name`: The name of the dummy function.
- `func`: The actual function to be called when the dummy function is invoked.

**Example:**
```python
import mpickle

# Define a custom reconstruction function
def custom_reconstructor(*args, **kwargs):
    print(f"Reconstructing with args: {args}, kwargs: {kwargs}")
    return args[0]  # Simple example

# Inject the dummy module function
mpickle.inject_dummy_module_func(
    module_name='custom_module',
    func_name='reconstruct_object',
    func=custom_reconstructor
)
```

### revert_dummy_module_func()

Reverts a previously injected dummy module function.

**Signature:**
```python
revert_dummy_module_func(module_name, func_name)
```

**Parameters:**
- `module_name`: The name of the module where the dummy function was injected.
- `func_name`: The name of the dummy function to be reverted.

**Example:**
```python
import mpickle

# Clean up after using dummy module functions
mpickle.revert_dummy_module_func(
    module_name='custom_module',
    func_name='reconstruct_object'
)
```

## Classes

### Pickler

The `Pickler` class is used to serialize Python objects into a byte stream.

**Constructor:**
```python
Pickler(file, protocol=None, fix_imports=True)
```

**Parameters:**
- `file`: A file-like object with a `write()` method where the pickled data will be written.
- `protocol`: The protocol version to use for pickling. If `None`, the highest protocol version will be used.
- `fix_imports`: If `True`, pickle will try to map the new Python 3 names to the old module names used in Python 2, so that the pickle data stream is readable with Python 2.

**Methods:**
- `dump(obj)`: Pickles the given object and writes it to the file object passed to the constructor.

**Example:**
```python
import mpickle

# Create a Pickler instance
with open('data.pkl', 'wb') as f:
    pickler = mpickle.Pickler(f, protocol=4)
    pickler.dump({'a': 1, 'b': 2, 'c': 3})
    pickler.dump([1, 2, 3, 4, 5])
```

### Unpickler

The `Unpickler` class is used to deserialize Python objects from a byte stream.

**Constructor:**
```python
Unpickler(file, fix_imports=True, encoding="ASCII", errors="strict")
```

**Parameters:**
- `file`: A file-like object with a `readline()` and `read()` method from which the pickled data will be read.
- `fix_imports`: If `True`, pickle will try to map the old Python 2 names to the new module names used in Python 3.
- `encoding`: Tells pickle how to decode any instances of `str` objects from the pickle data stream.
- `errors`: Tells pickle how to deal with errors when decoding `str` objects.

**Methods:**
- `load()`: Reads a pickled object from the file object passed to the constructor and returns it.

**Example:**
```python
import mpickle

# Create an Unpickler instance
with open('data.pkl', 'rb') as f:
    unpickler = mpickle.Unpickler(f)
    dict_data = unpickler.load()  # Load the dictionary
    list_data = unpickler.load()  # Load the list
```

## Exceptions

### PickleError

The base class for all exceptions raised by the mPickle module.

```python
from mpickle import PickleError

try:
    # Some pickling operation
    pass
except PickleError as e:
    print(f"Pickle error occurred: {e}")
```

### PicklingError

Raised when an error occurs during the pickling process. This is a subclass of `PickleError`.

```python
from mpickle import PicklingError

try:
    # Attempt to pickle an unpicklable object
    import mpickle
    mpickle.dumps(lambda x: x)  # Functions can't be pickled
except PicklingError as e:
    print(f"Could not pickle object: {e}")
```

### UnpicklingError

Raised when an error occurs during the unpickling process. This is a subclass of `PickleError`.

```python
from mpickle import UnpicklingError

try:
    # Attempt to unpickle corrupted data
    import mpickle
    mpickle.loads(b"corrupted data")
except UnpicklingError as e:
    print(f"Could not unpickle data: {e}")
```
