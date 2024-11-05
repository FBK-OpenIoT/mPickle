CPYTHON=python3
MPYTHON=../../firmware/dev-scripts/generic/output/unix/standard:latest/micropython

test() {
    echo "\e[0;36mtesting \e[1;36m$1\e[0m"
    echo
    OUT1=$($CPYTHON -c "${4-""}from pickle_tests import dump; dump(${2-$1})")
    OUT2=$($MPYTHON -c "${4-""}from pickle_tests import load; load()")
    echo "CPY - WRITE ->" $OUT1
    echo "MPY - READ  ->" $OUT2
    [ "$OUT1" = "$OUT2" ] && echo "\e[0;32mOK" || echo "\e[0;31mERR"
    echo "\e[0m"
    OUT1=$($MPYTHON -c "${4-""}from pickle_tests import dump; dump(${3-$1})")
    OUT2=$($CPYTHON -c "${4-""}from pickle_tests import load; load()")
    echo "MPY - WRITE ->" $OUT1
    echo "CPY - READ  ->" $OUT2
    [ "$OUT1" = "$OUT2" ] && echo "\e[0;32mOK" || echo "\e[0;31mERR"
    echo "\e[0m"
}

test "str" "'foo'" "'bar'"
test "int" "0" "1"
test "float" "1.5" "2.5"
test "complex" "1+2j" "3+4j"
test "bool" "False" "True"
test "bytes" "bytes(1)" "bytes(2)"
test "bytearray" "bytearray('foo', 'utf-8')" "bytearray('bar', 'utf-8')"
test "list" "[1,2,3]" "[3,2,1]"
test "tuple" "(1, 'foo', True)" "(0, 'bar', False)"
test "set" "{0, 'foo', True}" "{1, 'bar', False}"
test "dict" "{'int': 0, 'str': 'foo', 'bool': True}" "{'int': 1, 'str': 'bar', 'bool': False}"
test "None"
test "NotImplemented"
test "Ellipsis"
test "custom class" "CustomClass" "CustomClass" "import sys; sys.path.append('custom-class'); from example import CustomClass;"
test "custom class instance" "CustomClass()" "CustomClass()" "import sys; sys.path.append('custom-class'); from example import CustomClass;"

rm dump