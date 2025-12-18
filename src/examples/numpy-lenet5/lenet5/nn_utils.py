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
# nn_utils.py - Neural network utilities for LeNet-5 package
#             This module contains the utility functions for neural network 
#             operations including convolution, pooling, activation functions,
#             and weight initialization.   
#

try:
    import micropython
    from ulab import numpy as np
    from ulab import dtype as udtype
    from register_pickle_funcs import dtype_convert_matrix
    def dtype(x):
        #utility function to convert dtype from ulab to numpy
        return dtype_convert_matrix[str(udtype(x))]
    
    IS_MICROPYTHON = True

except ImportError:
    import numpy as np
    from numpy import dtype

    IS_MICROPYTHON = False

import math
import random

def relu(x):
    return np.maximum(0.0, x)


def tanh_activation(x):
    return np.tanh(x, dtype=dtype('float32'))


def box_muller_random(scale=1.0):
    """
    Generate Gaussian random variable using Box-Muller transform.
    This is MicroPython compatible (no random.gauss).
    """
    u1 = random.random()
    u2 = random.random()
    if u1 < 1e-10:
        u1 = 1e-10
    z = math.sqrt(-2.0 * math.log(u1)) * math.cos(2.0 * math.pi * u2)
    return z * scale


def he_init(shape):
    """He initialization for weights using Box-Muller transform."""
    if len(shape) == 2:  # Fully connected
        n_input = shape[0]
    else:  # Convolutional
        n_input = shape[1] * shape[2] * shape[3]
    
    scale = math.sqrt(2.0 / n_input)
    
    # Generate random weights
    weights = np.zeros(shape, dtype=dtype('float32'))
    flat_size = 1
    for dim in shape:
        flat_size *= dim
    
    # Fill with random values using Box-Muller for gaussian
    for idx in range(flat_size):
        # Calculate multi-dimensional index
        temp_idx = idx
        indices = []
        for dim in reversed(shape):
            indices.insert(0, temp_idx % dim)
            temp_idx //= dim
        
        val = box_muller_random(scale)
        
        if len(shape) == 4:
            weights[indices[0], indices[1], indices[2], indices[3]] = val
        elif len(shape) == 2:
            weights[indices[0], indices[1]] = val
    
    return weights


def conv2d(input_data, weights, biases, stride=1, padding=0):
    """
    2D convolution using ulab operations.
    
    Args:
        input_data: (batch, in_channels, height, width)
        weights: (out_channels, in_channels, kernel_h, kernel_w)
        biases: (out_channels,)
    """
    batch_size, in_channels, input_height, input_width = input_data.shape
    out_channels, _, kernel_size, _ = weights.shape
    
    # Calculate output dimensions
    output_height = (input_height + 2 * padding - kernel_size) // stride + 1
    output_width = (input_width + 2 * padding - kernel_size) // stride + 1
    
    # Apply padding if needed
    if padding > 0:
        padded = np.zeros((batch_size, in_channels, 
                          input_height + 2*padding, input_width + 2*padding), dtype=dtype('float32'))
        padded[:, :, padding:-padding, padding:-padding] = input_data
    else:
        padded = input_data
    
    # Initialize output
    output = np.zeros((batch_size, out_channels, output_height, output_width), dtype=dtype('float32'))
    
    # Perform convolution
    for b in range(batch_size):
        for oc in range(out_channels):
            for i in range(output_height):
                for j in range(output_width):
                    # Extract patch
                    start_i = i * stride
                    start_j = j * stride
                    patch = padded[b, :, start_i:start_i+kernel_size, 
                                  start_j:start_j+kernel_size]
                    
                    # Compute convolution
                    conv_val = np.sum(patch * weights[oc])
                    output[b, oc, i, j] = conv_val + biases[oc]
    
    return relu(output)


def avg_pool2d(input_data, kernel_size=2, stride=2):
    """
    2D average pooling using ulab.
    
    Args:
        input_data: (batch, channels, height, width)
    """
    batch_size, channels, input_height, input_width = input_data.shape
    
    # Calculate output dimensions
    output_height = (input_height - kernel_size) // stride + 1
    output_width = (input_width - kernel_size) // stride + 1
    
    # Initialize output
    output = np.zeros((batch_size, channels, output_height, output_width), dtype=dtype('float32'))
    
    # Perform pooling
    for b in range(batch_size):
        for c in range(channels):
            for i in range(output_height):
                for j in range(output_width):
                    start_i = i * stride
                    start_j = j * stride
                    patch = input_data[b, c, start_i:start_i+kernel_size, 
                                      start_j:start_j+kernel_size]
                    output[b, c, i, j] = np.mean(patch)
    
    return output


