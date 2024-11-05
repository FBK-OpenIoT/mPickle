try:
    import pickle
    import numpy 
except:
    import mpickle as pickle
    from ulab import numpy

def load(filename='dump'):
    with open(filename, 'br') as file:
        print(obj := pickle.load(file=file))
        return obj

def dump(obj: any, filename='dump'):
    print(obj)
    with open(filename, 'bw') as file:
        return pickle.dump(obj, file=file)

