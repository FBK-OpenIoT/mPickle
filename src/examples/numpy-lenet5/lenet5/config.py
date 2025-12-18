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
# config.py - Configuration module for LeNet-5 package
#               This module contains constants, default settings, and
#               configuration options for the LeNet-5 neural network.
#



class ModelConfig:
    """Configuration for the LeNet-5 model."""
    
    # Model architecture constants
    INPUT_SHAPE = (1, 32, 32)  # (channels, height, width)
    NUM_CLASSES = 10
    
    # Layer configurations
    LAYER_CONFIG = {
        'C1': {'filters': 6, 'kernel_size': 5, 'stride': 1, 'padding': 0},
        'S2': {'pool_size': 2, 'stride': 2},
        'C3': {'filters': 16, 'kernel_size': 5, 'stride': 1, 'padding': 0},
        'S4': {'pool_size': 2, 'stride': 2},
        'C5': {'filters': 120, 'kernel_size': 5, 'stride': 1, 'padding': 0},
        'F6': {'units': 84},
        'output': {'units': 10}
    }
    
    # Default file names
    DEFAULT_WEIGHTS_FILE = "lenet5_weights.pkl"
    DEFAULT_MODEL_FILE = "lenet5_model.pkl"
    
    # Training parameters (if used)
    DEFAULT_BATCH_SIZE = 1
    DEFAULT_LEARNING_RATE = 0.01
    DEFAULT_EPOCHS = 10
    
    # Inference parameters
    INFERENCE_DELAY = 1.0  # seconds between inference iterations
    
    @classmethod
    def get_layer_summary(cls):
        """Get a summary of the layer configuration."""
        return cls.LAYER_CONFIG


class DataConfig:
    """Configuration for data generation."""
    
    # Default data generation parameters
    DEFAULT_BATCH_SIZE = 1
    DEFAULT_NOISE_LEVEL = 0.1
    DEFAULT_DIGIT_RANGE = (0, 9)
    
    # Image dimensions
    IMAGE_HEIGHT = 32
    IMAGE_WIDTH = 32
    IMAGE_CHANNELS = 1
    
    @classmethod
    def get_image_shape(cls):
        """Get the standard image shape."""
        return (cls.IMAGE_CHANNELS, cls.IMAGE_HEIGHT, cls.IMAGE_WIDTH)


class SystemConfig:
    """System-level configuration."""
    
    # Debug settings
    DEBUG_MODE = False
    VERBOSE_LOGGING = True
    
    # File paths
    BASE_PATH = "./"
    
    @classmethod
    def set_debug_mode(cls, enabled):
        """Enable or disable debug mode."""
        cls.DEBUG_MODE = enabled
    
    @classmethod
    def is_debug_mode(cls):
        """Check if debug mode is enabled."""
        return cls.DEBUG_MODE


# Convenience functions for common configurations

def get_default_weights_path():
    """Get the default path for model weights."""
    return SystemConfig.BASE_PATH + ModelConfig.DEFAULT_WEIGHTS_FILE


def get_inference_config():
    """Get default inference configuration."""
    return {
        'batch_size': ModelConfig.DEFAULT_BATCH_SIZE,
        'delay_seconds': ModelConfig.INFERENCE_DELAY,
        'weights_file': get_default_weights_path()
    }