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

"""
Integration tests based on the example scenarios from the mpickle library.
"""

import unittest
import sys
import os

# Add src directory to path for imports
src_path = os.path.join(os.path.dirname(__file__), '..', 'src')
if src_path not in sys.path:
    sys.path.insert(0, src_path)

try:
    import micropython
    # Try both import paths
    try:
        import mpickle.mpickle as pickle
        MPICKLE_AVAILABLE = True
    except ImportError:
        import mPickle.mpickle as pickle
        MPICKLE_AVAILABLE = True
except ImportError:
    # Not in micropython, try to import mpickle for Python 3
    try:
        import mPickle.mpickle as pickle
        MPICKLE_AVAILABLE = True
    except ImportError:
        import pickle
        MPICKLE_AVAILABLE = False


class TestBuiltinsDataTypes(unittest.TestCase):
    """Integration test based on builtins-data-types example."""

    def test_all_builtin_types_from_example(self):
        """Test all builtin types from the builtins-data-types example."""
        # This mirrors the test_objects from examples/builtins-data-types/example.py
        test_objects = [
            'foo',                 # String
            12,                    # Integer
            1.2,                   # Float
            1 + 2j,                # Complex number
            True,                  # Boolean
            bytes(1),              # Bytes
            bytearray('foo', 'utf-8'), # Bytearray
            [1, 2, 3],             # List
            (1, 2, 3),             # Tuple
            {1, 2, 'foo', 'bar'},  # Set
            {'foo': 'bar'},        # Dictionary
            None,                  # NoneType
            frozenset(['a', 'b', 'c']), # Immutable Set
            [[1, 2], {'foo': (3, 4)}, {5: [6, 7]}],  # Nested array
            ({'key1': 'value1'}, [1, 2, {3, 4}])  # Nested dict in tuple
        ]
        
        if not MPICKLE_AVAILABLE:
            self.skipTest("Neither mpickle nor standard pickle available")
        
        for i, obj in enumerate(test_objects):
            with self.subTest(index=i, obj=obj):
                # Test individual serialization
                serialized = pickle.dumps(obj)
                deserialized = pickle.loads(serialized)
                
                # Handle special cases for equality comparison
                if isinstance(obj, (complex, float)):
                    self.assertAlmostEqual(deserialized, obj, places=6)
                elif isinstance(obj, set):
                    self.assertEqual(deserialized, obj)
                else:
                    self.assertEqual(deserialized, obj)
                
                # Verify types are preserved
                self.assertIsInstance(deserialized, type(obj))

    def test_nested_collections_integration(self):
        """Test nested collections similar to the example."""
        if not MPICKLE_AVAILABLE:
            self.skipTest("Neither mpickle nor standard pickle available")
        
        # Complex nested structure from the example
        complex_structure = [[1, 2], {'foo': (3, 4)}, {5: [6, 7]}]
        
        serialized = pickle.dumps(complex_structure)
        deserialized = pickle.loads(serialized)
        
        self.assertEqual(deserialized, complex_structure)
        self.assertIsInstance(deserialized, list)
        self.assertEqual(len(deserialized), 3)

    def test_full_collection_integration(self):
        """Test serializing the entire collection at once."""
        if not MPICKLE_AVAILABLE:
            self.skipTest("Neither mpickle nor standard pickle available")
        
        test_objects = [
            'foo', 12, 1.2, 1 + 2j, True, bytes(1),
            bytearray('foo', 'utf-8'), [1, 2, 3], (1, 2, 3),
            {1, 2, 'foo', 'bar'}, {'foo': 'bar'}, None,
            frozenset(['a', 'b', 'c'])
        ]
        
        serialized = pickle.dumps(test_objects)
        deserialized = pickle.loads(serialized)
        
        # Verify all objects are preserved
        self.assertEqual(len(deserialized), len(test_objects))
        
        for original, restored in zip(test_objects, deserialized):
            if isinstance(original, (complex, float)):
                self.assertAlmostEqual(restored, original, places=6)
            elif isinstance(original, set):
                self.assertEqual(restored, original)
            else:
                self.assertEqual(restored, original)


class TestProtocolCompatibility(unittest.TestCase):
    """Test protocol compatibility across different versions."""

    @unittest.skipUnless(MPICKLE_AVAILABLE, "mpickle not available")
    def test_basic_protocols(self):
        """Test that basic protocols work consistently."""
        test_data = {
            "string": "hello world",
            "number": 42,
            "list": [1, 2, 3],
            "nested": {"key": "value"}
        }
        
        # Test protocols 0-4
        for protocol in range(5):
            with self.subTest(protocol=protocol):
                serialized = pickle.dumps(test_data, protocol=protocol)
                deserialized = pickle.loads(serialized)
                self.assertEqual(deserialized, test_data)

    @unittest.skipUnless(MPICKLE_AVAILABLE, "mpickle not available")
    def test_unicode_handling(self):
        """Test unicode string handling."""
        unicode_strings = [
            "hello",
            "unicode: ñáéíóú",
            "chinese: 你好世界",
        ]
        
        for test_str in unicode_strings:
            with self.subTest(string=test_str):
                serialized = pickle.dumps(test_str)
                deserialized = pickle.loads(serialized)
                self.assertEqual(deserialized, test_str)


class TestErrorRecovery(unittest.TestCase):
    """Test error recovery scenarios."""

    @unittest.skipUnless(MPICKLE_AVAILABLE, "mpickle not available")
    def test_invalid_data_handling(self):
        """Test handling of invalid pickle data."""
        # Test with corrupted data
        invalid_data = b"this is not pickle data"
        
        # This should raise an exception
        with self.assertRaises(Exception):
            pickle.loads(invalid_data)
        
        # Test with empty data
        with self.assertRaises(Exception):
            pickle.loads(b"")


if __name__ == '__main__':
    unittest.main()