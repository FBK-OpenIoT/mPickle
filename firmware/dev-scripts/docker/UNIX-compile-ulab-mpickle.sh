#!/bin/sh

# -----------------------------------------------------------------------------
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
#
# UNIX-compile-ulab-mpickle.sh - Shell script to compile MicroPython
#                                 inside a Docker container for UNIX
#

. ./common.sh

echo "include(\"/mpy-compile/modules/mPickle/manifest.py\")" >> /mpy-compile/micropython/ports/unix/variants/manifest.py

# build with 4 dimensions
MATRIX_DIMENSIONS=4

cat > "/mpy-compile/micropython/ports/unix/makefile" <<EOL
CFLAGS += -DULAB_HAS_DTYPE_OBJECT=1
CFLAGS += -DMICROPY_FLOAT_IMPL=1

include Makefile
EOL

cd /mpy-compile/ulab
ln -s /mpy-compile/micropython micropython

# Overwrite the file with the new content
cat <<EOF > ./test-common.sh
echo "Skipping uLAB Tests..."
exit 1
EOF

./build.sh "$MATRIX_DIMENSIONS"
cd /mpy-compile/

cp /mpy-compile/micropython/ports/unix/build-$MATRIX_DIMENSIONS/micropython-$MATRIX_DIMENSIONS /mpy-compile/output/micropython
