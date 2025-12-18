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
# data.py - Data utilities for LeNet-5 package
#             This module contains functions for generating synthetic MNIST-like
#             digit images for testing the LeNet-5 neural network.
#


import random
try:
    from ulab import numpy as np
except ImportError:
    import numpy as np


def generate_digit_0(img, offset_x=10, offset_y=10, noise=0.1):
    """Generate a '0' digit pattern"""
    # Outer circle
    for i in range(4, 16):
        for j in range(6, 14):
            dist_from_center = ((i-9.5)**2 + (j-10)**2)**0.5
            if 3.5 <= dist_from_center <= 5.5:
                img[0, offset_y+i, offset_x+j] = 0.9 + random.uniform(-noise, noise)


def generate_digit_1(img, offset_x=10, offset_y=10, noise=0.1):
    """Generate a '1' digit pattern"""
    # Vertical line
    for i in range(3, 17):
        for j in range(9, 12):
            img[0, offset_y+i, offset_x+j] = 0.9 + random.uniform(-noise, noise)
    # Top diagonal
    for i in range(3, 6):
        j = 8 - (i - 3)
        img[0, offset_y+i, offset_x+j] = 0.8 + random.uniform(-noise, noise)


def generate_digit_2(img, offset_x=10, offset_y=10, noise=0.1):
    """Generate a '2' digit pattern"""
    # Top curve
    for j in range(6, 14):
        i = 4
        img[0, offset_y+i, offset_x+j] = 0.9 + random.uniform(-noise, noise)
    # Right side
    for i in range(4, 9):
        img[0, offset_y+i, offset_x+13] = 0.9 + random.uniform(-noise, noise)
    # Middle diagonal
    for k in range(6):
        i = 8 + k
        j = 13 - k
        img[0, offset_y+i, offset_x+j] = 0.9 + random.uniform(-noise, noise)
    # Bottom line
    for j in range(6, 14):
        img[0, offset_y+15, offset_x+j] = 0.9 + random.uniform(-noise, noise)


def generate_digit_3(img, offset_x=10, offset_y=10, noise=0.1):
    """Generate a '3' digit pattern"""
    # Top horizontal
    for j in range(6, 14):
        img[0, offset_y+4, offset_x+j] = 0.9 + random.uniform(-noise, noise)
    # Middle horizontal
    for j in range(8, 14):
        img[0, offset_y+9, offset_x+j] = 0.9 + random.uniform(-noise, noise)
    # Bottom horizontal
    for j in range(6, 14):
        img[0, offset_y+15, offset_x+j] = 0.9 + random.uniform(-noise, noise)
    # Right side
    for i in range(4, 16):
        if i != 9:
            img[0, offset_y+i, offset_x+13] = 0.9 + random.uniform(-noise, noise)


def generate_digit_4(img, offset_x=10, offset_y=10, noise=0.1):
    """Generate a '4' digit pattern"""
    # Left vertical
    for i in range(3, 11):
        img[0, offset_y+i, offset_x+6] = 0.9 + random.uniform(-noise, noise)
    # Horizontal
    for j in range(6, 14):
        img[0, offset_y+10, offset_x+j] = 0.9 + random.uniform(-noise, noise)
    # Right vertical
    for i in range(3, 17):
        img[0, offset_y+i, offset_x+12] = 0.9 + random.uniform(-noise, noise)


def generate_digit_5(img, offset_x=10, offset_y=10, noise=0.1):
    """Generate a '5' digit pattern"""
    # Top horizontal
    for j in range(6, 14):
        img[0, offset_y+4, offset_x+j] = 0.9 + random.uniform(-noise, noise)
    # Left vertical (top)
    for i in range(4, 10):
        img[0, offset_y+i, offset_x+6] = 0.9 + random.uniform(-noise, noise)
    # Middle horizontal
    for j in range(6, 14):
        img[0, offset_y+9, offset_x+j] = 0.9 + random.uniform(-noise, noise)
    # Right vertical (bottom)
    for i in range(9, 16):
        img[0, offset_y+i, offset_x+13] = 0.9 + random.uniform(-noise, noise)
    # Bottom horizontal
    for j in range(6, 14):
        img[0, offset_y+15, offset_x+j] = 0.9 + random.uniform(-noise, noise)


