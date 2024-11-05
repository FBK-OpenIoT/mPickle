class CustomClass:
    def __init__(self):
        self.A = 2
        self.B = 'foo'
    
    def add(self, A: int):
        return A+self.A
    
    def concat(self, B: str):
        return B+self.B

def example():
    try:
        import pickle as pickle
    except:
        import mpickle as pickle

    test_objects = [
        CustomClass,
        CustomClass()
    ]
    
    for obj in test_objects:
        dump = pickle.dumps(obj)
        print(f'object of {type(obj)}: {obj} encodes to: {dump}')