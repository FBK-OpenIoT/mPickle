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
# inference.py - Inference engine for LeNet-5 package
#             This module contains the inference engine and related utilities
#             for running predictions with the LeNet-5 neural network.
#


import time
from .model import LeNet5
from .data import generate_sample_input
from .utils import load_weights_from_file


class LeNet5InferenceEngine:
    """
    Inference engine for LeNet-5 model that handles model loading and prediction.
    """
    
    def __init__(self, weights_file=None):
        """
        Initialize the inference engine.
        
        Args:
            weights_file: Path to the weights file to load (None for default)
        """
        self.weights_file = weights_file
        self.model = None
        self._initialize_model()
    
    def _initialize_model(self):
        """Initialize the LeNet-5 model and load weights."""
        print("Initializing LeNet-5 inference engine...")
        self.model = LeNet5()
        
        # Load weights if available
        if not load_weights_from_file(self.model, self.weights_file):
            print("No weights loaded - using random initialization")
        
        print("Inference engine ready!")
        print(self.model.get_summary())
    
    def predict(self, input_data):
        """
        Run prediction on input data.
        
        Args:
            input_data: Input tensor of shape (batch_size, 1, 32, 32)
            
        Returns:
            tuple: (predicted_class, probabilities)
        """
        if self.model is None:
            raise RuntimeError("Model not initialized")
        
        return self.model.predict(input_data)
    
    def run_continuous_inference(self, batch_size=1, delay_seconds=1):
        """
        Run continuous inference on randomly generated samples.
        
        Args:
            batch_size: Number of samples to generate per iteration
            delay_seconds: Delay between iterations in seconds
        """
        try:
            while True:
                # Generate sample input
                print(f"\nGenerating random inputs (batch_size={batch_size})...")
                sample_batch, sample_labels = generate_sample_input(batch_size=batch_size)

                for i in range(batch_size):
                    sample_input = sample_batch[i:i+1]
                    sample_label = sample_labels[i]

                    print(f"Input shape: {sample_input.shape}")
                    
                    # Run inference
                    print("Running inference...")
                    output, _ = self.model.forward(sample_input)

                    print(f"Output shape: {output.shape}")
                    predicted_class, probabilities = self.predict(sample_input)
                    
                    # Display results
                    print(f"\nPredicted class: {predicted_class} (Expected: {sample_label})")
                    print("Output probabilities:")
                    for cls_idx in range(10):
                        print(f"  Class {cls_idx}: {probabilities[cls_idx]:.4f}")
                    
                    print("="*60)
                
                time.sleep(delay_seconds)
                
        except KeyboardInterrupt:
            print("\nInference stopped by user.")
    
    def get_model_summary(self):
        """Get model architecture summary."""
        return self.model.get_summary()


def create_inference_engine(weights_file=None):
    """
    Factory function to create an inference engine instance.
    
    Args:
        weights_file: Path to weights file
        
    Returns:
        LeNet5InferenceEngine: Initialized inference engine
    """
    return LeNet5InferenceEngine(weights_file)