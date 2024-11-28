class CustomClass:
    def __init__(self, arg_f=1+4j):
        self.A = 2
        self.B = 'foo'
        self.C = [1, 2, 3]  # A list to test more pickle
        self.D = {'key1': 'value1', 'key2': 'value2'}  # A dictionary to test pickling nested objects
        self.E = NestedClass()  # An instance of a nested class for pickling
        self.F = arg_f
    
    def add(self, A: int):
        return A + self.A
    
    def concat(self, B: str):
        return B + self.B
    
    def append_to_list(self, value):
        self.C.append(value)
        return self.C
    
    def update_dict(self, key, value):
        self.D[key] = value
        return self.D

    def abs_complex(self):
        return abs(self.F)

    def __eq__(self, other):
        if not isinstance(other, CustomClass):
            return False
        return (self.A == other.A and
                self.B == other.B and
                self.C == other.C and
                self.D == other.D and
                self.E == other.E and
                self.F == other.F)

class NestedClass:
    def __init__(self):
        self.value = "I'm nested"
    
    def greet(self):
        return "Hello from the nested class!"
    
    def __eq__(self, other):
        # Assuming that instances of NestedClass are always equal if they are the same type.
        # Update this logic if NestedClass has attributes that need comparison.
        return isinstance(other, NestedClass)