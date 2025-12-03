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
Test core pickle functionality including dumps, loads, dump, load operations.
"""

import unittest
import tempfile
import os
from io import BytesIO

try:
    import micropython
    import sys
    sys.path.insert(0, 'src')
    from mpickle import mpickle as pickle
    MPICKLE_AVAILABLE = True
except ImportError:
    import pickle
    MPICKLE_AVAILABLE = False


class TestCorePickle(unittest.TestCase):
    """Test core pickle and unpickle functionality."""

    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.test_file = os.path.join(self.temp_dir, 'test.pkl')

    def tearDown(self):
        """Clean up test files."""
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
        os.rmdir(self.temp_dir)

    def test_dumps_loads_simple_types(self):
        """Test basic types can be pickled and unpickled."""
        test_cases = [
            None,
            True,
            False,
            0,
            42,
            -123,
            3.14,
            2.718281828459045,
            1 + 2j,
            "hello",
            "unicode: ñáéíóú",
            b"bytes",
            bytearray(b"bytearray")
        ]
        
        for test_obj in test_cases:
            with self.subTest(obj=test_obj):
                pickled = pickle.dumps(test_obj)
                unpickled = pickle.loads(pickled)
                
                # Handle special cases for equality comparison
                if isinstance(test_obj, (complex, float)):
                    self.assertAlmostEqual(unpickled, test_obj, places=6)
                elif test_obj is None:
                    self.assertIsNone(unpickled)
                else:
                    self.assertEqual(unpickled, test_obj)

    def test_dumps_loads_collections(self):
        """Test collection types can be pickled and unpickled."""
        test_cases = [
            [],  # empty list
            [1, 2, 3],
            ["a", "b", "c"],
            [1, "mixed", True, None],
            (),  # empty tuple
            (1, 2, 3),
            ("a", "b", "c"),
            {},  # empty dict
            {"a": 1, "b": 2},
            {"key": "value", "number": 42},
            set(),  # empty set
            {1, 2, 3},
            {"a", "b", "c"},
            frozenset(),  # empty frozenset
            frozenset([1, 2, 3]),
        ]
        
        for test_obj in test_cases:
            with self.subTest(obj=test_obj):
                pickled = pickle.dumps(test_obj)
                unpickled = pickle.loads(pickled)
                self.assertEqual(unpickled, test_obj)

    def test_dump_load_file_operations(self):
        """Test dump and load with file objects."""
        test_data = {"test": [1, 2, 3], "number": 42, "flag": True}
        
        # Test with file write
        with open(self.test_file, 'wb') as f:
            pickle.dump(test_data, f)
        
        # Test with file read
        with open(self.test_file, 'rb') as f:
            loaded_data = pickle.load(f)
        
        self.assertEqual(loaded_data, test_data)

    def test_dump_load_bytesio(self):
        """Test dump and load with BytesIO objects."""
        test_data = {"key": "value", "list": [1, 2, 3]}
        
        # Test with BytesIO
        buffer = BytesIO()
        pickle.dump(test_data, buffer)
        
        buffer.seek(0)
        loaded_data = pickle.load(buffer)
        
        self.assertEqual(loaded_data, test_data)

    def test_nested_structures(self):
        """Test deeply nested data structures."""
        nested_data = {
            "level1": {
                "level2": {
                    "level3": [1, 2, {"deep": "value"}],
                    "tuple": (1, 2, 3)
                },
                "list": ["a", "b", {"nested": "dict"}]
            }
        }
        
        pickled = pickle.dumps(nested_data)
        unpickled = pickle.loads(pickled)
        self.assertEqual(unpickled, nested_data)

    # NOT SUPPORTED YET
    # Circular references are not yer well supported by Micropython implementation
    # def test_circular_references(self):
    #     """Test handling of circular references."""
    #     lst = [1, 2, 3]
    #     lst.append(lst)  # circular reference
        
    #     pickled = pickle.dumps(lst)
    #     unpickled = pickle.loads(pickled)
        
    #     self.assertEqual(unpickled[0:3], [1, 2, 3])
    #     self.assertIs(unpickled[3], unpickled)  # circular reference preserved

    def test_shared_references(self):
        """Test handling of shared references."""
        obj = {"shared": [1, 2, 3]}
        data = [obj, obj, obj]  # same object referenced multiple times
        
        pickled = pickle.dumps(data)
        unpickled = pickle.loads(pickled)
        
        self.assertEqual(unpickled[0], unpickled[1])
        self.assertEqual(unpickled[1], unpickled[2])
        self.assertIs(unpickled[0], unpickled[1])
        self.assertIs(unpickled[1], unpickled[2])

    def test_protocol_versions(self):
        """Test different pickle protocol versions."""
        test_data = {"data": [1, 2, 3], "number": 42}
        
        for protocol in range(6):  # Protocols 0-5
            with self.subTest(protocol=protocol):
                pickled = pickle.dumps(test_data, protocol=protocol)
                unpickled = pickle.loads(pickled)
                self.assertEqual(unpickled, test_data)

    def test_invalid_pickle_data(self):
        """Test handling of invalid pickle data."""
        invalid_data = [
            b"not a pickle",
            b"",
            b"\x80\x02]q\x00",  # incomplete pickle
            b"\xff\xff\xff\xff",  # invalid header
        ]
        
        for data in invalid_data:
            with self.subTest(data=data):
                with self.assertRaises((pickle.UnpicklingError, pickle.PickleError, EOFError, ValueError)):
                    pickle.loads(data)

    def test_mixed_protocol_compatibility(self):
        """Test compatibility between different protocol versions."""
        # Create pickled data with different protocols
        test_data = {"version": "test", "data": [1, 2, 3]}
        
        pickled_v2 = pickle.dumps(test_data, protocol=2)
        pickled_v4 = pickle.dumps(test_data, protocol=4)
        
        # Load v2 data
        loaded_v2 = pickle.loads(pickled_v2)
        self.assertEqual(loaded_v2, test_data)
        
        # Load v4 data
        loaded_v4 = pickle.loads(pickled_v4)
        self.assertEqual(loaded_v4, test_data)


class TestPickleConstants(unittest.TestCase):
    """Test pickle module constants."""
    
    def test_version_constants(self):
        """Test version-related constants."""
        self.assertIsInstance(pickle.format_version, str)
        self.assertIsInstance(pickle.compatible_formats, list)
        self.assertIsInstance(pickle.HIGHEST_PROTOCOL, int)
        self.assertIsInstance(pickle.DEFAULT_PROTOCOL, int)
        
        # Verify reasonable values
        self.assertGreaterEqual(pickle.HIGHEST_PROTOCOL, 0)
        self.assertGreaterEqual(pickle.DEFAULT_PROTOCOL, 0)
        self.assertGreaterEqual(pickle.DEFAULT_PROTOCOL, 0)
        self.assertLessEqual(pickle.DEFAULT_PROTOCOL, pickle.HIGHEST_PROTOCOL)
        
        # NOT SUPPORTED YET BY MICROPYTHON unittest MODULE
        # # Test format version format
        # self.assertRegex(pickle.format_version, r'\d+\.\d+')


class TestPickleErrors(unittest.TestCase):
    """Test pickle error handling."""
    
    def test_exceptions_defined(self):
        """Test that pickle exceptions are properly defined."""
        self.assertTrue(issubclass(pickle.PickleError, Exception))
        self.assertTrue(issubclass(pickle.PicklingError, pickle.PickleError))
        self.assertTrue(issubclass(pickle.UnpicklingError, pickle.PickleError))
    
    def test_pickling_error_for_unpicklable_objects(self):
        """Test that unpicklable objects raise PicklingError."""
        class UnpicklableClass:
            def __reduce__(self):
                # Return something unpicklable
                return (open, ('file', 'r'))  # open function can't be pickled in all contexts
        
        obj = UnpicklableClass()
        with self.assertRaises(pickle.PicklingError):
            pickle.dumps(obj)


if __name__ == '__main__':
    unittest.main()