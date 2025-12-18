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
# utils.py - Model Utilities for LeNet-5 package
#             This module provides utility functions for weight management and
#             model operations. The mPickle library is used for serialization in
#             MicroPython environments.
#


"""
Model Utilities

This module provides utility functions for weight management and model operations.
"""

try:
    import micropython #MicroPython
    import mpickle as pickle
    from ulab import numpy as np
    
    import register_pickle_funcs
    pickle.mpickle.DEBUG_MODE = False
except ImportError: #CPython
    import numpy as np
    import pickle

import os
from .config import ModelConfig


def load_weights_from_file(model, weights_file=None):
    """
    Load weights from file into the model.
    
    Args:
        model: LeNet5 model instance
        weights_file: Path to weights file (None for default)
        
    Returns:
        bool: True if successful, False otherwise
    """
    weights_file = weights_file or ModelConfig.DEFAULT_WEIGHTS_FILE
    
    if os.path.exists(weights_file):
        print(f"Weights file '{weights_file}' found. Loading weights...")
        try:
            with open(weights_file, 'rb') as f:
                weights_dict = pickle.load(f)
                model.load_weights_dict(weights_dict)
            
            print("✓ Weights loaded successfully!")
            print(f"  Architecture: {weights_dict['architecture']}")
            return True
        except Exception as e:
            print(f"✗ Error loading weights: {e}")
            print("Using random initialized weights.")
            return False
    else:
        print(f"Weights file '{weights_file}' not found. Using random initialized weights.")
        return False


def save_weights_to_file(model, weights_file=None):
    """
    Save model weights to file.
    
    Args:
        model: LeNet5 model instance
        weights_file: Path to save weights (None for default)
        
    Returns:
        bool: True if successful, False otherwise
    """
    weights_file = weights_file or ModelConfig.DEFAULT_WEIGHTS_FILE
    
    print(f"Saving weights to '{weights_file}'...")
    
    try:
        weights_dict = model.get_weights_dict()
        
        # Display weight information
        print("\nWeight shapes:")
        for key, value in weights_dict.items():
            if key != 'architecture':
                print(f"  {key}: {value.shape}")
        
        with open(weights_file, 'wb') as f:
            pickle.dump(weights_dict, f)
        
        print(f"✓ Weights saved successfully!")
        
        # Get file size
        file_size = os.stat(weights_file)[6]
        print(f"  File size: {file_size} B (~{file_size / 1024:.2f} KB)")
        
        return True
    except Exception as e:
        print(f"✗ Error saving weights: {e}")
        return False


def verify_weights_file(weights_file=None):
    """
    Verify that weights can be loaded from file.
    
    Args:
        weights_file: Path to weights file (None for default)
        
    Returns:
        bool: True if verification successful, False otherwise
    """
    weights_file = weights_file or ModelConfig.DEFAULT_WEIGHTS_FILE
    
    print("\nVerifying saved weights...")
    try:
        with open(weights_file, 'rb') as f:
            loaded_weights = pickle.load(f)
        
        print("✓ Weights loaded successfully!")
        print(f"  Architecture: {loaded_weights['architecture']}")
        print(f"  Number of weight tensors: {len(loaded_weights) - 1}")
        
        return True
    except Exception as e:
        print(f"✗ Error loading weights: {e}")
        return False