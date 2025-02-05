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
# example.py - Main code for the custom-class example
#

try:
    import micropython #MicroPython
    import mpickle as pickle

    pickle.mpickle.DEBUG_MODE = False
except ImportError: #CPython
    import pickle

from custom_class import CustomClass, NestedClass

test_objects = [
        CustomClass,
        CustomClass(arg_f=2+3j),
        NestedClass,
        NestedClass()
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
        print(f"Serialized ({len(serialized)} bytes): {serialized}")
        deserialized = pickle.loads(serialized)
        print(f"Deserialized: {deserialized}")
        print(f"Objects match? {obj == deserialized}")
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