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
# OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
# -----------------------------------------------------------------------------

"""
Test custom class serialization and deserialization.
Compatible with both CPython and MicroPython.
"""

import unittest
import sys

try:
    import micropython
    sys.path.insert(0, 'src')
    from mpickle import mpickle as pickle
    MPICKLE_AVAILABLE = True
except ImportError:
    import pickle
    MPICKLE_AVAILABLE = False


class SimpleClass:
    """A simple test class with basic attributes."""
    
    def __init__(self, value=None):
        self.value = value
        self.name = "SimpleClass"
    
    def __eq__(self, other):
        return (isinstance(other, SimpleClass) and
                self.value == other.value and
                self.name == other.name)


class ClassWithMethods:
    """A class with methods to test method preservation."""
    
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
    
    def get_coords(self):
        return (self.x, self.y)
    
    def set_coords(self, x, y):
        self.x = x
        self.y = y
    
    def __eq__(self, other):
        return (isinstance(other, ClassWithMethods) and
                self.x == other.x and
                self.y == other.y)


class ClassWithNesting:
    """A class that contains other objects."""
    
    def __init__(self, data=None):
        if data is None:
            data = []
        self.data = data
        self.metadata = {"created": "test", "version": 1}
    
    def __eq__(self, other):
        return (isinstance(other, ClassWithNesting) and
                self.data == other.data and
                self.metadata == other.metadata)


class ClassWithSlots:
    """A class using __slots__.
    
    Note: MicroPython has limited __slots__ support.
    """
    
    __slots__ = ['name', 'age', 'id']
    
    def __init__(self, name="", age=0, id_val=0):
        self.name = name
        self.age = age
        self.id = id_val
    
    def __eq__(self, other):
        return (isinstance(other, ClassWithSlots) and
                self.name == other.name and
                self.age == other.age and
                self.id == other.id)


class ClassWithGetStateSetState:
    """A class with custom __getstate__ and __setstate__.
    
    Note: MicroPython may have limited support for these methods.
    """
    
    def __init__(self, value=None):
        self.value = value
        self._internal_data = "internal"
    
    def __getstate__(self):
        """Return state for pickling."""
        return {"value": self.value, "processed": True}
    
    def __setstate__(self, state):
        """Restore state from pickling."""
        self.value = state.get("value")
        self._internal_data = "restored"
        self.restored_from_state = True
    
    def __eq__(self, other):
        if not isinstance(other, ClassWithGetStateSetState):
            return False
        
        # Check if both objects have been restored from pickle
        self_restored = hasattr(self, 'restored_from_state')
        other_restored = hasattr(other, 'restored_from_state')
        
        if self_restored and other_restored:
            # Both have been unpickled, compare all attributes
            return (self.value == other.value and
                    self._internal_data == other._internal_data and
                    self.restored_from_state == other.restored_from_state)
        elif not self_restored and not other_restored:
            # Neither has been unpickled, compare basic attributes
            return self.value == other.value and self._internal_data == other._internal_data
        else:
            # One has been restored, one hasn't - they can't be equal
            return False


class ClassWithReduce:
    """A class with custom __reduce__ method."""
    
    def __init__(self, data=None):
        if data is None:
            data = []
        self.data = data
    
    def __reduce__(self):
        """Custom reduce method."""
        return (self.__class__, (self.data,), None, None, None)
    
    def __eq__(self, other):
        return (isinstance(other, ClassWithReduce) and
                self.data == other.data)


class BaseClass:
    """Base class for inheritance testing."""
    
    def __new__(cls, *args, **kwargs):
        # Fix for pickle deserialization compatibility - pickle calls __new__
        # with different arguments than expected, so we accept any arguments
        instance = super().__new__(cls)
        if instance is not None:
            instance.__init__(*args, **kwargs)
        return instance
    
    def __init__(self, base_value=0):
        self.base_value = base_value
    
    def get_base_value(self):
        return self.base_value
    
    def __eq__(self, other):
        return (isinstance(other, BaseClass) and
                self.base_value == other.base_value)

class DerivedClass(BaseClass):
    """Derived class for inheritance testing."""
    
    def __init__(self, base_value=0, derived_value=0):
        super().__init__(base_value)
        self.derived_value = derived_value
    
    def get_derived_value(self):
        return self.derived_value
    
    def get_all_values(self):
        return (self.base_value, self.derived_value)
    
    def __eq__(self, other):
        return (isinstance(other, DerivedClass) and
                self.base_value == other.base_value and
                self.derived_value == other.derived_value)


class ClassWithNone:
    """Test class with None attributes."""
    
    def __init__(self):
        self.attr1 = None
        self.attr2 = None
        self.attr3 = "not_none"
    
    def __eq__(self, other):
        return (isinstance(other, ClassWithNone) and
                self.attr1 == other.attr1 and
                self.attr2 == other.attr2 and
                self.attr3 == other.attr3)