def flatten(input_data):
    """Flatten tensor using ulab."""
    batch_size = input_data.shape[0]
    flat_size = 1
    for dim in input_data.shape[1:]:
        flat_size *= dim
    
    # Reshape to (batch_size, flat_size)
    output = np.zeros((batch_size, flat_size), dtype=dtype('float32'))
    
    # Manual flattening for ulab compatibility
    if len(input_data.shape) == 4:
        batch, channels, height, width = input_data.shape
        for b in range(batch):
            idx = 0
            for c in range(channels):
                for h in range(height):
                    for w in range(width):
                        output[b, idx] = input_data[b, c, h, w]
                        idx += 1
    
    return output


def dense(input_data, weights, biases):
    """Dense layer using ulab matrix operations."""
    # Matrix multiplication: input @ weights + biases
    output = np.dot(input_data, weights)
    
    # Add biases
    for i in range(output.shape[0]):
        for j in range(output.shape[1]):
            output[i, j] += biases[j]
    
    return tanh_activation(output)


def softmax(x):
    """Softmax activation using ulab."""
    # Subtract max for numerical stability
    x_max = np.max(x, axis=1, keepdims=True)
    exp_x = np.exp(x - x_max)
    sum_exp = np.sum(exp_x, axis=1, keepdims=True)
    return exp_x / sum_exp


def shuffle_func(array):
    """Fisher–Yates shuffle"""
    for i in range(len(array)-1, 0, -1):
        j = random.randrange(i+1)
        array[i], array[j] = array[j], array[i]


def one_hot(labels, num_classes=10):
    # labels: (batch,) ints OR single int
    if isinstance(labels, (int, float)):
        y = np.zeros((1, num_classes))
        y[0, int(labels)] = 1.0
        return y

    batch = len(labels)
    y = np.zeros((batch, num_classes))
    for i in range(batch):
        y[i, int(labels[i])] = 1.0
    return y


def cross_entropy(y_pred, y_true, eps=1e-9):
    # y_pred, y_true: (batch, num_classes)
    batch = y_pred.shape[0]
    loss = 0.0
    for b in range(batch):
        for k in range(y_pred.shape[1]):
            if y_true[b, k] == 1.0:
                p = y_pred[b, k]
                if p < eps:
                    p = eps
                loss -= math.log(p)
                break
    return loss / batch


def sum_axis0_2d(x):
    # x: (batch, features) -> (features,)
    batch, feat = x.shape
    s = np.zeros((feat,))
    for j in range(feat):
        acc = 0.0
        for i in range(batch):
            acc += x[i, j]
        s[j] = acc
    return s


