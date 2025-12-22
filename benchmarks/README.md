# mPickle vs JSON MicroPython Benchmark <!-- omit in toc -->

This guide provides documentation for the mPickle vs JSON benchmarking suite. The benchmarks compare serialization efficiency between mPickle and JSON across various data types, structure sizes, and multiple runs for statistical significance.

## Table of Content <!-- omit in toc -->
- [Benchmark Objectives](#benchmark-objectives)
- [Directory Structure](#directory-structure)
- [Quick Start](#quick-start)
  - [1. Run the Benchmark](#1-run-the-benchmark)
  - [2. Generate Visualizations](#2-generate-visualizations)
  - [3. View Results](#3-view-results)
- [Command Line Options](#command-line-options)
  - [run\_benchmark.py Options](#run_benchmarkpy-options)
    - [Standard Benchmark (Recommended)](#standard-benchmark-recommended)
    - [Custom Benchmark (5 runs, integers only)](#custom-benchmark-5-runs-integers-only)
    - [Large Scale Benchmark (1-5000 elements)](#large-scale-benchmark-1-5000-elements)
    - [Focused Benchmark (floats and mixed data)](#focused-benchmark-floats-and-mixed-data)
    - [Custom Output File](#custom-output-file)
  - [plot\_results.py Options](#plot_resultspy-options)
    - [Default Visualization](#default-visualization)
    - [Custom Input File](#custom-input-file)
    - [PNG Format Output](#png-format-output)
    - [Custom Output Directory](#custom-output-directory)
- [Data Types Explained](#data-types-explained)
  - [Integer Data](#integer-data)
  - [Float Data](#float-data)
  - [Mixed Data](#mixed-data)
  - [Sequential Data](#sequential-data)
- [Benchmark Methodology (Reported in Manuscript)](#benchmark-methodology-reported-in-manuscript)
  - [Command Executed](#command-executed)
  - [Efficient Binary Search Algorithm](#efficient-binary-search-algorithm)
  - [Multiple Runs for Statistical Significance](#multiple-runs-for-statistical-significance)
  - [Structure Types Tested](#structure-types-tested)
  - [MicroPython Implementation Details](#micropython-implementation-details)
- [Metrics Collected](#metrics-collected)
- [Expected Results](#expected-results)
  - [Typical Break-Even Points](#typical-break-even-points)
  - [Typical Space Savings](#typical-space-savings)
- [Visualization Guide](#visualization-guide)
  - [Size Comparison Plot](#size-comparison-plot)
  - [Space Savings Plot](#space-savings-plot)
  - [Efficiency Ratio Plot](#efficiency-ratio-plot)
- [Output Files Description](#output-files-description)
  - [`benchmark_results.csv`](#benchmark_resultscsv)
  - [Visualization Plots](#visualization-plots)
  - [`breakeven_points.csv`](#breakeven_pointscsv)
  - [Console Output](#console-output)


## Benchmark Objectives

1. **Identify break-even points**: Determine when mPickle becomes more efficient than JSON
2. **Compare data types**: Test integers, floats, mixed, and sequential data
3. **Statistical significance**: Multiple runs with different random seeds
4. **Results analysis**: Detailed metrics and visualizations

## Directory Structure

```
benchmarks/
├── run_benchmark.py          # Main benchmark script
├── plot_results.py           # Visualization script
└── README.md                 # This documentation
```

## Quick Start

### 1. Run the Benchmark

Execute the benchmark script to compare mPickle and JSON serialization performance:

```bash
python3 benchmarks/run_benchmark.py
```

This command runs the benchmark with default settings:
- 3 runs with different random seeds for statistical significance
- Tests all data types: integer, float, mixed, and sequential
- Tests structure sizes from 1 to 2000 elements
- Tests both list and dictionary data structures
- Outputs detailed progress information to the console
- Saves results to `benchmarks/outputs/benchmark_results.csv`

### 2. Generate Visualizations

Create visual representations of the benchmark results:

```bash
python3 benchmarks/plot_results.py
```

This command generates the following visualization files:
- `benchmarks/outputs/size_comparison_list.pdf` - Size comparison for list structures
- `benchmarks/outputs/size_comparison_dict.pdf` - Size comparison for dictionary structures
- `benchmarks/outputs/space_savings_list.pdf` - Space savings analysis for lists
- `benchmarks/outputs/space_savings_dict.pdf` - Space savings analysis for dictionaries
- `benchmarks/outputs/efficiency_ratio_list.pdf` - Efficiency ratio for lists
- `benchmarks/outputs/efficiency_ratio_dict.pdf` - Efficiency ratio for dictionaries
- `benchmarks/outputs/breakeven_points.csv` - Summary table of break-even points

The script also displays a summary of identified break-even points in the console.

### 3. View Results

After running the benchmark and visualization scripts, you can examine the outputs:

- **CSV Data**: `benchmarks/outputs/benchmark_results.csv` - Contains all raw benchmark measurements with metadata header
- **Visualization Plots**: PDF files in `benchmarks/outputs/` directory showing performance comparisons
- **Summary Analysis**: Console output from both scripts providing key insights and statistics

## Command Line Options

### run_benchmark.py Options

**Basic Usage:**
```bash
python3 benchmarks/run_benchmark.py [OPTIONS]
```

**Available Options:**

| Option | Description | Default Value |
|--------|-------------|---------------|
| `--runs RUNS` | Number of benchmark runs with different random seeds | 3 |
| `--data_types` | Data types to test (space-separated): integer, float, mixed, sequential | integer float mixed sequential |
| `--min_size` | Minimum number of elements in data structures | 1 |
| `--max_size` | Maximum number of elements in data structures | 2000 |
| `--results_file` | Output file path for benchmark results | ./outputs/benchmark_results.csv |

**Examples:**

#### Standard Benchmark (Recommended)
Runs complete benchmark with all data types and default settings:
```bash
python3 benchmarks/run_benchmark.py
```

#### Custom Benchmark (5 runs, integers only)
Tests only integer data with 5 runs for better statistical analysis:
```bash
python3 benchmarks/run_benchmark.py --runs 5 --data_types integer
```

#### Large Scale Benchmark (1-5000 elements)
Extends testing to larger data structures up to 5000 elements:
```bash
python3 benchmarks/run_benchmark.py --max_size 5000
```

#### Focused Benchmark (floats and mixed data)
Tests only float and mixed data types with 4 runs:
```bash
python3 benchmarks/run_benchmark.py --data_types float mixed --runs 4
```

#### Custom Output File
Save results to a specific file path:
```bash
python3 benchmarks/run_benchmark.py --results_file ./custom_results.csv
```

### plot_results.py Options

**Basic Usage:**
```bash
python3 benchmarks/plot_results.py [OPTIONS]
```

**Available Options:**

| Option | Description | Default Value |
|--------|-------------|---------------|
| `--results_file` | Input results file path | ./outputs/benchmark_results.csv |
| `--output_dir` | Output directory for generated plots | ./outputs/ |
| `--plot_format` | Format for generated plots (pdf, png, etc.) | pdf |

**Examples:**

#### Default Visualization
Generate all plots with default settings:
```bash
python3 benchmarks/plot_results.py
```

#### Custom Input File
Use results from a custom benchmark run:
```bash
python3 benchmarks/plot_results.py --results_file ./custom_results.csv
```

#### PNG Format Output
Generate plots in PNG format instead of PDF:
```bash
python3 benchmarks/plot_results.py --plot_format png
```

#### Custom Output Directory
Save plots to a specific directory:
```bash
python3 benchmarks/plot_results.py --output_dir ./my_plots/
```

## Data Types Explained

This benchmark evaluates mPickle against JSON in scenarios where simple data structures, like lists and dictionaries, must be serialized.

### Integer Data
- Random integers uniformly distributed in [0; 10000)
- Tests serialization of whole numbers
- Most compact representation among numeric types

### Float Data
- Random floating-point numbers uniformly distributed from [0.0; 10000.0)
- Tests serialization of decimal numbers
- Larger footprint than integers due to decimal representation

### Mixed Data
- Randomly alternating integers and floats drawn from the same ranges
- Tests serialization of heterogeneous numeric data
- Simulates real-world scenarios with mixed numeric types

### Sequential Data
- Sequential integer numbers (values from 0 to 10000)
- Baseline for comparison with highly compressible pattern
- Tests serialization of predictable, ordered sequences

## Benchmark Methodology (Reported in Manuscript)

### Command Executed
```sh
python3 run_benchmark.py --runs 1000 --results_file ./outputs_1000/benchmark_results.csv
python3 plot_results.py --results_file ./outputs_1000/benchmark_results.csv --output_dir ./outputs_1000
```
The directory with the results is available at `./outputs_1000`.

### Efficient Binary Search Algorithm

To speed up the benchmarking process, we apply a binary search strategy to faster identify the break-even point:

1. **Test Endpoints**: Evaluate size 1 and size 2000 first to establish baseline performance
2. **Determine Strategy**:
   - If mPickle is efficient at both ends -> test key points for detailed analysis
   - If break-even is detected -> perform binary search to pinpoint the exact location
   - If mPickle is never efficient -> perform limited testing
3. **Binary Search Implementation**: Starting from the extremes (1 and 2000 elements), we measure serialized sizes at both ends to establish which format is smaller. We then evaluate the midpoint and iteratively narrow the search interval by keeping the half in which the break-even point can still lie:
   - Keep lower half if JSON is smaller at lower bound while mPickle is smaller at midpoint
   - Keep upper half if mPickle is smaller at midpoint while JSON is smaller at upper bound
4. **Termination**: Stop the search when lower and upper bounds collapse to a single size, which is reported as the break-even point
5. **Detailed Exploration**: Once the break-even point is identified, evaluate all data structures with sizes ranging from 1 up to twice the break-even-point value to explore the transition more clearly

### Multiple Runs for Statistical Significance

- Each run uses a different random seed following the pattern: `seed = 42 + 100 * run_id`
- This ensures reproducibility while providing statistical significance
- Results are averaged across runs to determine break-even points
- The default configuration uses 3 runs, but can be increased for more robust statistics

### Structure Types Tested

- **Lists**: Ordered sequences `[1, 2, 3, ...]`
- **Dictionaries**: Key-value pairs `{"key_1": 1, "key_2": 2, ...}` where keys are named `key_{id}` with `id` denoting the element index

### MicroPython Implementation Details

All serialization experiments are carried out on MicroPython (UNIX port) to ensure a fair comparison:

- **JSON Implementation**: MicroPython's JSON `dump` function does not allow setting indentation, so output is generated without pretty-printing (no additional whitespace)
- **Encoding**: JSON strings are UTF-8 encoded for consistent byte size measurement
- **mPickle Implementation**: Uses mPickle implementation optimized for embedded systems
- **Fair Comparison**: Both serializers run in the same MicroPython environment with identical data structures

## Metrics Collected

| Metric | Description | Formula |
|--------|-------------|---------|
| `size` | Number of elements in structure | - |
| `json_size` | JSON serialization size in bytes | `len(json.dumps(data).encode('utf-8'))` |
| `mpickle_size` | mPickle serialization size in bytes | `len(mpickle.dumps(data))` |
| `is_more_efficient` | Whether mPickle is more efficient | `mpickle_size < json_size` |
| `ratio` | mPickle size as % of JSON size | `(mpickle_size / json_size) * 100` |
| `savings` | Space savings percentage | `((json_size - mpickle_size) / json_size) * 100` |

## Expected Results

### Typical Break-Even Points

- **Integer Lists**: ~14 elements
- **Float Lists**: ~10-15 elements  
- **Mixed Lists**: ~12-16 elements
- **Sequential Lists**: ~8-12 elements
- **Integer Dicts**: ~9 elements
- **Float Dicts**: ~8-12 elements
- **Mixed Dicts**: ~10-14 elements
- **Sequential Dicts**: ~6-10 elements

### Typical Space Savings

Based on our experiments, the break-even point typically occurs:
- Between 5 and 20 elements for lists
- Between 5 and 10 elements for dictionaries

This indicates that mPickle becomes more space-efficient than JSON already for small data structures, and the efficiency gap increases for larger data structures.

Space savings vary by data type:
- **Lists**: mPickle achieves space savings up to 54% when serializing lists of sequential integer numbers, while up to 9% for lists of floating-point numbers
- **Dictionaries**: Savings are generally smaller than for lists, since dictionaries also require storing keys in addition to values

Size-based savings patterns:
- **Small data (1-10 elements)**: JSON more efficient (negative savings)
- **Medium data (10-100 elements)**: 5-30% savings
- **Large data (100-2000 elements)**: 20-55% savings

## Visualization Guide

### Size Comparison Plot
- Shows actual byte sizes for JSON vs mPickle
- Different colors for different data types
- Solid lines = mPickle, dotted lines = JSON
- Scatter points mark break-even locations

### Space Savings Plot
- Shows percentage space savings
- Positive values = mPickle more efficient
- Negative values = JSON more efficient
- Zero line indicates break-even point

### Efficiency Ratio Plot
- Shows mPickle size as % of JSON size
- Values < 100% = mPickle more efficient
- Values > 100% = JSON more efficient
- 100% line indicates equivalence

## Output Files Description

### `benchmark_results.csv`
- Contains all raw benchmark measurements in CSV format
- Includes metadata header with timestamp, MicroPython path, and description
- Each row represents a single benchmark measurement with the following columns:
  - `run`: Benchmark run number (1-N)
  - `size`: Number of elements in the tested data structure
  - `data_structure_type`: Type of data structure (list or dict)
  - `data_type`: Type of data (integer, float, mixed, or sequential)
  - `seed`: Random seed used for reproducibility
  - `json_size`: Serialization size in bytes using JSON
  - `mpickle_size`: Serialization size in bytes using mPickle
  - `is_more_efficient`: Boolean indicating if mPickle is more efficient
  - `ratio`: mPickle size as percentage of JSON size
  - `savings`: Space savings percentage when using mPickle

### Visualization Plots

The visualization script generates multiple plot files in PDF format:

- **size_comparison_list.pdf**: Compares serialization sizes for list structures across all data types, showing when mPickle becomes more efficient than JSON
- **size_comparison_dict.pdf**: Compares serialization sizes for dictionary structures across all data types
- **space_savings_list.pdf**: Shows percentage space savings for list structures on a logarithmic scale
- **space_savings_dict.pdf**: Shows percentage space savings for dictionary structures
- **efficiency_ratio_list.pdf**: Displays mPickle size as percentage of JSON size for lists
- **efficiency_ratio_dict.pdf**: Displays mPickle size as percentage of JSON size for dictionaries

All plots include:
- Different colored lines for each data type (integer, float, mixed, sequential)
- Solid lines for JSON, dotted lines for mPickle
- Scatter points marking break-even locations where mPickle becomes more efficient
- Zoom inset showing early break-even points in detail
- Grid lines and proper labeling for easy interpretation

### `breakeven_points.csv`
- Summary table identifying when mPickle becomes more efficient than JSON
- Contains one row per data type and structure type combination
- Includes break-even size, savings percentages, and statistical summaries

### Console Output

During benchmark execution:
- Real-time progress updates showing current test being executed
- Information about break-even point detection and binary search progress
- Timing information and measurement counts

After benchmark completion:
- Detailed analysis summary by data type and structure type
- break-even points identified for each configuration
- Space savings statistics including minimum, maximum, and average values
- Overall performance comparison across all tested configurations
- Best and worst performing configurations identified