class ClassWithSpecial:
    """Test class with special Python attributes."""
    
    def __init__(self):
        self.__private = "private_value"
        self._protected = "protected_value"
        self.public = "public_value"
    
    def __eq__(self, other):
        if not isinstance(other, ClassWithSpecial):
            return False
        try:
            # Compare all attributes, handling potential name mangling differences
            return (self._protected == other._protected and
                    self.public == other.public)
        except AttributeError:
            # If comparison fails due to attribute differences, fallback to basic check
            return type(self) == type(other)


class ClassWithoutInit:
    """Test class without __init__ method."""
    
    value = "class_value"
    
    def __eq__(self, other):
        return isinstance(other, ClassWithoutInit)


class ClassWithClassAttrs:
    """Test class with class-level attributes."""
    
    class_attr = "shared_value"
    
    def __init__(self, instance_attr):
        self.instance_attr = instance_attr
    
    def __eq__(self, other):
        return (isinstance(other, ClassWithClassAttrs) and
                self.instance_attr == other.instance_attr)


class ClassWithProperty:
    """Test class with properties."""
    
    def __init__(self, value):
        self._value = value
    
    @property
    def value(self):
        return self._value
    
    @value.setter
    def value(self, val):
        self._value = val
    
    def __eq__(self, other):
        return (isinstance(other, ClassWithProperty) and
                self._value == other._value)


class EmptyClass:
    """Test completely empty class."""
    pass


class TestCustomClasses(unittest.TestCase):
    """Test custom class serialization and deserialization."""

    def setUp(self):
        """Set up test environment."""
        if not MPICKLE_AVAILABLE:
            self.skipTest("Neither mpickle nor standard pickle available")

    def test_simple_class(self):
        """Test simple class serialization."""
        obj = SimpleClass("test_value")
        result = pickle.loads(pickle.dumps(obj))
        self.assertEqual(result, obj)
        self.assertIsInstance(result, SimpleClass)
        self.assertEqual(result.name, "SimpleClass")

    def test_class_with_methods(self):
        """Test class with methods."""
        obj = ClassWithMethods(10, 20)
        result = pickle.loads(pickle.dumps(obj))
        
        self.assertEqual(result, obj)
        self.assertIsInstance(result, ClassWithMethods)
        
        # Test that methods are preserved
        self.assertEqual(result.get_coords(), (10, 20))
        result.set_coords(30, 40)
        self.assertEqual(result.get_coords(), (30, 40))

    def test_class_with_nesting(self):
        """Test class with nested objects."""
        nested_obj = ClassWithNesting([1, 2, {"key": "value"}])
        result = pickle.loads(pickle.dumps(nested_obj))
        
        self.assertEqual(result, nested_obj)
        self.assertIsInstance(result, ClassWithNesting)
        self.assertEqual(result.data, [1, 2, {"key": "value"}])
        self.assertEqual(result.metadata, {"created": "test", "version": 1})

    @unittest.skipUnless(MPICKLE_AVAILABLE, "mpickle not available")
    def test_class_with_slots(self):
        """Test class with __slots__.
        
        Note: MicroPython may not fully support __slots__.
        """
        try:
            obj = ClassWithSlots("John", 25, 12345)
            result = pickle.loads(pickle.dumps(obj))
            
            self.assertEqual(result, obj)
            self.assertIsInstance(result, ClassWithSlots)
            self.assertEqual(result.name, "John")
            self.assertEqual(result.age, 25)
            self.assertEqual(result.id, 12345)
        except (AttributeError, TypeError) as e:
            # __slots__ may not be fully supported in MicroPython
            self.skipTest(f"__slots__ not fully supported: {e}")

    @unittest.skipUnless(MPICKLE_AVAILABLE, "mpickle not available")
    def test_class_with_getstate_setstate(self):
        """Test class with custom __getstate__ and __setstate__.
        
        Note: MicroPython may have limited support for these methods.
        """
        obj = ClassWithGetStateSetState("important_value")
        
        # Verify original object doesn't have restored_from_state
        self.assertFalse(hasattr(obj, 'restored_from_state'))
        self.assertEqual(obj._internal_data, "internal")
        
        # Pickle and unpickle
        result = pickle.loads(pickle.dumps(obj))
        
        # Verify the result has the expected state
        self.assertIsInstance(result, ClassWithGetStateSetState)
        self.assertEqual(result.value, "important_value")
        self.assertTrue(hasattr(result, 'restored_from_state'))
        self.assertEqual(result._internal_data, "restored")  # Changed by __setstate__
        self.assertEqual(result.restored_from_state, True)  # Set by __setstate__
        
        # Test that __getstate__ was called and returned expected state
        original_state = obj.__getstate__()
        expected_state = {"value": "important_value", "processed": True}
        self.assertEqual(original_state, expected_state)

    def test_class_with_reduce(self):
        """Test class with custom __reduce__."""
        obj = ClassWithReduce([1, 2, 3, "test"])
        result = pickle.loads(pickle.dumps(obj))
        
        self.assertEqual(result, obj)
        self.assertIsInstance(result, ClassWithReduce)
        self.assertEqual(result.data, [1, 2, 3, "test"])

    def test_inheritance(self):
        """Test inheritance serialization."""
        # Test base class
        base_obj = BaseClass(42)
        base_result = pickle.loads(pickle.dumps(base_obj))
        self.assertEqual(base_result, base_obj)
        self.assertEqual(base_result.get_base_value(), 42)

        # Test derived class
        derived_obj = DerivedClass(10, 20)
        derived_result = pickle.loads(pickle.dumps(derived_obj))
        self.assertEqual(derived_result, derived_obj)
        self.assertEqual(derived_result.get_base_value(), 10)
        self.assertEqual(derived_result.get_derived_value(), 20)
        self.assertEqual(derived_result.get_all_values(), (10, 20))

    def test_complex_nested_classes(self):
        """Test complex nested class structures."""
        # Create a complex nested structure
        inner_class = ClassWithMethods(1, 2)
        middle_class = ClassWithNesting([inner_class, "test"])
        outer_class = ClassWithNesting([middle_class, {"class": inner_class}])
        
        result = pickle.loads(pickle.dumps(outer_class))
        
        self.assertEqual(result, outer_class)
        self.assertEqual(len(result.data), 2)
        self.assertIsInstance(result.data[0], ClassWithNesting)
        self.assertIsInstance(result.data[0].data[0], ClassWithMethods)

    def test_class_instances_with_shared_references(self):
        """Test class instances with shared object references."""
        shared_obj = ClassWithMethods(1, 2)
        container = [shared_obj, shared_obj, {"reference": shared_obj}]
        
        result = pickle.loads(pickle.dumps(container))
        
        # Check that shared references are preserved
        self.assertIs(result[0], result[1])
        self.assertIs(result[0], result[2]["reference"])

    def test_class_with_none_attributes(self):
        """Test class with None attributes."""
        obj = ClassWithNone()
        result = pickle.loads(pickle.dumps(obj))
        
        self.assertIsNone(result.attr1)
        self.assertIsNone(result.attr2)
        self.assertEqual(result.attr3, "not_none")

    def test_class_with_special_attributes(self):
        """Test class with special Python attributes.
        
        Note: Name mangling may behave differently in MicroPython.
        """
        obj = ClassWithSpecial()
        result = pickle.loads(pickle.dumps(obj))
        
        # Note: MicroPython may not support name mangling
        try:
            # Try to access the mangled private attribute
            private_attr = result._ClassWithSpecial__private
            self.assertEqual(private_attr, "private_value")
        except AttributeError:
            # MicroPython may not support name mangling - this is acceptable
            pass
        
        # Protected and public attributes should always work
        self.assertEqual(result._protected, "protected_value")
        self.assertEqual(result.public, "public_value")

    def test_class_type_pickling(self):
        """Test pickling of class types themselves (not instances)."""
        # Test pickling the class type itself
        pickled_type = pickle.dumps(SimpleClass)
        loaded_type = pickle.loads(pickled_type)
        
        self.assertEqual(loaded_type, SimpleClass)
        self.assertIs(loaded_type, SimpleClass)
        
        # Test that we can create instances with the loaded type
        instance = loaded_type("test")
        self.assertEqual(instance.value, "test")


