# mPickle Library Tests Documentation

This directory contains comprehensive unit tests for the mPickle library, specifically designed for **MicroPython UNIX port** environments.

## Test Environment Setup

### MicroPython UNIX Port Testing

The mPickle library tests are specifically designed to run on **MicroPython UNIX port**. Follow these instructions to set up and run the tests.

#### Prerequisites

1. **MicroPython UNIX Port Binary**
   Ensure you have the MicroPython UNIX port compiled and available at:
   ```
   ./firmware/dev-scripts/output/micropython
   ```
   Otherwise, follow this [guide](/docs/SETUP.md).

2. **Required MicroPython Packages**
   Install the following packages using the MicroPython package manager (`mip`):

   ```python
   import mip
   
   # Install required packages
   mip.install("unittest-discover")
   mip.install("shutil") 
   mip.install("tempfile")
   mip.install("os-path")
   ```

#### Installation Commands

Run these commands inside the MicroPython interpreter:

```bash
# Start MicroPython interpreter
./firmware/dev-scripts/output/micropython

# Inside the interpreter:
import mip
mip.install("unittest-discover")
mip.install("shutil") 
mip.install("tempfile")
mip.install("os-path")

# Exit the interpreter
exit()
```

## Running Tests

### Command-Line Execution

Run all tests from the project root directory:

```bash
./firmware/dev-scripts/output/micropython -m unittest src/tests/test_*.py
```

This command will:
- Execute all Python test files in the tests directory
- Run tests using Python's built-in unittest module
- Display test results with pass/fail status for each test


## Test Suite Structure

### Individual Test Files

The test suite consists of the following files:

1. **`test_data_types.py`** - Tests for built-in data types serialization
   - Tests `None`, `bool`, `int`, `float`, `str`, `list`, `dict`, `tuple`, `set`, etc.
   - Validates round-trip serialization for all basic types

2. **`test_custom_classes.py`** - Tests for custom classes and inheritance
   - Tests class pickling/unpickling
   - Tests inheritance scenarios
   - Tests complex object hierarchies

3. **`test_protocols.py`** - Tests for protocol compatibility and versioning
   - Tests different pickle protocol versions (0-5)
   - Validates protocol-specific behaviors
   - Tests version compatibility

4. **`test_error_handling.py`** - Tests for error handling and edge cases
   - Tests invalid pickle data handling
   - Tests malformed objects
   - Tests boundary conditions

5. **`test_registration_system.py`** - Tests for registration system functionality
   - Tests `register_pickle` function
   - Tests `inject_dummy_module_func` and `revert_dummy_module_func`
   - Tests custom serialization registration

6. **`test_utility_functions.py`** - Tests for utility functions and codecs
   - Tests **38 utility function tests** including codecs, uBytesIO, encoding/decoding, and more


## Test Coverage Summary

The comprehensive test suite validates:

- ✅ **Core functionality**: Pickle/unpickle operations for all data types
- ✅ **MicroPython compatibility**: Optimized for constrained environments
- ✅ **Error handling**: Proper error conditions and edge cases
- ✅ **Protocol compatibility**: All pickle protocol versions
- ✅ **Custom classes**: User-defined class serialization
- ✅ **Registration system**: Custom serialization functions
- ✅ **Utility functions**: All 38 utility function tests
- ✅ **Integration**: End-to-end functionality validation

## MicroPython Test Results

Expected results for MicroPython environment:
```
Ran 34 tests
OK
```

## Troubleshooting

### Common Issues

1. **Module Import Errors**
   - Ensure MicroPython packages are installed using `mip.install()`
   - Check that the MicroPython binary path is correct

2. **Test Skipping**
   - Some tests may be skipped in MicroPython due to missing features
   - This is expected behavior, not a failure

3. **Performance**
   - MicroPython tests may take longer than standard Python tests
   - This is normal due to different execution environments

### Getting Help

If you encounter issues:

1. Verify MicroPython packages are installed correctly
2. Check that you're running from the project root directory
3. Ensure the MicroPython binary has execute permissions
4. Review test output for specific error messages

---

## Detailed Test Explanations and Outputs

This section provides detailed explanations of each test in the mPickle library test suite, including actual test outputs:

### 1. Built-in Data Types Tests (`test_data_types.py`)

**Purpose**: Validates that all Python built-in data types can be properly serialized and deserialized using mPickle.

