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
# run_benchmark.py - mPickle vs JSON benchmarking tool
#
# Features:
# - Multiple runs with different random seeds for statistical significance
# - Support for integers-only, floats-only, and mixed data types
# - Incremental testing from 1 to 2000 elements with efficient binary search
# - CSV export with detailed metadata
# - error handling and logging
#

import csv
import subprocess
import os
import random
from datetime import datetime
from pathlib import Path
import argparse
import tempfile

DEFAULT_RESULTS_FILE = './outputs/benchmark_results.csv'

def get_micropython_path():
    # Compute MicroPython path wrt repo root
    repo_root = Path(__file__).resolve().parent.parent
    micropython_path = repo_root.joinpath("firmware", "dev-scripts", "output", "micropython")
    return str(micropython_path)

def create_test_data_structure(size, data_structure_type="list", data_type="integer", seed=None):
    # Create test data data_structures of specified size and data type

    # Set seed for reproducibility
    if seed is not None:
        random.seed(seed)
    
    if data_structure_type == "list":
        if data_type == "integer":
            return [random.randint(0, 10000) for _ in range(size)]
        elif data_type == "float":
            return [random.uniform(0, 10000) for _ in range(size)]
        elif data_type == "mixed":
            return [random.choice([random.randint(0, 10000), random.uniform(0, 10000)]) for _ in range(size)]
        else:
            return list(range(size))  # Sequential for baseline
    
    elif data_structure_type == "dict":
        if data_type == "integer":
            return {f"key_{i}": random.randint(0, 10000) for i in range(size)}
        elif data_type == "float":
            return {f"key_{i}": random.uniform(0, 10000) for i in range(size)}
        elif data_type == "mixed":
            return {f"key_{i}": random.choice([random.randint(0, 10000), random.uniform(0, 10000)]) for i in range(size)}
        else:
            return {f"key_{i}": i for i in range(size)}  # Sequential for baseline
    
    else:
        raise ValueError(f"Unknown data_structure type: {data_structure_type}")

def convert_data_structure_to_str(data_structure):
    # Convert data_structure to a string representation
    if isinstance(data_structure, list):
        struct_str = str(data_structure)
    elif isinstance(data_structure, dict):
        struct_str = str(data_structure)
    else:
        struct_str = repr(data_structure)
    return struct_str

def create_mpickle_benchmark_script(data_structure, data_structure_name):
    #Create a MicroPython script to benchmark mPickle size

    struct_str = convert_data_structure_to_str(data_structure=data_structure)

    micropython_script = f'''import mpickle

# Test data_structure
{data_structure_name} = {struct_str}

# Benchmark mPickle
try:
    mpickle_data = mpickle.dumps({data_structure_name})
    mpickle_size = len(mpickle_data)
    print("SUCCESS:" + str(mpickle_size))
except Exception as e:
    print("ERROR:" + str(e))
'''
    return micropython_script

def create_json_benchmark_script(data_structure, data_structure_name):
    #Create a MicroPython script to benchmark JSON size

    struct_str = convert_data_structure_to_str(data_structure=data_structure)

    micropython_script = f'''import json

# Test data_structure
{data_structure_name} = {struct_str}

# Benchmark JSON
try:
    json_string = json.dumps({data_structure_name}).encode('utf-8')
    json_size = len(json_string)
    print("SUCCESS:" + str(json_size))
except Exception as e:
    print("ERROR:" + str(e))
'''
    return micropython_script

