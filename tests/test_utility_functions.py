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
Test mpickle utility functions and codecs - comprehensive test coverage.
"""

import unittest
import sys

# Add src directory to path for imports
src_path = 'src'
if src_path not in sys.path:
    sys.path.insert(0, src_path)

# Initialize all imports to None as fallback
pickle = None
codecs = None
uBytesIO = None
encode_long = None
decode_long = None
whichmodule = None
_getattribute = None
_handle_none_module_name = None
registered_pickle_dict_list = None
find_dict_by_key_value = None
register_pickle = None
inject_dummy_module_func = None
revert_dummy_module_func = None
MPICKLE_AVAILABLE = False

try:
    import micropython
    sys.path.insert(0, 'src')
    
    # Try to import mpickle modules with graceful fallback
    try:
        from mpickle import mpickle as pickle
        try:
            from mpickle.mpickle import (
                codecs,
                uBytesIO,
                encode_long,
                decode_long,
                whichmodule,
                _getattribute,
                _handle_none_module_name,
                registered_pickle_dict_list,
                find_dict_by_key_value,
                register_pickle,
                inject_dummy_module_func,
                revert_dummy_module_func
            )
            MPICKLE_AVAILABLE = True
        except ImportError:
            # Some modules may not be available - try basic imports
            try:
                from mpickle.mpickle import (
                    encode_long,
                    decode_long,
                    registered_pickle_dict_list,
                    find_dict_by_key_value,
                    _getattribute,
                    _handle_none_module_name
                )
                MPICKLE_AVAILABLE = True
            except ImportError:
                pass
    except ImportError:
        pass
    
    # MicroPython compatibility fixes
    import builtins
    if not hasattr(builtins, 'FileNotFoundError'):
        builtins.FileNotFoundError = OSError
    if not hasattr(builtins, 'RecursionError'):
        builtins.RecursionError = RuntimeError
    if not hasattr(builtins, 'IOError'):
        builtins.IOError = OSError
        
    # Add assertRegex for MicroPython if missing
    if not hasattr(unittest.TestCase, 'assertRegex'):
        def assertRegex(self, text, pattern, msg=None):
            import re
            if not re.search(pattern, text):
                msg = msg or "Regex %s not found in %s" % (pattern, text)
                self.fail(msg)
        unittest.TestCase.assertRegex = assertRegex
    
    # Add assertIsInstance for MicroPython if missing
    if not hasattr(unittest.TestCase, 'assertIsInstance'):
        def assertIsInstance(self, obj, cls, msg=None):
            if not isinstance(obj, cls):
                msg = msg or "%s is not an instance of %s" % (obj, cls)
                self.fail(msg)
        unittest.TestCase.assertIsInstance = assertIsInstance
        
    # Add assertIsNotNone for MicroPython if missing  
    if not hasattr(unittest.TestCase, 'assertIsNotNone'):
        def assertIsNotNone(self, obj, msg=None):
            if obj is None:
                msg = msg or "Expected object not to be None"
                self.fail(msg)
        unittest.TestCase.assertIsNotNone = assertIsNotNone
        
    # Add assertIn for MicroPython if missing
    if not hasattr(unittest.TestCase, 'assertIn'):
        def assertIn(self, member, container, msg=None):
            if member not in container:
                msg = msg or "%s not found in %s" % (member, container)
                self.fail(msg)
        unittest.TestCase.assertIn = assertIn
        
    # Add assertGreaterEqual for MicroPython if missing
    if not hasattr(unittest.TestCase, 'assertGreaterEqual'):
        def assertGreaterEqual(self, first, second, msg=None):
            if not (first >= second):
                msg = msg or "%s not >= %s" % (first, second)
                self.fail(msg)
        unittest.TestCase.assertGreaterEqual = assertGreaterEqual
        
    # Add assertLessEqual for MicroPython if missing
    if not hasattr(unittest.TestCase, 'assertLessEqual'):
        def assertLessEqual(self, first, second, msg=None):
            if not (first <= second):
                msg = msg or "%s not <= %s" % (first, second)
                self.fail(msg)
        unittest.TestCase.assertLessEqual = assertLessEqual
        
    # Add assertGreater for MicroPython if missing
    if not hasattr(unittest.TestCase, 'assertGreater'):
        def assertGreater(self, first, second, msg=None):
            if not (first > second):
                msg = msg or "%s not > %s" % (first, second)
                self.fail(msg)
        unittest.TestCase.assertGreater = assertGreater
    
except ImportError:
    # Not in MicroPython, try Python 3 mpickle
    try:
        import mPickle.mpickle as pickle
        from mPickle.mpickle import (
            encode_long,
            decode_long,
            whichmodule,
            _getattribute,
            _handle_none_module_name,
            registered_pickle_dict_list,
            find_dict_by_key_value,
            register_pickle,
            inject_dummy_module_func,
            revert_dummy_module_func,
            codecs,
            uBytesIO
        )
        MPICKLE_AVAILABLE = True
    except ImportError:
        pass


class TestFindDictByKeyValue(unittest.TestCase):
    """Test the find_dict_by_key_value helper function."""

    def test_find_dict_by_key_value_basic(self):
        """Test basic key-value search functionality."""
        test_dicts = [
            {"key1": "value1", "type": "dict1"},
            {"key2": "value2", "type": "dict2"},
            {"key3": "value3", "type": "dict3"},
        ]
        
        # Test existing key-value pair
        result = find_dict_by_key_value(test_dicts, "type", "dict2")
        self.assertEqual(result, test_dicts[1])
        
        # Test non-existing key-value pair
        result = find_dict_by_key_value(test_dicts, "type", "dict4")
        self.assertIsNone(result)
        
        # Test existing key with wrong value
        result = find_dict_by_key_value(test_dicts, "key1", "wrong_value")
        self.assertIsNone(result)

    def test_find_dict_by_key_value_empty_list(self):
        """Test with empty list."""
        result = find_dict_by_key_value([], "key", "value")
        self.assertIsNone(result)

    def test_find_dict_by_key_value_none_values(self):
        """Test with None values."""
        test_dicts = [
            {"key1": None, "type": "dict1"},
            {"key2": "value2", "type": None},
        ]
        
        # Test None value
        result = find_dict_by_key_value(test_dicts, "key1", None)
        self.assertEqual(result, test_dicts[0])
        
        result = find_dict_by_key_value(test_dicts, "type", None)
        self.assertEqual(result, test_dicts[1])


@unittest.skipUnless(MPICKLE_AVAILABLE and codecs, "codecs module not available")
class TestCodecs(unittest.TestCase):
    """Test codec functions."""

    def test_encode_ascii(self):
        """Test ASCII encoding."""
        test_cases = [
            ("hello", b"hello"),
            ("ASCII", b"ASCII"),
            ("123", b"123"),
            ("!@#$%", b"!@#$%"),
        ]
        
        for input_str, expected in test_cases:
            with self.subTest(input=input_str):
                result = codecs.encode(input_str, 'ascii')
                self.assertEqual(result, expected)

    def test_encode_latin1(self):
        """Test Latin-1 encoding."""
        test_cases = [
            ("hello", b"hello"),
            ("café", b"caf\xe9"),  # é is 0xE9 in Latin-1
            ("\x00\x01\x7f", b"\x00\x01\x7f"),
        ]
        
        for input_str, expected in test_cases:
            with self.subTest(input=repr(input_str)):
                result = codecs.encode(input_str, 'latin1')
                self.assertEqual(result, expected)

    def test_encode_utf8(self):
        """Test UTF-8 encoding."""
        test_cases = [
            ("hello", b"hello"),
            ("café", "café".encode('utf-8')),
            ("世界", "世界".encode('utf-8')),
            ("\x00\x01", b"\x00\x01"),
        ]
        
        for input_str, expected in test_cases:
            with self.subTest(input=repr(input_str)):
                result = codecs.encode(input_str, 'utf-8')
                self.assertEqual(result, expected)

    def test_encode_invalid_encoding(self):
        """Test encoding with invalid encoding name."""
        with self.assertRaises(ValueError):
            codecs.encode("test", "invalid_encoding")

    def test_escape_decode_basic(self):
        """Test basic escape sequence decoding."""
        test_cases = [
            (b"hello", (b"hello", 5)),
            (b"\\n", (b"\n", 1)),
            (b"\\t", (b"\t", 1)),
            (b"\\r", (b"\r", 1)),
            (b"\\\\", (b"\\", 1)),
            (b"\\'", (b"'", 1)),
            (b'\\"', (b'"', 1)),
            (b"\\b", (b"\b", 1)),
            (b"\\f", (b"\f", 1)),
            (b"\\v", (b"\v", 1)),
            (b"\\a", (b"\a", 1)),
            (b"\\0", (b"\0", 1)),
        ]
        
        for input_bytes, expected in test_cases:
            with self.subTest(input=repr(input_bytes)):
                result = codecs.escape_decode(input_bytes)
                self.assertEqual(result, expected)

    def test_escape_decode_no_escapes(self):
        """Test escape decode with no escape sequences."""
        test_cases = [
            b"hello world",
            b"no escapes here!",
            b"\x00\x01\x02\x03",
        ]
        
        for input_bytes in test_cases:
            with self.subTest(input=repr(input_bytes)):
                result = codecs.escape_decode(input_bytes)
                self.assertEqual(result, (input_bytes, len(input_bytes)))

    def test_escape_decode_mixed(self):
        """Test escape decode with mixed content."""
        mixed_cases = [
            (b"hello\\nworld", (b"hello\nworld", 11)),
            (b"tab\\there", (b"tab\there", 8)),
            (b"quote\\'test\\'", (b"quote'test'", 11)),
        ]
        
        for input_bytes, expected in mixed_cases:
            with self.subTest(input=repr(input_bytes)):
                result = codecs.escape_decode(input_bytes)
                self.assertEqual(result, expected)

    def test_escape_decode_unknown_escape(self):
        """Test escape decode with unknown escape sequences."""
        # Unknown escapes should be treated as literal backslash + character
        test_cases = [
            (b"\\x", (b"\\x", 2)),
            (b"\\q", (b"\\q", 2)),
            (b"test\\z", (b"test\\z", 6)),
        ]
        
        for input_bytes, expected in test_cases:
            with self.subTest(input=repr(input_bytes)):
                result = codecs.escape_decode(input_bytes)
                self.assertEqual(result, expected)


@unittest.skipUnless(MPICKLE_AVAILABLE and uBytesIO, "uBytesIO not available")
class TestUBytesIO(unittest.TestCase):
    """Test uBytesIO class functionality."""

    def test_ubytesio_basic_operations(self):
        """Test basic uBytesIO operations."""
        buffer = uBytesIO()
        
        # Test initial state
        self.assertEqual(buffer.tell(), 0)
        self.assertEqual(buffer.getvalue(), b"")
        
        # Test write
        buffer.write(b"hello")
        self.assertEqual(buffer.tell(), 5)
        self.assertEqual(buffer.getvalue(), b"hello")
        
        # Test seek
        buffer.seek(0)
        self.assertEqual(buffer.tell(), 0)
        
        buffer.seek(2)
        self.assertEqual(buffer.tell(), 2)
        
        # Test read
        data = buffer.read()
        self.assertEqual(data, b"hello")

    def test_ubytesio_getbuffer(self):
        """Test uBytesIO getbuffer method."""
        buffer = uBytesIO()
        buffer.write(b"test data")
        
        # getbuffer should return a memoryview
        buf_view = buffer.getbuffer()
        self.assertIsInstance(buf_view, memoryview)
        
        # The content should match
        self.assertEqual(bytes(buf_view), b"test data")

    def test_ubytesio_inheritance(self):
        """Test that uBytesIO properly inherits from BytesIO."""
        buffer = uBytesIO()
        
        # Should have all BytesIO methods
        self.assertTrue(hasattr(buffer, 'read'))
        self.assertTrue(hasattr(buffer, 'write'))
        self.assertTrue(hasattr(buffer, 'seek'))
        self.assertTrue(hasattr(buffer, 'tell'))
        self.assertTrue(hasattr(buffer, 'getvalue'))

    def test_ubytesio_empty_buffer(self):
        """Test uBytesIO with empty buffer."""
        buffer = uBytesIO()
        
        # getbuffer on empty buffer
        buf_view = buffer.getbuffer()
        self.assertEqual(len(buf_view), 0)
        self.assertEqual(bytes(buf_view), b"")


@unittest.skipUnless(MPICKLE_AVAILABLE and encode_long and decode_long, "encode_long/decode_long not available")
class TestEncodeDecodeLong(unittest.TestCase):
    """Test encode_long and decode_long functions."""

    def test_encode_long_zero(self):
        """Test encoding zero."""
        self.assertEqual(encode_long(0), b'')

    def test_encode_long_positive(self):
        """Test encoding positive integers."""
        test_cases = [
            (1, b'\x01'),
            (-1, b'\xff'),  # Two's complement
            (127, b'\x7f'),
            (255, b'\xff\x00'),
            (32767, b'\xff\x7f'),
            (128, b'\x80\x00'),
        ]
        
        for value, expected in test_cases:
            with self.subTest(value=value):
                result = encode_long(value)
                self.assertEqual(result, expected)

    def test_encode_long_negative(self):
        """Test encoding negative integers."""
        test_cases = [
            (-1, b'\xff'),
            (-128, b'\x80'),
            (-256, b'\x00\xff'),
            (-32768, b'\x00\x80'),
        ]
        
        for value, expected in test_cases:
            with self.subTest(value=value):
                result = encode_long(value)
                self.assertEqual(result, expected)

    def test_decode_long_zero(self):
        """Test decoding zero."""
        self.assertEqual(decode_long(b''), 0)

    def test_decode_long_positive(self):
        """Test decoding positive integers."""
        test_cases = [
            (b'\x01', 1),
            (b'\x7f', 127),
            (b'\xff\x00', 255),
            (b'\xff\x7f', 32767),
            (b'\x80\x00', 128),
        ]
        
        for encoded, expected in test_cases:
            with self.subTest(encoded=encoded):
                result = decode_long(encoded)
                self.assertEqual(result, expected)

    def test_decode_long_negative(self):
        """Test decoding negative integers."""
        test_cases = [
            (b'\xff', -1),
            (b'\x80', -128),
            (b'\x00\xff', -256),
            (b'\x00\x80', -32768),
        ]
        
        for encoded, expected in test_cases:
            with self.subTest(encoded=encoded):
                result = decode_long(encoded)
                self.assertEqual(result, expected)

    def test_roundtrip_long(self):
        """Test that encode_long/decode_long are inverses."""
        test_values = [
            0, 1, -1, 127, -128, 255, -256, 32767, -32768,
            1234567890, -1234567890,
        ]
        
        for value in test_values:
            with self.subTest(value=value):
                encoded = encode_long(value)
                decoded = decode_long(encoded)
                self.assertEqual(decoded, value)

    def test_large_long_values(self):
        """Test very large long values."""
        large_positive = 2**64 - 1
        large_negative = -(2**63)
        
        try:
            # Test positive large value
            encoded = encode_long(large_positive)
            decoded = decode_long(encoded)
            self.assertEqual(decoded, large_positive)
            
            # Test negative large value
            encoded = encode_long(large_negative)
            decoded = decode_long(encoded)
            self.assertEqual(decoded, large_negative)
            
        except (OverflowError, ValueError):
            # Some systems might not handle such large values
            self.skipTest("System cannot handle large long values")


@unittest.skipUnless(MPICKLE_AVAILABLE and _getattribute, "_getattribute not available")
class TestGetAttribute(unittest.TestCase):
    """Test _getattribute utility function."""

    def test_getattribute_single_level(self):
        """Test _getattribute with single level."""
        class TestClass:
            attr = "value"
        
        obj = TestClass()
        result = _getattribute(obj, ["attr"])
        self.assertEqual(result, "value")

    def test_getattribute_nested(self):
        """Test _getattribute with nested attributes."""
        class Inner:
            inner_attr = "inner_value"
        
        class Middle:
            middle_attr = "middle_value"
            inner = Inner()
        
        class Outer:
            outer_attr = "outer_value"
            middle = Middle()
        
        obj = Outer()
        
        # Test nested attribute access
        result = _getattribute(obj, ["middle", "inner", "inner_attr"])
        self.assertEqual(result, "inner_value")

    def test_getattribute_nonexistent(self):
        """Test _getattribute with nonexistent attribute."""
        class TestClass:
            attr = "value"
        
        obj = TestClass()
        
        with self.assertRaises(AttributeError):
            _getattribute(obj, ["nonexistent"])

    def test_getattribute_empty_path(self):
        """Test _getattribute with empty path."""
        class TestClass:
            attr = "value"
        
        obj = TestClass()
        
        # Empty path should raise an error or return obj
        try:
            result = _getattribute(obj, [])
            # If no error is raised, result should be the object itself
            self.assertEqual(result, obj)
        except (AttributeError, IndexError):
            # Expected behavior: error is raised
            pass


@unittest.skipUnless(MPICKLE_AVAILABLE and _handle_none_module_name, "_handle_none_module_name not available")
class TestHandleNoneModuleName(unittest.TestCase):
    """Test _handle_none_module_name utility function."""

    def test_handle_none_module_name_complex(self):
        """Test handling of complex type."""
        result = _handle_none_module_name(None, complex)
        self.assertEqual(result, 'builtins')

    def test_handle_none_module_name_bytearray(self):
        """Test handling of bytearray type."""
        result = _handle_none_module_name(None, bytearray)
        self.assertEqual(result, 'builtins')

    def test_handle_none_module_name_object(self):
        """Test handling of object type."""
        result = _handle_none_module_name(None, object)
        self.assertEqual(result, 'builtins')

    def test_handle_none_module_name_function(self):
        """Test handling of function type."""
        def test_func():
            pass
        
        result = _handle_none_module_name(None, test_func)
        # Should be the module name - check it's a string or None
        self.assertTrue(result is None or isinstance(result, str))

    def test_handle_none_module_name_existing_module(self):
        """Test that existing module names are preserved."""
        module_name = "test_module"
        obj = lambda: None  # Some object
        
        result = _handle_none_module_name(module_name, obj)
        self.assertEqual(result, module_name)


@unittest.skipUnless(MPICKLE_AVAILABLE and whichmodule, "whichmodule not available")
class TestWhichModule(unittest.TestCase):
    """Test whichmodule function."""

    def test_whichmodule_builtin(self):
        """Test whichmodule for built-in functions."""
        result = whichmodule(len, "len")
        self.assertEqual(result, "builtins")

    def test_whichmodule_os_module(self):
        """Test whichmodule for os module functions."""
        result = whichmodule(__import__('os').path.join, "join")
        self.assertEqual(result, "os.path")

    def test_whichmodule_string_type(self):
        """Test whichmodule for string type."""
        result = whichmodule(str, "str")
        self.assertEqual(result, "builtins")

    def test_whichmodule_int_type(self):
        """Test whichmodule for int type."""
        result = whichmodule(int, "int")
        self.assertEqual(result, "builtins")


@unittest.skipUnless(MPICKLE_AVAILABLE and pickle, "pickle module not available")
class TestPickleConstants(unittest.TestCase):
    """Test pickle module constants."""

    def test_format_version_format(self):
        """Test that format_version has correct format."""
        self.assertRegex(pickle.format_version, r'\d+\.\d+')

    def test_compatible_formats_type(self):
        """Test that compatible_formats is a list of strings."""
        self.assertIsInstance(pickle.compatible_formats, list)
        for fmt in pickle.compatible_formats:
            self.assertIsInstance(fmt, str)
            self.assertRegex(fmt, r'\d+\.\d+')

    def test_protocol_constants(self):
        """Test protocol-related constants."""
        self.assertIsInstance(pickle.HIGHEST_PROTOCOL, int)
        self.assertIsInstance(pickle.DEFAULT_PROTOCOL, int)
        self.assertGreaterEqual(pickle.HIGHEST_PROTOCOL, 0)
        self.assertGreaterEqual(pickle.DEFAULT_PROTOCOL, 0)
        self.assertLessEqual(pickle.DEFAULT_PROTOCOL, pickle.HIGHEST_PROTOCOL)

    def test_opcode_constants(self):
        """Test that pickle opcodes are defined."""
        opcodes = [
            'MARK', 'STOP', 'POP', 'POP_MARK', 'DUP',
            'FLOAT', 'INT', 'BININT', 'BININT1', 'LONG',
            'NONE', 'PERSID', 'BINPERSID', 'REDUCE',
            'STRING', 'BINSTRING', 'UNICODE', 'APPEND',
            'BUILD', 'GLOBAL', 'DICT', 'EMPTY_DICT',
            'LIST', 'EMPTY_LIST', 'TUPLE', 'EMPTY_TUPLE',
        ]
        
        for opcode in opcodes:
            self.assertTrue(hasattr(pickle, opcode), f"Missing opcode: {opcode}")


@unittest.skipUnless(MPICKLE_AVAILABLE and pickle, "pickle module not available")
class TestFramerUnframer(unittest.TestCase):
    """Test _Framer and _Unframer classes."""

    def test_framer_basic_functionality(self):
        """Test basic _Framer functionality."""
        import io
        
        output = io.BytesIO()
        framer = pickle._Framer(output.write)
        
        # Test writing data
        framer.write(b"test data")
        
        # Test framing
        framer.start_framing()
        framer.write(b"framed data")
        framer.end_framing()
        
        # Should have produced some output
        result = output.getvalue()
        self.assertIsInstance(result, bytes)
        self.assertGreater(len(result), 0)

    def test_unframer_basic_functionality(self):
        """Test basic _Unframer functionality."""
        import io
        
        input_data = b"test input data"
        input_stream = io.BytesIO(input_data)
        
        unframer = pickle._Unframer(
            input_stream.read,
            input_stream.readline
        )
        
        # Test reading data
        read_data = unframer.read(4)
        self.assertEqual(read_data, b"test")
        
        # Test reading line (should read to end since no newlines)
        line = unframer.readline()
        self.assertEqual(line, b" input data")


if __name__ == '__main__':
    unittest.main()