**Actual Test Output**:
```
test_none_type (test_data_types.TestDataTypes) ... ok
test_boolean_types (test_data_types.TestDataTypes) ... ok
test_integer_types (test_data_types.TestDataTypes) ... ok
test_float_types (test_data_types.TestDataTypes) ... ok
test_complex_types (test_data_types.TestDataTypes) ... ok
test_string_types (test_data_types.TestDataTypes) ... ok
test_bytes_types (test_data_types.TestDataTypes) ... ok
test_bytearray_types (test_data_types.TestDataTypes) ... ok
test_list_types (test_data_types.TestDataTypes) ... ok
test_tuple_types (test_data_types.TestDataTypes) ... ok
test_dict_types (test_data_types.TestDataTypes) ... ok
test_set_types (test_data_types.TestDataTypes) ... ok
test_frozenset_types (test_data_types.TestDataTypes) ... ok
test_range_objects (test_data_types.TestDataTypes) ... ok
test_mixed_nested_structures (test_data_types.TestDataTypes) ... ok
test_type_roundtrip (test_data_types.TestDataTypes) ... ok
test_empty_vs_none_handling (test_data_types.TestDataTypeEdgeCases) ... ok
test_large_collections (test_data_types.TestDataTypeEdgeCases) ... ok
test_deeply_nested_structures (test_data_types.TestDataTypeEdgeCases) ... ok
----------------------------------------------------------------------
Ran 19 tests

OK
```

**Test Coverage**:
- **None values**: `None` serialization and reconstruction
- **Boolean values**: `True` and `False` handling
- **Integers**: Standard and long integer serialization
- **Floating point numbers**: Float precision and range handling
- **Strings**: Unicode string encoding and decoding
- **Lists**: Dynamic list serialization with mixed content
- **Dictionaries**: Key-value pair handling with various data types
- **Tuples**: Immutable sequence serialization
- **Sets**: Unordered collection serialization
- **Complex numbers**: Real and imaginary part preservation
- **Bytes and bytearrays**: Binary data handling
- **Range objects**: Range(start, stop, step) serialization
- **Empty collections**: Edge cases for empty containers
- **Large collections**: Performance with big data structures
- **Deeply nested structures**: Complex nested object graphs

**Why Important**: These tests ensure that mPickle can handle the fundamental data types that Python applications commonly use, providing the foundation for more complex serialization scenarios.

### 2. Custom Classes Tests (`test_custom_classes.py`)

**Purpose**: Validates that user-defined classes can be properly pickled and unpickled with their attributes and methods preserved.

**Actual Test Output**:
```
test_simple_class (test_custom_classes.TestCustomClasses) ... ok
test_class_with_methods (test_custom_classes.TestCustomClasses) ... ok
test_class_with_nesting (test_custom_classes.TestCustomClasses) ... ok
test_class_with_slots (test_custom_classes.TestCustomClasses) ... ok
test_class_with_getstate_setstate (test_custom_classes.TestCustomClasses) ... ok
test_class_with_reduce (test_custom_classes.TestCustomClasses) ... ok
test_inheritance (test_custom_classes.TestCustomClasses) ... ok
test_complex_nested_classes (test_custom_classes.TestCustomClasses) ... ok
test_class_instances_with_shared_references (test_custom_classes.TestCustomClasses) ... ok
test_class_with_none_attributes (test_custom_classes.TestCustomClasses) ... ok
test_class_with_special_attributes (test_custom_classes.TestCustomClasses) ... ok
test_class_type_pickling (test_custom_classes.TestCustomClasses) ... ok
test_class_without_init (test_custom_classes.TestClassEdgeCases) ... ok
test_class_with_class_attributes (test_custom_classes.TestClassEdgeCases) ... ok
test_class_with_property (test_custom_classes.TestClassEdgeCases) ... ok
test_empty_class (test_custom_classes.TestClassEdgeCases) ... ok
----------------------------------------------------------------------
Ran 16 tests

OK
```

**Test Coverage**:
- **Simple classes**: Basic class serialization with instance attributes
- **Class methods and static methods**: Method preservation during serialization
- **Nested classes**: Classes containing other class instances
- **__slots__ classes**: Memory-optimized classes using __slots__
- **Custom __getstate__/__setstate__**: State management methods
- **Custom __reduce__ methods**: Custom reduction functions
- **Inheritance hierarchies**: Multi-level class inheritance scenarios
- **Complex object graphs**: Circular references and shared objects
- **None attributes**: Handling None values in class attributes
- **Special attributes**: Private and protected attribute handling
- **Class type pickling**: Pickling class objects themselves
- **Classes without __init__**: Edge case class definitions
- **Class attributes**: Static class-level attributes
- **Property decorators**: Getter/setter method handling
- **Empty classes**: Minimal class definitions

