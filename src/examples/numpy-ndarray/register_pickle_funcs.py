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
# register_pickle_funcs.py - Support code for the numpy-ndarray example
#

# Importing necessary functions from the mpickle library for handling object serialization and module injection.
from mpickle.mpickle import (inject_fake_module_func, register_pickle)

# Importing the ulab library, which is commonly used in MicroPython environments to work with NumPy-like arrays.
import ulab

# Function to reduce a NumPy ndarray object into a format suitable for serialization.
# This function specifies how an ndarray should be broken down into its components for serialization.
def reduce_ndarray(x):
    # Injecting a function from a fake module to handle array reconstruction during deserialization.
    func = inject_fake_module_func("numpy.core.multiarray", "_reconstruct")
    # Returning a tuple of reconstruction information, including type, shape, data type, and the actual data as bytes.
    return (func, (type(x), (0,), b'b'), (1, x.shape, x.dtype, False, bytes(x.tobytes())))

# A dictionary to support specific data types for reducing them during serialization.
# This dictionary maps different ulab data types to tuples that describe how each type should be handled.
reduce_dtype_matrix = {
    str(ulab.dtype('int8')): (ulab.dtype, ('i1', False, True), (3, '|', None, None, None, -1, -1, 0)),
    str(ulab.dtype('int16')): (ulab.dtype, ('i2', False, True), (3, '<', None, None, None, -1, -1, 0)),
    str(ulab.dtype('uint8')): (ulab.dtype, ('u1', False, True), (3, '|', None, None, None, -1, -1, 0)),
    str(ulab.dtype('uint16')): (ulab.dtype, ('u2', False, True), (3, '<', None, None, None, -1, -1, 0)),
    str(ulab.dtype('float8')): (ulab.dtype, ('f4', False, True), (3, '<', None, None, None, -1, -1, 0)),
    str(ulab.dtype('float16')): (ulab.dtype, ('f4', False, True), (3, '<', None, None, None, -1, -1, 0)),
    str(ulab.dtype('float32')): (ulab.dtype, ('f4', False, True), (3, '<', None, None, None, -1, -1, 0)),
    str(ulab.dtype('float64')): (ulab.dtype, ('f4', False, True), (3, '<', None, None, None, -1, -1, 0)),
    str(ulab.dtype('complex64')): (ulab.dtype, ('c8', False, True), (3, '<', None, None, None, -1, -1, 0)),
    str(ulab.dtype('complex128')): (ulab.dtype, ('c8', False, True), (3, '<', None, None, None, -1, -1, 0)),
    str(ulab.dtype('complex256')): (ulab.dtype, ('c8', False, True), (3, '<', None, None, None, -1, -1, 0)),
    str(ulab.dtype('float')): (ulab.dtype, ('f4', False, True), (3, '<', None, None, None, -1, -1, 0)),
    str(ulab.dtype('complex')): (ulab.dtype, ('c8', False, True), (3, '<', None, None, None, -1, -1, 0))
}

# A dictionary for reconstructing specific data types from reduced representations during deserialization.
# It maps strings representing data types to actual ulab dtype objects.
reconstruct_dtype_matrix = {
    "i1": ulab.dtype('int8'),
    "i2": ulab.dtype('int16'),
    "u1": ulab.dtype('uint8'),
    "u2": ulab.dtype('uint16'),
    "f4": ulab.dtype('float32'),
    "c8": ulab.dtype('complex')
}

# A dictionary to convert between ulab data types and their NumPy equivalents.
# This helps convert ulab dtypes into standard NumPy dtypes.
dtype_convert_matrix = {
    str(ulab.dtype('int8')): ulab.numpy.int8,
    str(ulab.dtype('int16')): ulab.numpy.int16,
    str(ulab.dtype('uint8')): ulab.numpy.uint8,
    str(ulab.dtype('uint16')): ulab.numpy.uint16,
    str(ulab.dtype('float32')): ulab.numpy.float,
    str(ulab.dtype('complex')): ulab.numpy.complex
}

# Function to reduce a dtype object into a suitable form for serialization.
def reduce_dtype(x):
    return reduce_dtype_matrix[str(x)]

# Function to reconstruct an ndarray object from its reduced representation.
# This function takes a class type, a base, and a state, and returns an empty ndarray object.
def reconstructor_ndarray(cls, base, state):
    # print(f"reconstructor_ndarray - CLS={cls}, BASE={base}, STATE={state}")
    return cls([])

# Function to reconstruct a dtype object based on its serialized form.
# It looks up the appropriate dtype in the reconstruct_dtype_matrix.
def reconstructor_dtype(*args):
    dtype_str = args[0]
    # print(f"reconstructor_dtype - Type={dtype_str}")
    if dtype_str in reconstruct_dtype_matrix:
        return reconstruct_dtype_matrix[dtype_str]
    else:
        raise ValueError(f"Dtype {dtype_str} is not available")

# Function to set the state of an ndarray during deserialization.
# This includes reshaping the ndarray based on the provided shape and dtype.
def setstate_ndarray(inst, state):
    # print(f"setstate_ndarray - INST={inst}({type(inst)}) STATE={state}({type(state)})")

    shape = state[1]
    dtype = state[2]
    data = state[4]

    # print(f"setstate_ndarray - SHAPE={shape}({type(shape)}) DTYPE={dtype}({type(dtype)}) DATA={data}({type(data)})")

    # Create a new ndarray from the buffer data, dtype, and reshape it to the original shape.
    inst = ulab.numpy.frombuffer(data, dtype=dtype_convert_matrix[str(dtype)]).reshape(shape)

    # print(inst)
    return inst

# Register the pickling and unpickling functions for the ulab numpy ndarray.
# This ensures that ndarrays can be properly serialized and deserialized.
register_pickle(obj_type=ulab.numpy.ndarray, 
                obj_full_name="ulab.numpy.ndarray",
                obj_module="ulab",
                obj_reconstructor_func=None,
                reduce_func=reduce_ndarray,
                reconstruct_func=reconstructor_ndarray,
                setstate_func=setstate_ndarray,
                map_obj_module="numpy",
                map_obj_full_name="numpy.ndarray",
                map_reconstructor_func="numpy.core.multiarray._reconstruct") # Missing the map of the reconstruction function

# Register the pickling and unpickling functions for the ulab dtype.
# This ensures that dtypes can be properly serialized and deserialized.
register_pickle(obj_type=ulab.dtype, 
                obj_full_name="ulab.dtype",
                obj_module="ulab",
                obj_reconstructor_func=None,  # The reconstruction function is explicitly passed via reconstruct_func
                reduce_func=reduce_dtype,
                reconstruct_func=reconstructor_dtype,
                setstate_func=None,
                map_obj_module="numpy",
                map_obj_full_name="numpy.dtype",
                map_reconstructor_func="numpy.dtype")