# NumPy fast-path overrides for CPython
if not IS_MICROPYTHON:
    from numpy.lib.stride_tricks import as_strided

    # ---- faster + NumPy-compatible tanh ----
    def tanh_activation(x):
        # NumPy has no dtype= kwarg for tanh
        y = np.tanh(x)
        return y.astype(np.float32, copy=False)

    # ---- faster He init on NumPy ----
    def he_init(shape):
        if len(shape) == 2:
            n_input = shape[0]
        else:
            n_input = shape[1] * shape[2] * shape[3]
        scale = np.sqrt(2.0 / n_input)
        return (np.random.standard_normal(size=shape).astype(np.float32) * np.float32(scale))

    # ---- vectorized helpers ----
    def sum_axis0_2d(x):
        return np.sum(x, axis=0)

    def cross_entropy(y_pred, y_true, eps=1e-9):
        y_pred = np.clip(y_pred, eps, 1.0)
        return -np.mean(np.sum(y_true * np.log(y_pred), axis=1))

    def one_hot(labels, num_classes=10):
        labels = np.asarray(labels, dtype=np.int64)
        return np.eye(num_classes, dtype=np.float32)[labels]

    # ---- flatten / backward ----
    def flatten(input_data):
        return input_data.reshape(input_data.shape[0], -1).astype(np.float32, copy=False)

    # ---- dense / backward (tanh) ----
    def dense(input_data, weights, biases):
        # (B,in)@(in,out) + (out,) broadcast
        z = input_data @ weights + biases
        return tanh_activation(z)

    # ---- im2col / col2im for NCHW ----
    def _im2col_nchw(X, KH, KW, stride=1, padding=0):
        B, C, H, W = X.shape
        if padding > 0:
            Xp = np.pad(X, ((0, 0), (0, 0), (padding, padding), (padding, padding)), mode="constant")
        else:
            Xp = X

        Hp, Wp = Xp.shape[2], Xp.shape[3]
        out_h = (Hp - KH) // stride + 1
        out_w = (Wp - KW) // stride + 1

        sB, sC, sH, sW = Xp.strides
        shape = (B, C, out_h, out_w, KH, KW)
        strides = (sB, sC, sH * stride, sW * stride, sH, sW)

        patches = as_strided(Xp, shape=shape, strides=strides)
        # -> (B*out_h*out_w, C*KH*KW)
        cols = patches.transpose(0, 2, 3, 1, 4, 5).reshape(B * out_h * out_w, -1)
        return cols, out_h, out_w, Xp.shape

    def _col2im_nchw(cols, X_shape, KH, KW, out_h, out_w, stride=1, padding=0, Xp_shape=None):
        B, C, H, W = X_shape
        if Xp_shape is None:
            Hp, Wp = H + 2 * padding, W + 2 * padding
        else:
            Hp, Wp = Xp_shape[2], Xp_shape[3]

        dXp = np.zeros((B, C, Hp, Wp), dtype=cols.dtype)

        cols = cols.reshape(B, out_h, out_w, C, KH, KW)

        # Loop only over kernel dims (25 for 5x5) — still fast on NumPy
        for kh in range(KH):
            ih_end = kh + stride * out_h
            for kw in range(KW):
                iw_end = kw + stride * out_w
                dXp[:, :, kh:ih_end:stride, kw:iw_end:stride] += cols[:, :, :, :, kh, kw].transpose(0, 3, 1, 2)

        if padding > 0:
            return dXp[:, :, padding:-padding, padding:-padding]
        return dXp

    # ---- conv2d / backward (ReLU included) ----
    def conv2d(input_data, weights, biases, stride=1, padding=0):
        # input: (B,C,H,W), weights: (O,C,KH,KW), biases: (O,)
        B, C, H, W = input_data.shape
        O, _, KH, KW = weights.shape

        X_col, out_h, out_w, Xp_shape = _im2col_nchw(input_data, KH, KW, stride=stride, padding=padding)
        W_col = weights.reshape(O, -1)

        out = X_col @ W_col.T
        out += biases  # broadcast (O,)
        out = out.reshape(B, out_h, out_w, O).transpose(0, 3, 1, 2)

        return np.maximum(out, 0.0)

    def relu_backward(dA, A):
        return dA * (A > 0.0)

    def conv2d_backward(dA, X, W, A, stride=1, padding=0):
        # dA matches A (post-ReLU)
        dZ = relu_backward(dA, A)

        B, C, H, W_in = X.shape
        O, _, KH, KW = W.shape

        X_col, out_h, out_w, Xp_shape = _im2col_nchw(X, KH, KW, stride=stride, padding=padding)

        dZ_col = dZ.transpose(0, 2, 3, 1).reshape(-1, O)  # (B*out_h*out_w, O)

        dW = (dZ_col.T @ X_col).reshape(W.shape)
        db = np.sum(dZ_col, axis=0)

        W_col = W.reshape(O, -1)
        dX_col = dZ_col @ W_col
        dX = _col2im_nchw(dX_col, X.shape, KH, KW, out_h, out_w, stride=stride, padding=padding, Xp_shape=Xp_shape)
        return dX, dW, db

    # ---- avg pool / backward (LeNet uses 2x2, stride=2) ----
    def avg_pool2d(input_data, kernel_size=2, stride=2):
        B, C, H, W = input_data.shape
        out_h = (H - kernel_size) // stride + 1
        out_w = (W - kernel_size) // stride + 1

        if kernel_size == 2 and stride == 2 and (H % 2 == 0) and (W % 2 == 0):
            x = input_data.reshape(B, C, out_h, 2, out_w, 2)
            return np.mean(x, axis=(3, 5))
        else:
            # generic strided pooling
            sB, sC, sH, sW = input_data.strides
            shape = (B, C, out_h, out_w, kernel_size, kernel_size)
            strides = (sB, sC, sH * stride, sW * stride, sH, sW)
            patches = as_strided(input_data, shape=shape, strides=strides)
            return np.mean(patches, axis=(4, 5))

    def avg_pool2d_backward(dout, input_shape, kernel_size=2, stride=2):
        B, C, H, W = input_shape
        if kernel_size == 2 and stride == 2 and (H % 2 == 0) and (W % 2 == 0):
            scale = 1.0 / (kernel_size * kernel_size)
            # expand each dout cell into a 2x2 block
            dx = np.repeat(np.repeat(dout, 2, axis=2), 2, axis=3) * scale
            return dx
        else:
            # generic fallback
            _, _, out_h, out_w = dout.shape
            dX = np.zeros((B, C, H, W), dtype=dout.dtype)
            scale = 1.0 / (kernel_size * kernel_size)
            for i in range(out_h):
                for j in range(out_w):
                    si = i * stride
                    sj = j * stride
                    dX[:, :, si:si+kernel_size, sj:sj+kernel_size] += dout[:, :, i:i+1, j:j+1] * scale
            return dX