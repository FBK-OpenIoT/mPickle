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
# Dockerfile - docker file to build compilation image
#

FROM debian:bookworm-slim
WORKDIR /mpy-compile
ENV WORKDIR=/mpy-compile
### SYSTEM DEPENDENCIES
RUN apt update -y \
&& apt install -y \
build-essential \
libffi-dev \
git \
pkg-config \
gcc-arm-none-eabi \
libnewlib-arm-none-eabi \
wget \
flex \
bison \
gperf \
python3 \
python3-pip \
python3-venv \
cmake \
ninja-build \
ccache \
libffi-dev \
libssl-dev \
udev \
dfu-util \
libusb-1.0-0 \
stlink-tools \
&& rm -rf /var/lib/apt/lists/*
### MICROPYTHON SETUP
ENV MICROPYTHON_VERSION=v1.25.0
RUN git clone --depth 1 --branch ${MICROPYTHON_VERSION} https://github.com/micropython/micropython.git \
&& git -C micropython submodule update --init  \
&& make -C micropython/mpy-cross -j $(nproc)
### ESP-IDF SETUP
ENV IDF_VERSION=v5.4.1
ENV IDF_PATH=${WORKDIR}/esp-idf
RUN git clone -b ${IDF_VERSION} --recursive https://github.com/espressif/esp-idf.git \
&& ${IDF_PATH}/install.sh all

COPY . /mpy-compile/