def generate_digit_6(img, offset_x=10, offset_y=10, noise=0.1):
    """Generate a '6' digit pattern"""
    # Left vertical
    for i in range(4, 16):
        img[0, offset_y+i, offset_x+6] = 0.9 + random.uniform(-noise, noise)
    # Top horizontal
    for j in range(6, 11):
        img[0, offset_y+4, offset_x+j] = 0.9 + random.uniform(-noise, noise)
    # Middle horizontal
    for j in range(6, 14):
        img[0, offset_y+10, offset_x+j] = 0.9 + random.uniform(-noise, noise)
    # Bottom curve
    for j in range(6, 14):
        img[0, offset_y+15, offset_x+j] = 0.9 + random.uniform(-noise, noise)
    # Right vertical (bottom)
    for i in range(10, 16):
        img[0, offset_y+i, offset_x+13] = 0.9 + random.uniform(-noise, noise)


def generate_digit_7(img, offset_x=10, offset_y=10, noise=0.1):
    """Generate a '7' digit pattern"""
    # Top horizontal
    for j in range(6, 14):
        img[0, offset_y+4, offset_x+j] = 0.9 + random.uniform(-noise, noise)
    # Diagonal line
    for k in range(12):
        i = 4 + k
        j = 13 - int(k * 0.5)
        img[0, offset_y+i, offset_x+j] = 0.9 + random.uniform(-noise, noise)


def generate_digit_8(img, offset_x=10, offset_y=10, noise=0.1):
    """Generate an '8' digit pattern"""
    # Top loop
    for i in range(4, 10):
        img[0, offset_y+i, offset_x+6] = 0.9 + random.uniform(-noise, noise)
        img[0, offset_y+i, offset_x+13] = 0.9 + random.uniform(-noise, noise)
    for j in range(6, 14):
        img[0, offset_y+4, offset_x+j] = 0.9 + random.uniform(-noise, noise)
        img[0, offset_y+9, offset_x+j] = 0.9 + random.uniform(-noise, noise)
    # Bottom loop
    for i in range(9, 16):
        img[0, offset_y+i, offset_x+6] = 0.9 + random.uniform(-noise, noise)
        img[0, offset_y+i, offset_x+13] = 0.9 + random.uniform(-noise, noise)
    for j in range(6, 14):
        img[0, offset_y+15, offset_x+j] = 0.9 + random.uniform(-noise, noise)


def generate_digit_9(img, offset_x=10, offset_y=10, noise=0.1):
    """Generate a '9' digit pattern"""
    # Top horizontal
    for j in range(6, 14):
        img[0, offset_y+4, offset_x+j] = 0.9 + random.uniform(-noise, noise)
    # Left vertical (top)
    for i in range(4, 10):
        img[0, offset_y+i, offset_x+6] = 0.9 + random.uniform(-noise, noise)
    # Middle horizontal
    for j in range(6, 14):
        img[0, offset_y+9, offset_x+j] = 0.9 + random.uniform(-noise, noise)
    # Right vertical
    for i in range(4, 16):
        img[0, offset_y+i, offset_x+13] = 0.9 + random.uniform(-noise, noise)
    # Bottom horizontal
    for j in range(9, 14):
        img[0, offset_y+15, offset_x+j] = 0.9 + random.uniform(-noise, noise)


def generate_sample_input(batch_size=1, digit=None, noise=0.1):
    """
    Generate MNIST-like digit images as ulab array.
    
    Args:
        batch_size: Number of samples to generate
        digit: Specific digit to generate (0-9), or None for random
        noise: Amount of random noise to add (0.0 to 0.2 recommended)
    
    Returns:
        numpy array of shape (batch_size, 1, 32, 32)
        list of digit labels
    """
    digit_generators = [
        generate_digit_0,
        generate_digit_1,
        generate_digit_2,
        generate_digit_3,
        generate_digit_4,
        generate_digit_5,
        generate_digit_6,
        generate_digit_7,
        generate_digit_8,
        generate_digit_9
    ]
    
    # Create input with shape (batch_size, 1, 32, 32)
    input_image = np.zeros((batch_size, 1, 32, 32))
    labels = []
    
    for b in range(batch_size):
        # Choose digit
        if digit is not None:
            current_digit = digit
        else:
            current_digit = random.randint(0, 9)
        
        labels.append(current_digit)
        
        # Generate the digit
        digit_generators[current_digit](input_image[b], 
                                          offset_x=10, 
                                          offset_y=8, 
                                          noise=noise)
        
        # Add slight random variations in position
        offset_variation_x = random.randint(-2, 2)
        offset_variation_y = random.randint(-2, 2)
        
        # Apply background noise
        for i in range(32):
            for j in range(32):
                if input_image[b, 0, i, j] < 0.1:
                    input_image[b, 0, i, j] = random.uniform(0, 0.1)
    
    return input_image, labels