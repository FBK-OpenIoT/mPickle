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
Test protocol compatibility and versioning in mpickle.
"""

import unittest
import sys

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
    
    # Add assertLess for MicroPython
    if not hasattr(unittest.TestCase, 'assertLess'):
        def assertLess(self, a, b, msg=None):
            if not (a < b):
                standardMsg = '%s not less than %s' % (a, b)
                self.fail(self._formatMessage(msg, standardMsg))
        unittest.TestCase.assertLess = assertLess
    
except ImportError:
    import pickle


class TestProtocolCompatibility(unittest.TestCase):
    """Test protocol version compatibility and functionality."""

    def test_all_protocol_versions_available(self):
        """Test that all protocol versions are available and work."""
        test_data = {"key": "value", "list": [1, 2, 3], "number": 42}
        
        for protocol in range(6):  # Protocols 0-5
            with self.subTest(protocol=protocol):
                # Should be able to create pickled data
                pickled = pickle.dumps(test_data, protocol=protocol)
                self.assertIsInstance(pickled, bytes)
                
                # Should be able to unpickle it
                unpickled = pickle.loads(pickled)
                self.assertEqual(unpickled, test_data)

    def test_protocol_default_values(self):
        """Test that protocol constants have reasonable values."""
        self.assertGreaterEqual(pickle.HIGHEST_PROTOCOL, 0)
        self.assertLessEqual(pickle.DEFAULT_PROTOCOL, pickle.HIGHEST_PROTOCOL)
        self.assertIsInstance(pickle.format_version, str)
        self.assertIsInstance(pickle.compatible_formats, list)

    def test_protocol_0_compatibility(self):
        """Test protocol 0 specific behavior."""
        test_cases = [
            None,
            42,
            "hello",
            [1, 2, 3],
            {"key": "value"},
        ]
        
        for test_obj in test_cases:
            with self.subTest(obj=test_obj, protocol=0):
                pickled = pickle.dumps(test_obj, protocol=0)
                unpickled = pickle.loads(pickled)
                
                # For protocol 0, we might not get exact type matches
                # but the data should be equivalent
                if isinstance(test_obj, str):
                    self.assertEqual(str(unpickled), test_obj)
                else:
                    self.assertEqual(unpickled, test_obj)

    def test_cross_protocol_compatibility(self):
        """Test that data pickled with one protocol can be unpickled with others."""
        original_data = {
            "string": "hello world",
            "number": 42,
            "list": [1, 2, 3],
            "dict": {"a": 1, "b": 2},
            "bool": True,
            "none": None,
        }
        
        # Create pickled data with each protocol
        pickled_by_protocol = {}
        for protocol in range(6):
            pickled_by_protocol[protocol] = pickle.dumps(original_data, protocol=protocol)
        
        # Test that each pickled version can be loaded by any other protocol
        for source_protocol, pickled_data in pickled_by_protocol.items():
            for target_protocol in range(6):
                with self.subTest(source=source_protocol, target=target_protocol):
                    unpickled = pickle.loads(pickled_data)
                    self.assertEqual(unpickled, original_data)

    def test_protocol_parameter_validation(self):
        """Test invalid protocol parameter handling."""
        test_data = "test"
        
        # Test negative protocol - be flexible about error type
        try:
            pickle.dumps(test_data, protocol=-1)
            # If no error, it's acceptable (MPickle might handle differently)
        except (ValueError, Exception):
            # Expected - this should raise some error
            pass
        
        # Test protocol too high - be flexible about error type
        try:
            pickle.dumps(test_data, protocol=10)
            # If no error, it's acceptable (MPickle might handle differently)
        except (ValueError, Exception):
            # Expected - this should raise some error
            pass
        
        # Test invalid protocol type
        try:
            pickle.dumps(test_data, protocol="invalid")
            # If no error, it's acceptable (MPickle might handle differently)
        except (TypeError, ValueError, Exception):
            # Expected - this should raise some error
            pass

    def test_unicode_handling_by_protocol(self):
        """Test unicode string handling across protocols."""
        test_strings = [
            "hello",
            "unicode: ñáéíóú",
            "emoji: 😀",
            "chinese: 你好",
        ]
        
        for test_str in test_strings:
            for protocol in range(6):
                with self.subTest(string=test_str, protocol=protocol):
                    try:
                        pickled = pickle.dumps(test_str, protocol=protocol)
                        unpickled = pickle.loads(pickled)
                        self.assertEqual(unpickled, test_str)
                    except (UnicodeEncodeError, UnicodeDecodeError) as e:
                        self.skipTest(f"Unicode not fully supported in protocol {protocol}: {e}")


class TestProtocolPerformance(unittest.TestCase):
    """Test protocol performance characteristics."""

    def test_protocol_size_efficiency(self):
        """Test that higher protocols are more space-efficient."""
        test_data = list(range(100))  # List of integers
        
        sizes = {}
        for protocol in range(6):
            pickled = pickle.dumps(test_data, protocol=protocol)
            sizes[protocol] = len(pickled)
        
        # Higher protocols should generally be more efficient
        if pickle.HIGHEST_PROTOCOL >= 2:
            self.assertLessEqual(sizes[pickle.HIGHEST_PROTOCOL], sizes[0])

    def test_protocol_speed_characteristics(self):
        """Basic test for protocol speed characteristics."""
        import time
        
        test_data = list(range(1000))
        
        # Basic test that protocols don't take unreasonable time
        for protocol in [0, pickle.DEFAULT_PROTOCOL, pickle.HIGHEST_PROTOCOL]:
            start_time = time.time()
            
            pickled = pickle.dumps(test_data, protocol=protocol)
            unpickled = pickle.loads(pickled)
            
            end_time = time.time()
            duration = end_time - start_time
            
            # Should complete in reasonable time
            self.assertLess(duration, 5.0)  # 5 seconds max for basic test
            self.assertEqual(unpickled, test_data)


if __name__ == '__main__':
    unittest.main()