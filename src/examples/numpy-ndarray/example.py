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
# example.py - Main code for the numpy-ndarray example
#

try:
    import micropython #MicroPython
    import mpickle as pickle
    from ulab import numpy as np, dtype

    import register_pickle_funcs

    pickle.mpickle.DEBUG_MODE = False
except ImportError: #CPython
    import pickle
    import numpy as np
    from numpy import dtype

test_array = [int(x) for x in range(64)]
test_objects = [
    np.array(test_array, dtype=dtype('int16')),                     # 1D array with 64 int16 numbers
    np.array(test_array, dtype=dtype('int16')).reshape((8,8)),      # 2D array (4x4) with 64 int16 numbers
    np.array(test_array, dtype=dtype('int16')).reshape((4,4,4)),    # 3D array (4x2x2) with 64 int16 numbers
    np.array(test_array, dtype=dtype('int16')).reshape((4,2,2,4)),  # 4D array (2x2x2x2) with 64 int16 numbers
    np.array(test_array, dtype=dtype('float32')),                     # 1D array with 64 float32 numbers
    np.array(test_array, dtype=dtype('float32')).reshape((8,8)),      # 2D array (4x4) with 64 float32 numbers
    np.array(test_array, dtype=dtype('float32')).reshape((4,4,4)),    # 3D array (4x2x2) with 64 float32 numbers
    np.array(test_array, dtype=dtype('float32')).reshape((4,2,2,4)),  # 4D array (2x2x2x2) with 64 float32 numbers
]

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
        print(f"Serialized ({len(serialized)} bytes): \n\n{serialized}\n")
        deserialized = pickle.loads(serialized)
        print(f"Deserialized: {deserialized}")
        if type(obj) is list:
            print(f"\nObjects match? {obj == deserialized}")
        else:
            print(f"\nObjects match? {list(obj.tolist()) == list(deserialized.tolist())}")
    except Exception as e:
        print(f"Error with {obj}: {e}")

def main():
   
    # Serialize individual test objects
    for obj in test_objects:
        print(f"Testing Object: {obj} (Type: {type(obj)})")
        serialize_and_deserialize(obj)
        print("\n" + "="*50)

    # # Serialize the entire list of test objects
    print("Testing all objects as a single collection")
    serialize_and_deserialize(test_objects)

if __name__ == "__main__":
    main()