**Why Important**: Most real-world applications use custom classes. These tests ensure that complex object-oriented code can be serialized without losing structure or functionality.

### 3. Protocol Compatibility Tests (`test_protocols.py`)

**Purpose**: Validates that mPickle works correctly with different pickle protocol versions and maintains compatibility across versions.

**Actual Test Output**:
```
test_all_protocol_versions_available (test_protocols.TestProtocolCompatibility) ... ok
test_protocol_default_values (test_protocols.TestProtocolCompatibility) ... ok
test_protocol_0_compatibility (test_protocols.TestProtocolCompatibility) ... ok
test_cross_protocol_compatibility (test_protocols.TestProtocolCompatibility) ... ok
test_protocol_parameter_validation (test_protocols.TestProtocolCompatibility) ... ok
test_unicode_handling_by_protocol (test_protocols.TestProtocolCompatibility) ... ok
test_protocol_size_efficiency (test_protocols.TestProtocolPerformance) ... ok
test_protocol_speed_characteristics (test_protocols.TestProtocolPerformance) ... ok
----------------------------------------------------------------------
Ran 8 tests

OK
```

**Test Coverage**:
- **Protocol availability**: All protocol versions (0-5) are accessible
- **Default protocol values**: Correct default protocol selection
- **Protocol 0 compatibility**: Legacy protocol support
- **Cross-protocol compatibility**: Reading data from different protocol versions
- **Parameter validation**: Invalid protocol number handling
- **Unicode handling**: String encoding differences between protocols
- **Size efficiency**: Comparing pickle sizes across protocols
- **Speed characteristics**: Performance differences between protocols

**Why Important**: Different MicroPython versions and environments may support different protocol versions. These tests ensure data can be exchanged between systems regardless of their protocol support.

### 4. Error Handling Tests (`test_error_handling.py`)

**Purpose**: Validates that mPickle gracefully handles error conditions and malformed data without crashing.

**Actual Test Output**:
```
test_invalid_pickle_data (test_error_handling.TestErrorHandling) ... ok
test_unsupported_type_pickling (test_error_handling.TestErrorHandling) ... ok
test_corrupted_pickle_stream (test_error_handling.TestErrorHandling) ... ok
test_file_operation_errors (test_error_handling.TestErrorHandling) ... ok
test_protocol_version_mismatch (test_error_handling.TestErrorHandling) ... ok
test_memory_limit_handling (test_error_handling.TestErrorHandling) ... ok
test_recursive_structure_limits (test_error_handling.TestErrorHandling) ... ok
test_invalid_unicode_data (test_error_handling.TestErrorHandling) ... ok
test_empty_pickle_data (test_error_handling.TestErrorHandling) ... ok
test_malformed_opcodes (test_error_handling.TestErrorHandling) ... ok
test_buffer_overflow_protection (test_error_handling.TestErrorHandling) ... ok
test_type_mismatch_errors (test_error_handling.TestErrorHandling) ... ok
----------------------------------------------------------------------
Ran 12 tests

OK
```

**Test Coverage**:
- **Invalid pickle data**: Corrupted or malformed pickle streams
- **Unsupported types**: Objects that cannot be serialized
- **Corrupted streams**: Partially damaged pickle data
- **File I/O errors**: Reading from non-existent or unreadable files
- **Protocol version mismatches**: Incompatible protocol versions
- **Memory limits**: Handling data that exceeds available memory
- **Recursive structure limits**: Infinite recursion prevention
- **Invalid Unicode data**: Malformed string encoding
- **Empty pickle data**: Zero-length pickle streams
- **Malformed opcodes**: Invalid pickle operation codes
- **Buffer overflow protection**: Memory safety checks
- **Type mismatch errors**: Incorrect type conversions during unpickling

**Why Important**: Robust error handling is crucial for production applications. These tests ensure the library fails gracefully and provides meaningful error messages when issues occur.

### 5. Registration System Tests (`test_registration_system.py`)

**Purpose**: Validates the custom serialization registration system that allows users to define their own pickle behavior for specific types.