def run_micropython_benchmark(micropython_script, micropython_path):
    # Run the MicroPython benchmark script

    bechmarking_output = None

    # Store the MicroPython script in a temporary file
    with tempfile.NamedTemporaryFile(mode="w+", suffix=".py", prefix="mp_bench_", delete=True) as temp_script_file:

        # Write the script to the file
        temp_script_file.write(micropython_script)
        temp_script_file.seek(0)

        # Run the script using MicroPython
        try:
            result = subprocess.run([micropython_path, temp_script_file.name], 
                                capture_output=True, text=True, timeout=30)
            if result.stdout:
                lines = result.stdout.strip().split('\n')
                for line in lines:
                    if line.startswith('SUCCESS:'):
                        bechmarking_output = int(line.replace('SUCCESS:', ''))
                    elif line.startswith('ERROR:'):
                        print(f"MicroPython error: {line.replace('ERROR:', '')}")
            
            if result.stderr:
                print(f"MicroPython stderr: {result.stderr}")            
            
        except subprocess.TimeoutExpired:
            print("MicroPython benchmark timed out")
            print(f"Script: {temp_script_file.name}")
        except Exception as e:
            print(f"Error running MicroPython benchmark: {e}")
            print(f"Script: {temp_script_file.name}")

        # Delete script once completed
        temp_script_file.flush()

    return bechmarking_output
    
def benchmark(data_structure_type, data_type, seed, benchmark_size, micropython_path, run):
    result = None

    # Create data structure
    data_data_structure = create_test_data_structure(benchmark_size, data_structure_type, data_type, seed)
    data_structure_name = f"test_{data_structure_type}_{data_type}_{seed}_{benchmark_size}"

    # Benchmark JSON
    micropython_script = create_json_benchmark_script(data_data_structure, data_structure_name)
    json_size = run_micropython_benchmark(micropython_script, micropython_path)

    # Benchmark mPickle
    micropython_script = create_mpickle_benchmark_script(data_data_structure, data_structure_name)
    mpickle_size = run_micropython_benchmark(micropython_script, micropython_path)

    if json_size is not None and mpickle_size is not None:
        result = {
                'run': run,
                'size': benchmark_size,
                'data_structure_type': data_structure_type,
                'data_type': data_type,
                'seed': seed,
                'json_size': json_size,
                'mpickle_size': mpickle_size,
                'is_more_efficient': mpickle_size < json_size,
                'ratio': (mpickle_size / json_size) * 100 if json_size > 0 else 0,
                'savings': ((json_size - mpickle_size) / json_size) * 100 if json_size > 0 else 0
            }

    return result

