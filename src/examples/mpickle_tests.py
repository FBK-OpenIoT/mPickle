import sys
import argparse

try:
    import micropython  # MicroPython
    import mpickle as pickle
    from ulab import numpy as np
except ImportError:  # CPython
    import pickle
    import numpy as np

DUMP_FILE = "dump.pkl"

def serialize_data(test_objects):
    try:
        with open(DUMP_FILE, "wb") as f:
            pickle.dump(test_objects, f)
        print(f"Data successfully serialized to {DUMP_FILE}")
    except Exception as e:
        print(f"Serialization failed: {e}")

def arrays_are_equal(arr1, arr2):
    """Compare two ulab arrays element-wise"""
    if arr1.shape != arr2.shape:  # Ensure same shape
        return False
    return np.sum(arr1 == arr2) == arr1.size  # Compare element-wise

def deserialize_data(test_objects):
    success_count = 0
    fail_count = len(test_objects)
    try:
        with open(DUMP_FILE, "rb") as f:
            loaded_data = pickle.load(f)

            #fix the problem of float32 and float 64
            tollerance = 1e-7
            for i in range(len(loaded_data)):
                if type(loaded_data[i]) is float:
                    new_obj = int(loaded_data[i] * (1/tollerance))
                    loaded_data[i] = float(new_obj)/(1/tollerance)

        results = []
        for obj in test_objects:
            if isinstance(obj, np.ndarray) and any(arrays_are_equal(obj, item) for item in loaded_data):
                    results.append(("✅", obj))
            elif obj in loaded_data:
                    results.append(("✅", obj))
            else:
                results.append(("❌", obj))
            success_count = sum(1 for status, _ in results if status == "✅")
            fail_count = len(test_objects) - success_count

        print("\n".join(f"{type(obj).__name__} : {obj} {status}" for status, obj in results))

    except Exception as e:
        print(f"Deserialization failed: {e}")
        # sys.exit(-1)
    
    print(f"\n✅ {success_count} successful | ❌ {fail_count} failed | 📦 Total: {len(test_objects)}")

    if success_count == len(test_objects):
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Serialize and deserialize Python objects for a given example.")
    parser.add_argument("--example_name", type=str, help="Name of the example to serialize/deserialize.")
    parser.add_argument("--dump", action="store_true", help="Serialize and save data.")
    parser.add_argument("--load", action="store_true", help="Deserialize and verify data.")
    args = parser.parse_args()

    # import the example
    example_name = args.example_name
    sys.path.append(example_name)
    #remove example from modules after importing test_objects, this helps mpickle to solve modules
    from example import test_objects
    sys.modules.pop("example")

    if args.dump:
        serialize_data(test_objects)
    elif args.load:
        deserialize_data(test_objects)
    else:
        print("❌ You must specify either --dump or --load")
        parser.print_help()