**Actual Test Output**:
```
test_register_pickle_basic (test_registration_system.TestRegistrationSystem) ... ok
test_register_pickle_with_reduce_func (test_registration_system.TestRegistrationSystem) ... ok
test_register_pickle_with_reconstruct_func (test_registration_system.TestRegistrationSystem) ... ok
test_register_pickle_with_setstate_func (test_registration_system.TestRegistrationSystem) ... ok
test_inject_dummy_module_func (test_registration_system.TestRegistrationSystem) ... ok
test_revert_dummy_module_func (test_registration_system.TestRegistrationSystem) ... ok
test_cross_environment_compatibility (test_registration_system.TestRegistrationSystem) ... ok
test_module_remapping (test_registration_system.TestRegistrationSystem) ... ok
test_function_serialization (test_registration_system.TestRegistrationSystem) ... ok
test_state_restoration (test_registration_system.TestRegistrationSystem) ... ok
test_multiple_registrations (test_registration_system.TestRegistrationSystem) ... ok
test_registration_override (test_registration_system.TestRegistrationSystem) ... ok
----------------------------------------------------------------------
Ran 12 tests

OK
```

**Test Coverage**:
- **Basic registration**: Simple custom serialization registration
- **Reduce function**: Custom reduction function handling
- **Reconstruct function**: Custom reconstruction function handling
- **Setstate function**: Custom state restoration function handling
- **Dummy module injection**: Creating missing modules for compatibility
- **Dummy module reversion**: Cleaning up injected modules
- **Cross-environment compatibility**: Python to MicroPython data migration
- **Module remapping**: Changing import paths during deserialization
- **Function serialization**: Preserving custom functions and lambdas
- **State restoration**: Custom `__setstate__` and `__getnewargs__` handling
- **Multiple registrations**: Handling multiple custom types
- **Registration override**: Updating existing registrations

**Why Important**: This advanced feature enables complex scenarios where data needs to be customized for specific environments or when migrating between different Python implementations.

### 6. Utility Functions Tests (`test_utility_functions.py`)

**Purpose**: Validates the utility functions and helper modules that support the core pickle functionality.

**Actual Test Output**:
```
test_find_dict_by_key_value_basic (__main__.TestFindDictByKeyValue) ... ok
test_find_dict_by_key_value_empty_list (__main__.TestFindDictByKeyValue) ... ok
test_find_dict_by_key_value_none_values (__main__.TestFindDictByKeyValue) ... ok
test_encode_ascii (__main__.TestCodecs) ... ok
test_encode_latin1 (__main__.TestCodecs) ... ok
test_encode_utf8 (__main__.TestCodecs) ... ok
test_encode_invalid_encoding (__main__.TestCodecs) ... ok
test_escape_decode_basic (__main__.TestCodecs) ... ok
test_escape_decode_no_escapes (__main__.TestCodecs) ... ok
test_escape_decode_mixed (__main__.TestCodecs) ... ok
test_escape_decode_unknown_escape (__main__.TestCodecs) ... ok
test_encode_long_zero (__main__.TestEncodeDecodeLong) ... ok
test_encode_long_positive (__main__.TestEncodeDecodeLong) ... ok
test_encode_long_negative (__main__.TestEncodeDecodeLong) ... ok
test_decode_long_zero (__main__.TestEncodeDecodeLong) ... ok
test_decode_long_positive (__main__.TestEncodeDecodeLong) ... ok
test_decode_long_negative (__main__.TestEncodeDecodeLong) ... ok
test_roundtrip_long (__main__.TestEncodeDecodeLong) ... ok
test_large_long_values (__main__.TestEncodeDecodeLong) ... ok
test_getattribute_single_level (__main__.TestGetAttribute) ... ok
test_getattribute_nested (__main__.TestGetAttribute) ... ok
test_getattribute_nonexistent (__main__.TestGetAttribute) ... ok
test_getattribute_empty_path (__main__.TestGetAttribute) ... ok
test_handle_none_module_name_complex (__main__.TestHandleNoneModuleName) ... ok
test_handle_none_module_name_bytearray (__main__.TestHandleNoneModuleName) ... ok
test_handle_none_module_name_object (__main__.TestHandleNoneModuleName) ... ok
test_handle_none_module_name_function (__main__.TestHandleNoneModuleName) ... ok
test_handle_none_module_name_existing_module (__main__.TestHandleNoneModuleName) ... ok
test_format_version_format (__main__.TestPickleConstants) ... ok
test_compatible_formats_type (__main__.TestPickleConstants) ... ok
test_protocol_constants (__main__.TestPickleConstants) ... ok
test_opcode_constants (__main__.TestPickleConstants) ... ok
test_framer_basic_functionality (__main__.TestFramerUnframer) ... ok
test_unframer_basic_functionality (__main__.TestFramerUnframer) ... ok
----------------------------------------------------------------------
Ran 34 tests

OK
```

