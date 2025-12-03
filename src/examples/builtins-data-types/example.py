# -----------------------------------------------------------------------------
# MIT License
# 
# Copyright (c) 2025 Mattia Antonini (Fondazione Bruno Kessler) m.antonini@fbk.eu
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
# -----------------------------------------------------------------------------
#
# example.py - Main code for the builtins-data-types example
#
try:
    import micropython #MicroPython
    import mpickle as pickle
except ImportError: #CPython
    import pickle

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
        ({'key1': 'value1'}, [1, 2, {3, 4}]),  # Nested dict in tuple
        range(0, 10, 2)        # Range object
    ]

def objects_equal(obj1, obj2):
    """
    Compare two objects for equality, handling sets and other unordered types.
    """
    if type(obj1) != type(obj2):
        return False
    
    # Handle sets and frozensets (unordered comparison)
    if isinstance(obj1, (set, frozenset)):
        return obj1 == obj2
    
    # Handle ranges
    if isinstance(obj1, range):
        return list(obj1) == list(obj2)
    
    # Handle lists and tuples (recursive comparison)
    if isinstance(obj1, list):
        if len(obj1) != len(obj2):
            return False
        return all(objects_equal(item1, item2) for item1, item2 in zip(obj1, obj2))
    
    if isinstance(obj1, tuple):
        if len(obj1) != len(obj2):
            return False
        return all(objects_equal(item1, item2) for item1, item2 in zip(obj1, obj2))
    
    # Handle dictionaries (recursive comparison of values)
    if isinstance(obj1, dict):
        if set(obj1.keys()) != set(obj2.keys()):
            return False
        return all(objects_equal(obj1[key], obj2[key]) for key in obj1.keys())
    
    # Standard equality for other types
    return obj1 == obj2

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
        print(f"Objects match? {objects_equal(obj, deserialized)}")
    except Exception as e:
        print(f"Error with {obj}: {e}")

def main():
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
