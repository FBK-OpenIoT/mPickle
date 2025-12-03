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
Test serialization of all built-in Python data types.
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


class TestDataTypes(unittest.TestCase):
    """Test serialization and deserialization of all Python data types."""

    def test_none_type(self):
        """Test None type serialization."""
        result = pickle.loads(pickle.dumps(None))
        self.assertIsNone(result)

    def test_boolean_types(self):
        """Test boolean type serialization."""
        true_result = pickle.loads(pickle.dumps(True))
        self.assertIsInstance(true_result, bool)
        self.assertTrue(true_result)
        
        false_result = pickle.loads(pickle.dumps(False))
        self.assertIsInstance(false_result, bool)
        self.assertFalse(false_result)

    def test_integer_types(self):
        """Test integer type serialization."""
        # Small integers
        for value in [0, 1, -1, 42, -42, 255, -255]:
            result = pickle.loads(pickle.dumps(value))
            self.assertEqual(result, value)
            self.assertIsInstance(result, int)

        # Large integers
        large_int = 123456789012345678901234567890
        result = pickle.loads(pickle.dumps(large_int))
        self.assertEqual(result, large_int)

        # Negative large integers
        neg_large_int = -123456789012345678901234567890
        result = pickle.loads(pickle.dumps(neg_large_int))
        self.assertEqual(result, neg_large_int)

    def test_float_types(self):
        """Test float type serialization."""
        test_floats = [0.0, 1.0, -1.0, 3.14159265359, -2.71828182846]
        
        for value in test_floats:
            with self.subTest(value=value):
                result = pickle.loads(pickle.dumps(value))
                self.assertAlmostEqual(result, value, places=10)
                self.assertIsInstance(result, float)

        # Test infinity values (compatible with both CPython and MicroPython)
        inf_value = float('inf')
        result = pickle.loads(pickle.dumps(inf_value))
        self.assertTrue((result == inf_value) and (result != -result))

        neg_inf_value = float('-inf')
        result = pickle.loads(pickle.dumps(neg_inf_value))
        self.assertTrue((result == neg_inf_value) and (result != -result))

        # Test NaN (special case due to equality issues)
        nan_value = float('nan')
        result = pickle.loads(pickle.dumps(nan_value))
        # NaN is the only value that doesn't equal itself
        self.assertTrue(result != result)

    def test_complex_types(self):
        """Test complex number serialization."""
        test_complex = [
            0+0j,
            1+0j,
            0+1j,
            1+1j,
            -1-1j,
            3.14+2.71j,
            complex(1.5, -2.3)
        ]
        
        for value in test_complex:
            with self.subTest(value=value):
                result = pickle.loads(pickle.dumps(value))
                self.assertAlmostEqual(result.real, value.real, places=10)
                self.assertAlmostEqual(result.imag, value.imag, places=10)
                self.assertIsInstance(result, complex)

    def test_string_types(self):
        """Test string type serialization."""
        test_strings = [
            "",
            "hello",
            "Hello World!",
            "unicode: ñáéíóú 日本語",
            "special chars: !@#$%^&*()",
            "multiline\nstring\nwith\nnewlines",
            "tab\ttab\ttab",
            "backslash\\string",
            "quote'string\"",
        ]
        
        for value in test_strings:
            with self.subTest(value=value):
                result = pickle.loads(pickle.dumps(value))
                self.assertEqual(result, value)
                self.assertIsInstance(result, str)

    def test_bytes_types(self):
        """Test bytes type serialization."""
        test_bytes = [
            b"",
            b"hello",
            b"\x00\x01\x02\x03\xff",
            b"binary data \x00\x01\x02\x03",
        ]
        
        for value in test_bytes:
            with self.subTest(value=value):
                result = pickle.loads(pickle.dumps(value))
                self.assertEqual(result, value)
                self.assertIsInstance(result, bytes)

    def test_bytearray_types(self):
        """Test bytearray type serialization."""
        test_bytearrays = [
            bytearray(),
            bytearray(b"hello"),
            bytearray([0, 1, 2, 3, 255]),
        ]
        
        for value in test_bytearrays:
            with self.subTest(value=value):
                result = pickle.loads(pickle.dumps(value))
                self.assertEqual(bytes(result), bytes(value))
                self.assertIsInstance(result, bytearray)

    def test_list_types(self):
        """Test list type serialization."""
        test_lists = [
            [],
            [1, 2, 3],
            ["a", "b", "c"],
            [1, "two", 3.0, True, None],
            [[1, 2], [3, 4]],
            list(range(10)),
            [x**2 for x in range(5)],  # list comprehension
        ]
        
        for value in test_lists:
            with self.subTest(value=value):
                result = pickle.loads(pickle.dumps(value))
                self.assertEqual(result, value)
                self.assertIsInstance(result, list)

    def test_tuple_types(self):
        """Test tuple type serialization."""
        test_tuples = [
            (),
            (1,),
            (1, 2, 3),
            ("a", "b", "c"),
            (1, "two", 3.0, True, None),
            ((1, 2), (3, 4)),
            tuple(range(5)),
            tuple(x**2 for x in range(3)),  # generator comprehension
        ]
        
        for value in test_tuples:
            with self.subTest(value=value):
                result = pickle.loads(pickle.dumps(value))
                self.assertEqual(result, value)
                self.assertIsInstance(result, tuple)

    def test_dict_types(self):
        """Test dict type serialization."""
        test_dicts = [
            {},
            {"key": "value"},
            {"number": 42, "string": "hello", "bool": True},
            {"nested": {"dict": "value"}},
            dict([("a", 1), ("b", 2), ("c", 3)]),
            {i: i**2 for i in range(5)},  # dict comprehension
            {"mixed": [1, 2, 3], "tuple": (4, 5, 6), "nested": {"deep": "value"}},
        ]
        
        for value in test_dicts:
            with self.subTest(value=value):
                result = pickle.loads(pickle.dumps(value))
                self.assertEqual(result, value)
                self.assertIsInstance(result, dict)

    def test_set_types(self):
        """Test set type serialization."""
        test_sets = [
            set(),
            {1, 2, 3},
            {"a", "b", "c"},
            {1, "string", True},
            set([1, 2, 3, 2, 1]),  # duplicates should be removed
            {x for x in range(5) if x % 2 == 0},  # set comprehension
        ]
        
        for value in test_sets:
            with self.subTest(value=value):
                result = pickle.loads(pickle.dumps(value))
                self.assertEqual(result, value)
                self.assertIsInstance(result, set)

    def test_frozenset_types(self):
        """Test frozenset type serialization."""
        test_frozensets = [
            frozenset(),
            frozenset([1, 2, 3]),
            frozenset(["a", "b", "c"]),
            frozenset([1, "string", True]),
        ]
        
        for value in test_frozensets:
            with self.subTest(value=value):
                result = pickle.loads(pickle.dumps(value))
                self.assertEqual(result, value)
                self.assertIsInstance(result, frozenset)

    def test_range_objects(self):
        """Test range object serialization (if available)."""
        try:
            # Python 3.3+
            test_ranges = [
                range(0),
                range(5),
                range(1, 10),
                range(0, 10, 2),
                range(-5, 5),
                range(10, 0, -2),      # negative step
                range(0, 100, 10),     # large step
                range(0, 0, 1),        # empty range
                range(-10, 10, 3),     # negative start with positive step
                range(5, -5, -1),      # positive start with negative step
            ]
            
            for value in test_ranges:
                with self.subTest(value=value):
                    result = pickle.loads(pickle.dumps(value))
                    # Test that the range produces the same sequence
                    self.assertEqual(list(result), list(value))
                    self.assertIsInstance(result, range)
                    # Test individual attributes
                    self.assertEqual(result.start, value.start)
                    self.assertEqual(result.stop, value.stop)
                    self.assertEqual(result.step, value.step)
                    
            # Test range in complex data structures
            complex_data = {
                'ranges': [range(10), range(5, 15), range(0, 100, 7)],
                'mixed': [1, 'hello', range(20, 30, 3), {'nested': range(-5, 5)}]
            }
            result = pickle.loads(pickle.dumps(complex_data))
            # Verify ranges in complex structure
            for i, original_range in enumerate(complex_data['ranges']):
                self.assertEqual(list(result['ranges'][i]), list(original_range))
            self.assertEqual(list(result['mixed'][2]), list(complex_data['mixed'][2]))
            self.assertEqual(list(result['mixed'][3]['nested']), list(complex_data['mixed'][3]['nested']))
            
        except AttributeError:
            self.skipTest("range object pickling not available")

    def test_mixed_nested_structures(self):
        """Test complex nested structures with mixed types."""
        complex_structure = {
            "level1": {
                "list": [1, 2, {"nested": "dict"}],
                "tuple": (1, 2, 3),
                "set": {4, 5, 6},
                "frozenset": frozenset([7, 8, 9]),
                "complex": 1+2j,
            },
            "level2": [
                {"a": [1, 2, 3]},
                (4, 5, 6),
                {7, 8, 9},
                frozenset([10, 11, 12]),
            ],
            "special_values": {
                "none": None,
                "bool_true": True,
                "bool_false": False,
                "empty_string": "",
                "empty_list": [],
                "empty_dict": {},
                "empty_tuple": (),
                "empty_set": set(),
            }
        }
        
        result = pickle.loads(pickle.dumps(complex_structure))
        self.assertEqual(result, complex_structure)

    def test_type_roundtrip(self):
        """Test that types are preserved through pickle cycle."""
        # Test that we get back the exact same type
        test_objects = [
            (type(None), None),
            (bool, True),
            (int, 42),
            (float, 3.14),
            (complex, 1+2j),
            (str, "hello"),
            (bytes, b"hello"),
            (bytearray, bytearray(b"hello")),
            (list, [1, 2, 3]),
            (tuple, (1, 2, 3)),
            (dict, {"a": 1}),
            (set, {1, 2, 3}),
            (frozenset, frozenset([1, 2, 3])),
        ]
        
        for expected_type, value in test_objects:
            with self.subTest(type=expected_type, value=value):
                result = pickle.loads(pickle.dumps(value))
                self.assertIsInstance(result, expected_type)