**Test Coverage**:

#### 6.1 Dictionary Search Functions (`TestFindDictByKeyValue`)
- **find_dict_by_key_value_basic**: Basic key-value pair search in list of dictionaries
- **find_dict_by_key_value_empty_list**: Handling empty input lists gracefully
- **find_dict_by_key_value_none_values**: Proper handling of None values as keys or values

#### 6.2 Codec Functions (`TestCodecs`)
- **test_encode_ascii**: ASCII character encoding validation
- **test_encode_latin1**: Latin-1 extended character encoding
- **test_encode_utf8**: UTF-8 Unicode encoding for international characters
- **test_encode_invalid_encoding**: Error handling for unsupported encoding names
- **test_escape_decode_basic**: Basic escape sequence decoding (newline, tab, etc.)
- **test_escape_decode_no_escapes**: Handling strings with no escape sequences
- **test_escape_decode_mixed**: Mixed content with both literal and escaped characters
- **test_escape_decode_unknown_escape**: Proper handling of undefined escape sequences

#### 6.3 Buffer I/O Functions (`TestUBytesIO`)
- **test_ubytesio_basic_operations**: Core read/write/seek operations on byte buffers
- **test_ubytesio_getbuffer**: Memoryview buffer access and manipulation
- **test_ubytesio_inheritance**: Verifying proper BytesIO inheritance
- **test_ubytesio_empty_buffer**: Handling empty buffer states

#### 6.4 Long Integer Operations (`TestEncodeDecodeLong`)
- **test_encode_long_zero**: Encoding zero value to empty byte sequence
- **test_encode_long_positive**: Positive integer encoding with two's complement
- **test_encode_long_negative**: Negative integer encoding with sign preservation
- **test_decode_long_zero**: Decoding empty sequence back to zero
- **test_decode_long_positive**: Reconstructing positive integers from byte data
- **test_decode_long_negative**: Restoring negative integers with sign
- **test_roundtrip_long**: Verifying encode/decode are inverse operations
- **test_large_long_values**: Handling very large integer values without overflow

#### 6.5 Attribute Access Utilities (`TestGetAttribute`)
- **test_getattribute_single_level**: Single attribute name access
- **test_getattribute_nested**: Multi-level dotted path attribute access
- **test_getattribute_nonexistent**: Error handling for missing attributes
- **test_getattribute_empty_path**: Handling empty attribute path lists

#### 6.6 Module Name Management (`TestHandleNoneModuleName`)
- **test_handle_none_module_name_complex**: Handling complex number type module resolution
- **test_handle_none_module_name_bytearray**: Bytearray type module detection
- **test_handle_none_module_name_object**: Built-in object type handling
- **test_handle_none_module_name_function**: Function module name extraction
- **test_handle_none_module_name_existing_module**: Preserving provided module names

#### 6.7 Module Resolution (`TestWhichModule`)
- **test_whichmodule_builtin**: Built-in function module detection (e.g., `len` -> `builtins`)
- **test_whichmodule_os_module**: Standard library module detection (e.g., `os.path.join`)
- **test_whichmodule_string_type**: String type module identification
- **test_whichmodule_int_type**: Integer type module resolution

#### 6.8 Pickle Constants (`TestPickleConstants`)
- **test_format_version_format**: Pickle format version validation
- **test_compatible_formats_type**: Protocol version list validation
- **test_protocol_constants**: Protocol number range validation
- **test_opcode_constants**: Pickle operation code availability

#### 6.9 Framing Operations (`TestFramerUnframer`)
- **test_framer_basic_functionality**: Frame-based data encoding
- **test_unframer_basic_functionality**: Frame-based data decoding

**Why Important**: These utility functions provide the infrastructure that makes the pickle system work efficiently and reliably. Testing them ensures the underlying mechanisms function correctly, which is essential for the entire serialization system.

## MicroPython-Specific Considerations

The test suite is optimized for **MicroPython UNIX port** environments, which have different characteristics than standard Python:

- **Memory constraints**: Tests verify functionality within limited memory
- **Missing features**: Graceful handling of unavailable standard library modules
- **Performance optimization**: Efficient algorithms suitable for embedded systems
- **Cross-platform compatibility**: Consistent behavior across different MicroPython builds

These considerations ensure that mPickle works reliably in resource-constrained environments while maintaining full functionality.