def find_breakeven_point(run, data_structure_type, data_type, seed, min_size=1, max_size=2000, tolerance=1):
    #Find the point where mPickle becomes more efficient than JSON
    
    results = []
    micropython_path = get_micropython_path()
    
    print(f"Finding break-even point for {data_structure_type} ({data_type}) with seed {seed}...")
    
    # Test endpoints
    low = min_size
    high = max_size

    # Run benchmark for low-end size
    print(f"Running benchmark for {data_structure_type} ({data_type}) low-end size: {low} elements")
    benchmark_result_low = benchmark(data_structure_type=data_structure_type,
                                 data_type=data_type,
                                 seed=seed,
                                 benchmark_size=low, 
                                 micropython_path=micropython_path,
                                 run=run)
    if benchmark_result_low is not None:
        results.append(benchmark_result_low)
        json_size_low, mpickle_size_low = benchmark_result_low['json_size'], benchmark_result_low['mpickle_size']
    else:
        json_size_low, mpickle_size_low = None, None

    # Run benchmark for high-end size
    print(f"Running benchmark for {data_structure_type} ({data_type}) high-end size: {high} elements")
    benchmark_result_high= benchmark(data_structure_type=data_structure_type,
                                    data_type=data_type,
                                    seed=seed,
                                    benchmark_size=high, 
                                    micropython_path=micropython_path,
                                    run=run)
    if benchmark_result_high is not None:
        results.append(benchmark_result_high)
        json_size_high, mpickle_size_high = benchmark_result_high['json_size'], benchmark_result_high['mpickle_size']
    else:
        json_size_high, mpickle_size_high = None, None

    # Determine test strategy based on endpoints (binary search, if break-even not found yet, or key points)
    if (json_size_low is not None and mpickle_size_low is not None and 
        json_size_high is not None and mpickle_size_high is not None):
        
        if mpickle_size_low < json_size_low and mpickle_size_high < json_size_high:
            # Already efficient at both ends - test just key points
            test_sizes = [1, 5, 10, 25, 50, 100, 250, 500, 1000, 1500, 2000]
        elif mpickle_size_low >= json_size_low and mpickle_size_high >= json_size_high:
            # Not efficient in this range
            test_sizes = []
        else:
            # Binary search for break-even point
            test_sizes = []
            while high - low > tolerance:
                mid = (low + high) // 2
                test_sizes.append(mid)
                
                # Run benchmark for mid (binary search) size
                print(f"Running benchmark for {data_structure_type} ({data_type}) - binary search - size: {mid} elements")
                benchmark_result_mid= benchmark(data_structure_type=data_structure_type,
                                                 data_type=data_type,
                                                 seed=seed,
                                                 benchmark_size=mid, 
                                                 micropython_path=micropython_path,
                                 run=run)
                if benchmark_result_mid is not None:
                    json_size_mid, mpickle_size_mid = benchmark_result_mid['json_size'], benchmark_result_mid['mpickle_size']
                else:
                    json_size_mid, mpickle_size_mid = None, None
                
                if json_size_mid is not None and mpickle_size_mid is not None:
                    results.append(benchmark_result_mid)
                    
                    if mpickle_size_mid < json_size_mid:
                        high = mid
                    else:
                        low = mid
            breakeven_point = mid +1
            test_sizes += [x for x in range(breakeven_point*2)]
    else:
        # Default test sizes
        test_sizes = [1, 5, 10, 25, 50, 100, 250, 500, 1000, 1500, 2000]

    # Remove duplicates
    test_sizes = list(dict.fromkeys(test_sizes))

    # Test additional points
    for size in test_sizes:
        if size < min_size or size > max_size:
            continue
        
        # Skip if already tested
        if any(r['size'] == size and r['seed'] == seed for r in results):
            continue

        print(f"Running benchmark for {data_structure_type} ({data_type}) - additional - size: {size} elements")
        benchmark_result_additional = benchmark(data_structure_type=data_structure_type,
                                            data_type=data_type,
                                            seed=seed,
                                            benchmark_size=size, 
                                            micropython_path=micropython_path,
                                 run=run)
        if benchmark_result_additional is not None:
            results.append(benchmark_result_additional)
    
    return results

def run_benchmark_engine(num_runs=3, data_types=["integer"], min_size=1, max_size=2000):
    # Run benchmark with multiple runs and data types.
    # Test lists and dicts
    
    # Empty results
    all_results = []
    start_time = datetime.now()
    
    print(f"Starting benchmark at {start_time}")
    print(f"Number of runs: {num_runs}")
    print(f"Data types: {', '.join(data_types)}")
    print("="*80)
    
    for run in range(1, num_runs + 1):
        print(f"\nRun {run}/{num_runs}")
        
        for data_type in data_types:
            print(f"Testing {data_type} data...")
            
            # Use different seed for each run
            seed = 42 + run * 100
            
            # Test both list and dict data_structures
            for data_structure_type in ["list", "dict"]:
                results = find_breakeven_point(run, data_structure_type, data_type, seed, min_size, max_size)
                all_results.extend(results)
    
    end_time = datetime.now()
    duration = end_time - start_time
    
    print(f"\nBenchmark completed at {end_time}")
    print(f"Total duration: {duration}")
    print(f"Total measurements: {len(all_results)}")
    print("="*80)
    
    return all_results

def export_results_to_csv(results, filename="benchmarks/outputs/benchmark_results.csv"):
    # Export results to CSV file with metadata
    
    if not results:
        print("No results to export")
        return
    
    # Ensure outputs directory exists
    out_path = Path(filename)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    
    print(f"Exporting {len(results)} results to {filename}...")
    
    # Add metadata header
    metadata = {
        'timestamp': datetime.now().isoformat(),
        'micropython_path': get_micropython_path(),
        'description': 'mPickle vs JSON benchmark with multiple runs and data types'
    }
    
    with open(filename, 'w', newline='') as csvfile:
        # Write metadata as comments
        csvfile.write(f"# mPickle Benchmark Results\n")
        csvfile.write(f"# Generated: {metadata['timestamp']}\n")
        csvfile.write(f"# MicroPython Path: {metadata['micropython_path']}\n")
        csvfile.write(f"# Description: {metadata['description']}\n")
        csvfile.write(f"#\n")
        
        fieldnames = ['run', 'size', 'data_structure_type', 'data_type', 'seed', 'json_size',
                     'mpickle_size', 'is_more_efficient', 'ratio', 'savings']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for result in results:
            writer.writerow(result)
    
    print(f"Results successfully exported to {filename}")

