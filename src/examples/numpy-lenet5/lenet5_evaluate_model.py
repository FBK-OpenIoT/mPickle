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
# lenet5_evaluate_model.py - Model Evaluation Script
#           This script loads pre-trained weights into a LeNet-5 neural network
#           using the mPickle library for deserialization in MicroPython and
#           evaluates the model's performance on a generated test dataset.
#


from lenet5.model import LeNet5
from lenet5.utils import load_weights_from_file
from lenet5.config import get_default_weights_path
from lenet5.data import generate_sample_input

import os


def main():
    """Main function to load LeNet-5 model weights."""
    
    evaluation_dataset_size = 64
    dataset_noise = 0.5

    model_pretrained_path = "./weights/lenet5_weights_cpython.pkl"
    model_path = get_default_weights_path()

    # Check if pretrained model weights file exists
    if not (os.path.exists(model_path)):
        print("Model weights not found! Using pretrained model weights from CPython...")
        model_path = model_pretrained_path

    print("Initializing LeNet-5 network...")
    model = LeNet5()

    # Load weights using mPickle
    load_weights_from_file(model, model_path)
    
    print("\nLoad completed successfully!")

    print(model.get_summary())

    # Test the trained model using integrated evaluation function
    print("\n" + "="*50)
    print("Model Evaluation")
    print("="*50)
    
    # Generate test data (unseen during training)
    test_batch, test_labels = generate_sample_input(batch_size=evaluation_dataset_size, noise=dataset_noise)
    
    # Use the model's integrated evaluation method
    eval_results = model.evaluate(test_batch, test_labels)
    
    # Display evaluation results
    print(f"Test Accuracy: {eval_results['accuracy']:.3f}")
    print(f"Correct: {eval_results['correct']}/{eval_results['total']}")
    print(f"Error Rate: {eval_results['error_rate']:.3f}")

    return True


if __name__ == "__main__":
    main()