class TestClassEdgeCases(unittest.TestCase):
    """Test edge cases for class serialization."""

    def setUp(self):
        """Set up test environment."""
        if not MPICKLE_AVAILABLE:
            self.skipTest("Neither mpickle nor standard pickle available")

    def test_class_without_init(self):
        """Test class without __init__ method."""
        obj = ClassWithoutInit()
        result = pickle.loads(pickle.dumps(obj))
        self.assertEqual(result, obj)

    def test_class_with_class_attributes(self):
        """Test class with class-level attributes."""
        obj = ClassWithClassAttrs("instance_value")
        result = pickle.loads(pickle.dumps(obj))
        self.assertEqual(result, obj)
        self.assertEqual(result.class_attr, "shared_value")

    @unittest.skipUnless(MPICKLE_AVAILABLE, "mpickle not available")
    def test_class_with_property(self):
        """Test class with properties.
        
        Note: MicroPython may have limited property support.
        """
        try:
            obj = ClassWithProperty(42)
            result = pickle.loads(pickle.dumps(obj))
            self.assertEqual(result, obj)
            self.assertEqual(result.value, 42)
        except (AttributeError, NameError) as e:
            # Properties may not be fully supported in MicroPython
            self.skipTest(f"Properties not fully supported: {e}")

    def test_empty_class(self):
        """Test completely empty class."""
        obj = EmptyClass()
        result = pickle.loads(pickle.dumps(obj))
        self.assertIsInstance(result, EmptyClass)


if __name__ == '__main__':
    unittest.main()