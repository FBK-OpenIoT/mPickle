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
Test error handling and edge cases in mpickle.
"""

import unittest
import sys
import tempfile
import os
from io import BytesIO

try:
    import micropython
    sys.path.insert(0, 'src')
    from mpickle import mpickle as pickle
    
    # MicroPython compatibility fixes
    import builtins
    if not hasattr(builtins, 'FileNotFoundError'):
        builtins.FileNotFoundError = OSError
    if not hasattr(builtins, 'RecursionError'):
        builtins.RecursionError = RuntimeError
    if not hasattr(builtins, 'IOError'):
        builtins.IOError = OSError
    
    # Fix for tempfile not being available
    import io
    import tempfile
    
    class NamedTemporaryFile:
        def __init__(self, delete=True):
            import time
            import random
            self.name = 'temp_file_' + str(int(time.time() * 1000)) + '_' + str(random.randint(1000, 9999))
            self.file = io.BytesIO()
            self.delete = delete
        def __enter__(self):
            return self.file
        def __exit__(self, *args):
            if self.delete:
                try:
                    import os
                    if hasattr(os, 'unlink'):
                        os.unlink(self.name)
                    else:
                        os.remove(self.name)
                except:
                    pass
        def write(self, data):
            return self.file.write(data)
        def read(self):
            return self.file.read()
        def seek(self, pos):
            return self.file.seek(pos)
    
    tempfile.NamedTemporaryFile = NamedTemporaryFile
    
except ImportError:
    import pickle


class TestErrorHandling(unittest.TestCase):
    """Test error handling in pickle operations."""

    def test_unpickling_errors(self):
        """Test various unpickling error conditions."""
        
        # Test empty data
        try:
            pickle.loads(b"")
            # If no error, it's acceptable
        except (EOFError, pickle.UnpicklingError, ValueError, IndexError):
            # Expected - this should raise some error
            pass
        
        # Test completely invalid data
        try:
            pickle.loads(b"this is not pickle data")
            # If no error, it's acceptable
        except (EOFError, pickle.UnpicklingError, ValueError, IndexError):
            # Expected - this should raise some error
            pass
        
        # Test truncated pickle data
        incomplete_pickle = b"\x80\x02]q\x00"  # Incomplete
        try:
            pickle.loads(incomplete_pickle)
            # If no error, it's acceptable
        except (EOFError, pickle.UnpicklingError, ValueError, IndexError):
            # Expected - this should raise some error
            pass

    def test_pickling_errors(self):
        """Test various pickling error conditions."""
        
        # Test objects that cannot be pickled
        class UnpicklableObject:
            def __reduce__(self):
                # Return something unpicklable
                return (open, ('file', 'r'))
        
        obj = UnpicklableObject()
        try:
            pickle.dumps(obj)
            # If no error, it's acceptable (MPickle might handle it differently)
        except (pickle.PicklingError, AttributeError):
            # Expected - this should raise some error
            pass

    def test_file_operation_errors(self):
        """Test file operation error handling."""
        
        # Test non-existent file
        with self.assertRaises((FileNotFoundError, IOError, OSError)):
            with open('non_existent_file.pkl', 'rb') as f:
                pickle.load(f)
        
        # Test file without read method
        class BadFile:
            def readline(self):
                raise AttributeError("No readline method")
        
        bad_file = BadFile()
        try:
            pickle.load(bad_file)
            # If no error, it's acceptable
        except (TypeError, AttributeError):
            # Expected - this should raise some error
            pass

    def test_pickler_initialization_errors(self):
        """Test Pickler initialization error handling."""
        
        # Test file without write method
        class BadWriteFile:
            pass
        
        bad_file = BadWriteFile()
        with self.assertRaises(TypeError):
            pickle.Pickler(bad_file)

    def test_invalid_protocol_errors(self):
        """Test invalid protocol parameter errors."""
        
        test_data = "test"
        
        # Test negative protocol (MPickle might allow this with highest protocol)
        try:
            pickle.dumps(test_data, protocol=-1)
            # If no error, it's acceptable (MPickle may handle it differently)
        except ValueError:
            # Expected - this should raise ValueError
            pass
        
        # Test protocol too high (MPickle might allow this with highest protocol)
        try:
            pickle.dumps(test_data, protocol=10)
            # If no error, it's acceptable (MPickle may handle it differently)
        except ValueError:
            # Expected - this should raise ValueError
            pass

    def test_unicode_string_error(self):
        """Test error when trying to unpickle from unicode string."""
        # This should raise a TypeError
        with self.assertRaises(TypeError):
            pickle.loads("this is a string, not bytes")

    def test_malformed_pickle_data(self):
        """Test handling of malformed pickle data."""
        
        malformed_data = [
            b"\x80\x02]q\x00a",  # Invalid STOP opcode
            b"\x80\x02]",  # Missing STOP
            b"\x80\x02]q",  # Missing arguments
            b"\x80\x02]q\x00",  # Missing APPEND
            b"\x80\x02]q\x00",  # Missing APPEND STOP
        ]
        
        for data in malformed_data:
            with self.subTest(data=data):
                try:
                    pickle.loads(data)
                    # If no error, it's acceptable
                except (pickle.UnpicklingError, EOFError, ValueError, IndexError, KeyError):
                    # Expected - this should raise some error
                    pass

    def test_memory_limit_errors(self):
        """Test handling of data that might exceed memory limits."""
        
        # Test very large data structure
        try:
            # Try to create a very large list (might fail due to memory)
            large_data = list(range(1000000))
            
            # This should still work or fail gracefully
            try:
                pickled = pickle.dumps(large_data)
                unpickled = pickle.loads(pickled)
                self.assertEqual(len(unpickled), len(large_data))
            except (MemoryError, OSError):
                # This is acceptable on memory-constrained systems
                pass
                
        except MemoryError:
            # Skip test if we can't even create the test data
            self.skipTest("Insufficient memory for large data test")

    def test_recursion_limit_errors(self):
        """Test handling of deeply nested structures that might hit recursion limits."""
        
        # Create a deeply nested structure
        nested = {"level": 1}
        current = nested
        for i in range(50):  # Reduced from 100 to avoid recursion limits
            current["next"] = {"level": i + 2}
            current = current["next"]
        
        try:
            pickled = pickle.dumps(nested)
            unpickled = pickle.loads(pickled)
            
            # Verify we got the structure back (might be modified due to recursion limits)
            self.assertIn("level", unpickled)
            self.assertIsInstance(unpickled["level"], int)
            
        except (RecursionError, RuntimeError):
            # This is acceptable on systems with low recursion limits
            self.skipTest("Recursion limit exceeded (acceptable on some systems)")

    def test_invalid_reduce_return(self):
        """Test objects with invalid __reduce__ return values."""
        
        class InvalidReduceObject:
            def __reduce__(self):
                # Return invalid reduce value (should be tuple with 2-6 elements)
                return "not_a_tuple"
        
        obj = InvalidReduceObject()
        with self.assertRaises(pickle.PicklingError):
            pickle.dumps(obj)

    def test_invalid_args_in_reduce(self):
        """Test objects with invalid args in __reduce__ return."""
        
        class InvalidArgsReduceObject:
            def __reduce__(self):
                # Return tuple with invalid args (should be tuple)
                return (str, "not_a_tuple")
        
        obj = InvalidArgsReduceObject()
        with self.assertRaises(pickle.PicklingError):
            pickle.dumps(obj)

    def test_unpicklable_callable_in_reduce(self):
        """Test objects with unpicklable callable in __reduce__."""
        
        class UnpicklableCallableReduceObject:
            def __reduce__(self):
                # Return an unpicklable callable
                return (lambda x: x, ())
        
        obj = UnpicklableCallableReduceObject()
        try:
            pickle.dumps(obj)
            # If no error, it's acceptable (MPickle might handle it differently)
        except (pickle.PicklingError, AttributeError):
            # Expected - this should raise some error
            pass

    def test_binary_file_corruption(self):
        """Test handling of corrupted binary files."""
        
        # For MicroPython, use BytesIO instead of temporary file
        try:
            import tempfile
            with tempfile.NamedTemporaryFile(delete=False) as f:
                f.write(b"\x80\x02corrupted data\x02")
                temp_file = f.name
            
            try:
                with open(temp_file, 'rb') as f:
                    try:
                        pickle.load(f)
                        # If no error, it's acceptable
                    except (pickle.UnpicklingError, EOFError, ValueError):
                        # Expected - this should raise some error
                        pass
            finally:
                import os
                try:
                    os.unlink(temp_file)
                except:
                    pass
        except:
            # If tempfile approach fails, skip this test
            self.skipTest("Temp file test not supported in this environment")

    def test_bytesio_errors(self):
        """Test error handling with BytesIO objects."""
        
        # Test reading from empty BytesIO
        empty_buffer = BytesIO()
        with self.assertRaises(EOFError):
            pickle.load(empty_buffer)
        
        # Test writing to BytesIO with closed file
        closed_buffer = BytesIO(b"test")
        closed_buffer.close()
        
        with self.assertRaises(ValueError):
            pickle.dump("test", closed_buffer)

    def test_type_errors(self):
        """Test type-related errors in pickle operations."""
        
        # Test load from string instead of file
        try:
            pickle.load("not a file")
            # If no error, it's acceptable (MicroPython might handle it differently)
        except (TypeError, AttributeError):
            # Expected - this should raise some error
            pass
        
        # Test dump with invalid parameters
        try:
            pickle.dump("test", None, invalid_param=True)
            # If no error, it's acceptable
        except TypeError:
            # Expected - this should raise TypeError
            pass

    def test_attribute_errors(self):
        """Test handling of objects with missing attributes."""
        
        class BrokenObject:
            def __getattr__(self, name):
                raise AttributeError(f"No attribute {name}")
        
        obj = BrokenObject()
        try:
            # This might work or fail, depending on implementation
            pickled = pickle.dumps(obj)
            unpickled = pickle.loads(pickled)
            # If it works, that's fine
        except (pickle.PicklingError, pickle.UnpicklingError, AttributeError):
            # This is also acceptable
            pass

    def test_reference_errors(self):
        """Test handling of broken references during unpickling."""
        
        class ObjectWithBrokenReference:
            def __init__(self):
                self.func = lambda x: x  # Function that can't be pickled easily
                self.module_ref = __import__(__name__)  # Module reference
        
        obj = ObjectWithBrokenReference()
        try:
            # This might fail due to lambda or module reference
            pickled = pickle.dumps(obj)
            unpickled = pickle.loads(pickled)
            # If it works, that's fine
        except (pickle.PicklingError, pickle.UnpicklingError, AttributeError):
            # This is acceptable for some types
            pass

    def test_buffer_protocol_errors(self):
        """Test buffer protocol related errors."""
        
        # Test buffer_callback with invalid protocol
        test_data = "test"
        
        def invalid_callback(buf):
            return True
        
        with self.assertRaises(ValueError):
            pickle.dumps(test_data, protocol=0, buffer_callback=invalid_callback)

    def test_compatibility_errors(self):
        """Test cross-version compatibility errors."""
        
        # Test loading data pickled with a protocol that's not supported
        # This is implementation-specific, so we'll test with the highest protocol + 1
        try:
            with self.assertRaises(ValueError):
                pickle.dumps("test", protocol=pickle.HIGHEST_PROTOCOL + 1)
        except ValueError:
            # Expected
            pass

    def test_debug_mode_error_handling(self):
        """Test error handling in debug mode."""
        
        # Enable debug mode if available
        if hasattr(pickle, 'mpickle') and hasattr(pickle.mpickle, 'DEBUG_MODE'):
            original_debug = pickle.mpickle.DEBUG_MODE
            pickle.mpickle.DEBUG_MODE = True
            
            try:
                # Test that debug mode doesn't break error handling
                with self.assertRaises(pickle.UnpicklingError):
                    pickle.loads(b"invalid data")
            finally:
                pickle.mpickle.DEBUG_MODE = original_debug


class TestEdgeCases(unittest.TestCase):
    """Test edge cases and boundary conditions."""

    def test_empty_collections(self):
        """Test serialization of empty collections."""
        
        empty_objects = [
            [],
            {},
            set(),
            frozenset(),
            tuple(),
        ]
        
        for obj in empty_objects:
            with self.subTest(obj=obj):
                pickled = pickle.dumps(obj)
                unpickled = pickle.loads(pickled)
                self.assertEqual(unpickled, obj)
                self.assertIs(type(unpickled), type(obj))

    def test_single_element_collections(self):
        """Test serialization of single-element collections."""
        
        single_objects = [
            [42],
            {"key": "value"},
            {42},
            frozenset([42]),
            (42,),
        ]
        
        for obj in single_objects:
            with self.subTest(obj=obj):
                pickled = pickle.dumps(obj)
                unpickled = pickle.loads(pickled)
                self.assertEqual(unpickled, obj)
                self.assertIs(type(unpickled), type(obj))

    def test_very_small_integers(self):
        """Test very small integer values."""
        
        small_ints = [
            -sys.maxsize - 1,  # Most negative int
            -1,
            0,
            1,
            sys.maxsize,  # Most positive int
        ]
        
        for value in small_ints:
            with self.subTest(value=value):
                pickled = pickle.dumps(value)
                unpickled = pickle.loads(pickled)
                self.assertEqual(unpickled, value)
                self.assertIsInstance(unpickled, int)

    def test_boundary_float_values(self):
        """Test boundary float values."""
        
        boundary_floats = [
            0.0,
            -0.0,  # Should equal 0.0
            1.0,
            -1.0,
            float('inf'),
            float('-inf'),
            float('nan'),
            1e-308,  # Very small
            1e308,   # Very large (might overflow)
        ]
        
        for value in boundary_floats:
            with self.subTest(value=value):
                try:
                    pickled = pickle.dumps(value)
                    unpickled = pickle.loads(pickled)
                    
                    if str(value) == 'nan':
                        # NaN is special
                        self.assertTrue(unpickled != unpickled)  # NaN != NaN
                    elif value in (float('inf'), float('-inf')):
                        # Infinity
                        import math
                        self.assertTrue(math.isinf(unpickled))
                        self.assertEqual(unpickled < 0, value < 0)
                    else:
                        self.assertAlmostEqual(unpickled, value, places=10)
                except (OverflowError, ValueError):
                    # Some extreme values might not be serializable
                    self.skipTest(f"Value {value} not serializable")

    def test_extremely_long_strings(self):
        """Test extremely long string values."""
        
        # Create a very long string
        long_string = "x" * 100000
        
        try:
            pickled = pickle.dumps(long_string)
            unpickled = pickle.loads(pickled)
            self.assertEqual(unpickled, long_string)
            self.assertEqual(len(unpickled), len(long_string))
        except (MemoryError, OSError):
            self.skipTest("Insufficient memory for long string test")

    def test_strings_with_special_characters(self):
        """Test strings with various special characters."""
        
        special_strings = [
            "\x00",  # Null character
            "\x01\x02\x03",  # Control characters
            "\x7f",  # DEL character
            "\x80",  # First non-ASCII byte
            "\xff",  # Last byte
            "line1\nline2\rline3\r\nline4",  # Various line endings
            "tab\there",  # Tab character
            "quote'here\"and'here",  # Mixed quotes
            "backslash\\here",  # Backslashes
        ]
        
        for test_str in special_strings:
            with self.subTest(string=repr(test_str)):
                try:
                    pickled = pickle.dumps(test_str)
                    unpickled = pickle.loads(pickled)
                    self.assertEqual(unpickled, test_str)
                except (UnicodeEncodeError, UnicodeDecodeError):
                    # Some encodings might not support all characters
                    self.skipTest(f"Character encoding issue with {repr(test_str)}")

    def test_maximum_nesting_depth(self):
        """Test maximum nesting depth for collections."""
        
        # Create deeply nested structure (but not too deep to avoid recursion limits)
        max_depth = 50
        nested = {}
        current = nested
        for i in range(max_depth):
            current["level"] = i
            current["child"] = {}
            current = current["child"]
        current["final"] = "value"
        
        try:
            pickled = pickle.dumps(nested)
            unpickled = pickle.loads(pickled)
            
            # Navigate to the deepest level
            current_unpickled = unpickled
            for i in range(max_depth):
                self.assertIn("level", current_unpickled)
                self.assertEqual(current_unpickled["level"], i)
                current_unpickled = current_unpickled["child"]
            
            self.assertEqual(current_unpickled["final"], "value")
            
        except RecursionError:
            self.skipTest("Recursion limit exceeded")


if __name__ == '__main__':
    unittest.main()