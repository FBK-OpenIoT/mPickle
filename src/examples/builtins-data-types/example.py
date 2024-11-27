"""
This script demonstrates the process of serializing and deserializing various types of Python objects using 
the `pickle` and `mPickle` libraries. Serialization is the process of converting a Python object into a byte stream, which can 
then be saved to a file or transmitted over a network. Deserialization is the reverse process, where the byte 
stream is converted back into the original Python object.

### Purpose and Importance:
1. **Cross-Environment Compatibility**:
   The script checks for different environments (e.g., MicroPython or standard Python). It demonstrates how the 
   appropriate module (`mpickle` or `pickle`) can be imported based on the environment, which is crucial for 
   ensuring code portability across different Python runtimes.

2. **Comprehensive Data Type Coverage**:
   The script tests various data types, including strings, numbers, collections, nested structures, and more. 
   This is important because it allows us to ensure that all common data types can be successfully serialized 
   and deserialized without data loss or corruption.

### Application:
This example can be useful for developers who need to:
- Understand how to persist different types of Python data.
- Share complex data structures between different parts of an application.
- Develop software that needs to save state between executions.

The script uses a modular approach, making it easy to reuse the serialization logic in other projects.
"""

try:
    import micropython #MicroPython
    import mpickle as pickle
except ImportError: #CPython
    import pickle

def serialize_and_deserialize(obj):
    """
    This function attempts to serialize and deserialize the given object using the pickle module.
    If successful, it prints the serialized byte stream, the deserialized object, and verifies 
    if the deserialized object matches the original.

    Parameters:
    obj (any): The Python object to be serialized and deserialized.
    """
    try:
        serialized = pickle.dumps(obj)
        print(f"Serialized: {serialized}")
        deserialized = pickle.loads(serialized)
        print(f"Deserialized: {deserialized}")
        print(f"Objects match? {obj == deserialized}")
    except Exception as e:
        print(f"Error with {obj}: {e}")

def main():
    test_objects = [
        'foo',                 # String
        12,                    # Integer
        1.2,                   # Float
        1 + 2j,                # Complex number
        True,                  # Boolean
        bytes(1),              # Bytes
        bytearray('foo', 'utf-8'), # Bytearray
        [1, 2, 3],             # List
        (1, 2, 3),             # Tuple
        {1, 2, 'foo', 'bar'},  # Set
        {'foo': 'bar'},        # Dictionary
        None,                  # NoneType
        frozenset(['a', 'b', 'c']), # Immutable Set
        [[1, 2], {'foo': (3, 4)}, {5: [6, 7]}],  # Nested array
        ({'key1': 'value1'}, [1, 2, {3, 4}])  # Nested dict in tuple
    ]

    # Serialize individual test objects
    for obj in test_objects:
        print(f"Testing Object: {obj} (Type: {type(obj)})")
        serialize_and_deserialize(obj)
        print("\n" + "="*50)

    # Serialize the entire list of test objects
    print("Testing all objects as a single collection")
    serialize_and_deserialize(test_objects)

if __name__ == "__main__":
    main()