def analyze_results(results):
    # Analyze and summarize benchmark results
    
    print("\n" + "="*80)
    print("BENCHMARK ANALYSIS")
    print("="*80)
    
    # Group results by data type and data_structure type
    from collections import defaultdict
    grouped_results = defaultdict(list)
    
    for result in results:
        key = (result['data_type'], result['data_structure_type'])
        grouped_results[key].append(result)
    
    for (data_type, data_structure_type), data_structure_results in sorted(grouped_results.items()):
        print(f"\n{data_type.upper()} {data_structure_type.upper()}:")
        print("-" * 40)
        
        # Find break-even point
        efficient_points = [r for r in data_structure_results if r['is_more_efficient']]
        
        if efficient_points:
            first_efficient = min(efficient_points, key=lambda x: x['size'])
            max_savings = max(efficient_points, key=lambda x: x['savings'])
            avg_savings = sum(r['savings'] for r in efficient_points) / len(efficient_points)
            
            print(f"  Break-even Point: {first_efficient['size']} elements")
            print(f"  Savings at Break-even: {first_efficient['savings']:.1f}%")
            print(f"  Maximum Savings: {max_savings['savings']:.1f}% at {max_savings['size']} elements")
            print(f"  Average Savings: {avg_savings:.1f}%")
            print(f"  Total Measurements: {len(data_structure_results)}")
        else:
            print(f"  mPickle never becomes more efficient")
            print(f"  Total Measurements: {len(data_structure_results)}")
    
    # Overall statistics
    print(f"\nOVERALL STATISTICS:")
    print(f"  Total Data Points: {len(results)}")
    print(f"  Unique Configurations: {len(grouped_results)}")
    
    # Data type comparison
    data_type_stats = defaultdict(list)
    for result in results:
        data_type_stats[result['data_type']].append(result)
    
    print(f"\nDATA TYPE COMPARISON:")
    for data_type, dt_results in sorted(data_type_stats.items()):
        efficient_count = sum(1 for r in dt_results if r['is_more_efficient'])
        avg_savings = sum(r['savings'] for r in dt_results if r['is_more_efficient']) / max(1, efficient_count)
        print(f"  {data_type}: {efficient_count}/{len(dt_results)} efficient points, avg {avg_savings:.1f}% savings")

def main():

    parser = argparse.ArgumentParser(description="mPickle vs JSON benchmarking tool")
    parser.add_argument('--runs',
                        type=int,
                        default=3, 
                        help='Number of benchmarking runs (default: 3)')
    parser.add_argument('--data_types',
                        nargs='+', 
                        default=["integer", "float", "mixed", "sequential"],
                        help='Data types to test: integer, float, mixed, sequential (default: all)')
    parser.add_argument('--min_size',
                        type=int,
                        default=1,
                        help='Minimum elements in benchmarking data data_structure (default: 1)')
    parser.add_argument('--max_size',
                        type=int,
                        default=2000,
                        help='Maximum elements in benchmarking data data_structure (default: 2000)')
    parser.add_argument('--results_file',
                        type=str,
                        default=DEFAULT_RESULTS_FILE,
                        help='Output file for results')
    
    args = parser.parse_args()
    
    # Run benchmark
    results = run_benchmark_engine(
        num_runs=args.runs,
        data_types=args.data_types,
        min_size=args.min_size,
        max_size=args.max_size
    )
    
    if results:
        # Export results
        export_results_to_csv(results, args.results_file)
        
        # Analyze results
        analyze_results(results)
        
        

if __name__ == "__main__":
    main()