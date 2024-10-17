from mpickle import (inject_fake_module_func,
                     register_pickle)
import ulab

def reduce_ndarray(x):
    func = inject_fake_module_func("numpy.core.multiarray", "_reconstruct")
    return (func, (type(x), (0,), b'b'), (1, x.shape, x.dtype, False, bytes(x.tobytes())) )

# SUpports for only these data types
reduce_dtype_matrix= {
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

reconstruct_dtype_matrix = {
    "i1": ulab.dtype('int8'),
    "i2": ulab.dtype('int16'),
    "u1": ulab.dtype('uint8'),
    "u2": ulab.dtype('uint16'),
    "f4": ulab.dtype('float32'),
    "c8": ulab.dtype('complex')
}

dtype_convert_matrix = {
    str(ulab.dtype('int8')): ulab.numpy.int8,
    str(ulab.dtype('int16')): ulab.numpy.int16,
    str(ulab.dtype('uint8')): ulab.numpy.uint8,
    str(ulab.dtype('uint16')): ulab.numpy.uint16,
    str(ulab.dtype('float32')): ulab.numpy.float,
    str(ulab.dtype('complex')): ulab.numpy.complex
}

def reduce_dtype(x):
    return reduce_dtype_matrix[str(x)]

def reconstructor_ndarray(cls, base, state):
    print(f"reconstructor_ndarray - CLS={cls}, BASE={base}, STATE={state}")
    return cls([])

def reconstructor_dtype(*args):
    dtype_str = args[0]
    print(f"reconstructor_dtype - Type={dtype_str}")
    if dtype_str in reconstruct_dtype_matrix:
        return reconstruct_dtype_matrix[dtype_str]
    else:
        raise ValueError(f"Dtype {dtype_str} is not available")

def setstate_ndarray(inst, state):
    print(f"setstate_ndarray - INST={inst}({type(inst)}) STATE={state}({type(state)})")

    shape = state[1]
    dtype = state[2]
    data = state[4]

    print(f"setstate_ndarray - SHAPE={shape}({type(shape)}) DTYPE={dtype}({type(dtype)}) DATA={data}({type(data)})")

    inst = ulab.numpy.frombuffer(data, dtype=dtype_convert_matrix[str(dtype)]).reshape(shape)

    print(inst)
    return inst
    

register_pickle(obj_type=ulab.numpy.ndarray, 
                obj_full_name="ulab.numpy.ndarray",
                obj_module="ulab",
                obj_reconstructor_func=None,
                reduce_func=reduce_ndarray,
                reconstruct_func=reconstructor_ndarray,
                setstate_func=setstate_ndarray,
                map_obj_module="numpy",
                map_obj_full_name="numpy.ndarray",
                map_reconstructor_func="numpy.core.multiarray._reconstruct") # miss the map of the reconstruction funtion

register_pickle(obj_type=ulab.dtype, 
                obj_full_name="ulab.dtype",
                obj_module="ulab",
                obj_reconstructor_func=None, # the reconstruction function is excplicity passed via reconstruct_func, otherise it uses the packaged func
                reduce_func=reduce_dtype,
                reconstruct_func=reconstructor_dtype,
                setstate_func=None,
                map_obj_module="numpy",
                map_obj_full_name="numpy.dtype",
                map_reconstructor_func="numpy.dtype")