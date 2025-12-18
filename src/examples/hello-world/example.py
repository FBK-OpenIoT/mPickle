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
# example.py - Main code for the hello-world example
#
try:
    import micropython #MicroPython
    import mpickle
    IS_MICROPYTHON = True
except ImportError: #CPython
    raise ImportError("This example is intended to be run in a MicroPython environment.")

def main():

    print("\n=== mPickle Hello World Example ===\n")
    print("mPickle available:", IS_MICROPYTHON, "\n")

    # String serialization and deserialization with mPickle
    my_string = "Hello, I am using mPickle!"
    
    serialized_string = mpickle.dumps(my_string)  # Serialize the string
    deserialized_string = mpickle.loads(serialized_string)  # Deserialize the string

    print("Original string:", my_string)
    print("Serialized string:", serialized_string)
    print("Deserialized string:", deserialized_string)

    print("\n=======================================\n")

    # String serialization and deserialization with mPickle
    my_number = 42    

    serialized_number = mpickle.dumps(my_number)  # Serialize the number
    deserialized_number = mpickle.loads(serialized_number)  # Deserialize the number

    print("Original number:", my_number)
    print("Serialized number:", serialized_number)
    print("Deserialized number:", deserialized_number)

if __name__ == "__main__":
    main()
