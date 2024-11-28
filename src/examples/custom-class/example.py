try:
    import micropython #MicroPython
    import mpickle as pickle

    pickle.mpickle.DEBUG_MODE = False
except ImportError: #CPython
    import pickle

from custom_class import CustomClass, NestedClass

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

    test_objects = [
        CustomClass,
        CustomClass(arg_f=2+3j),
        NestedClass,
        NestedClass()
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