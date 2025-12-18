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
# __init__.py - Core package for LeNet-5 neural network example, customly 
#                 designed for the mPickle project.
#

from .model import LeNet5
from .config import ModelConfig, DataConfig, SystemConfig, get_default_weights_path
from .utils import load_weights_from_file, save_weights_to_file, verify_weights_file
from .inference import LeNet5InferenceEngine, create_inference_engine
from .data import generate_sample_input

__all__ = [
    "LeNet5",
    "ModelConfig",
    "DataConfig",
    "SystemConfig",
    "get_default_weights_path",
    "load_weights_from_file",
    "save_weights_to_file",
    "verify_weights_file",
    "LeNet5InferenceEngine",
    "create_inference_engine",
    "generate_sample_input"
]