class TestDataTypeEdgeCases(unittest.TestCase):
    """Test edge cases for data type serialization."""

    def test_empty_vs_none_handling(self):
        """Test that empty containers are handled correctly vs None."""
        test_cases = [
            ([], "empty list"),
            ([None], "list with None"),
            ({}, "empty dict"),
            ({"key": None}, "dict with None value"),
            (set(), "empty set"),
            ({None}, "set with None"),
            ("", "empty string"),
            (None, "None value"),
        ]
        
        for value, description in test_cases:
            with self.subTest(description=description):
                result = pickle.loads(pickle.dumps(value))
                self.assertEqual(result, value)

    def test_large_collections(self):
        """Test serialization of large collections."""
        # Large list
        large_list = list(range(10000))
        result = pickle.loads(pickle.dumps(large_list))
        self.assertEqual(result, large_list)
        
        # Large dict
        large_dict = {i: f"value_{i}" for i in range(1000)}
        result = pickle.loads(pickle.dumps(large_dict))
        self.assertEqual(result, large_dict)
        
        # Large set
        large_set = set(range(5000))
        result = pickle.loads(pickle.dumps(large_set))
        self.assertEqual(result, large_set)

    def test_deeply_nested_structures(self):
        """Test serialization of deeply nested structures."""
        # Create a nested structure with reasonable depth
        nested = {"level": 1}
        current = nested
        for i in range(20):  # 20 levels deep (reasonable for most systems)
            current["next"] = {"level": i + 2}
            current = current["next"]
        
        result = pickle.loads(pickle.dumps(nested))
        
        # Navigate to the deepest level
        current_result = result
        expected_level = 1
        while "next" in current_result:
            self.assertEqual(current_result["level"], expected_level)
            expected_level += 1
            current_result = current_result["next"]
        self.assertEqual(current_result["level"], 21)


if __name__ == '__main__':
    unittest.main()