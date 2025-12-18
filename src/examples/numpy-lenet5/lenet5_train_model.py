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
# lenet5_train_model.py - Lenet-5 Model Trainer
#           This script creates and trains a LeNet-5 neural network using 
#           randomly generated digit images. It saves the trained model weights
#           to a file using the pickle library for serialization in CPython.
#           Weights can then be loaded in MicroPython using mPickle.
#

try:
    import micropython #MicroPython
    import mpickle as pickle

    import register_pickle_funcs
    pickle.mpickle.DEBUG_MODE = False

    IS_MICROPYTHON = True
except ImportError: #CPython
    print("Warning: ulab or micropython not available")
    import pickle # Native Pickle for CPython
    IS_MICROPYTHON = False

# Import from the new integrated structure
from lenet5.model import LeNet5
from lenet5.data import generate_sample_input


def main():
    model_file = "lenet5_weights.pkl"
    model = LeNet5()

    print("\n" + "="*50)
    dataset_noise = 0.5
    if IS_MICROPYTHON:
        print("Training LeNet-5 model on MicroPython...")
        epochs = 10
        batch_size = 16
        train_dataset_size = 1024
        evaluation_dataset_size = 128
        lr = 0.01
    else:
        print("Training LeNet-5 model on CPython...")
        epochs = 5
        batch_size = 32
        train_dataset_size = 16*1024
        evaluation_dataset_size = 1024
        lr = 0.01
        
    
    print("="*50)
    sample_batch, sample_labels = generate_sample_input(batch_size=train_dataset_size, noise=dataset_noise)
    model.train(sample_batch, sample_labels, epochs=epochs, lr=lr, batch_size=batch_size, verbose=True)
    print("Training completed.")

    # Storing weights
    print("Exporting model weights...")
    weights_dict = model.get_weights_dict()
    
    # Display weight information
    print("\nWeight shapes:")
    for key, value in weights_dict.items():
        if key != 'architecture':
            print(f"  {key}: {value.shape}")
    
    # Save weights using pickle
    print(f"\nSaving weights to '{model_file}'...")
    
    try:
        with open(model_file, 'wb') as f:
            pickle.dump(weights_dict, f)
        print(f"✓ Weights saved successfully!")
        
        # Get file size
        import os
        file_size = os.stat(model_file)[6]
        print(f"  File size: {file_size} B (~{file_size / 1024:.2f} KB)")
        
    except Exception as e:
        print(f"✗ Error saving weights: {e}")
        return False

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
    

if __name__ == "__main__":
    main()