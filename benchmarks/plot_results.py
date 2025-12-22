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
# plot_results.py - Plot the results between mPickle and JSON benchmarking
#

import matplotlib.pyplot as plt
import numpy as np
import os
import argparse
from pathlib import Path
import pandas as pd
from collections import OrderedDict
import math

DEFAULT_RESULTS_FILE = './outputs/benchmark_results.csv'
DEFAULT_OUTPUT_DIR = './outputs/'

def load_results(filename=DEFAULT_RESULTS_FILE):
    # Load results from CSV file
    
    if not os.path.exists(filename):
        print(f"Error: {filename} not found")
        return None, None
    
    # Find the header line (skip metadata above it)
    header_row = None
    with open(filename, "r", encoding="utf-8") as f:
        for i, line in enumerate(f):
            if line.startswith("run,"):
                header_row = i
                break
    
    if header_row is None:
        raise ValueError("Could not find CSV header line starting with 'run,'")

    # Read CSV from the header onward
    df_raw = pd.read_csv(filename, skiprows=header_row)

    # Type conversions (match your original parsing)
    int_cols = ["run", "size", "seed", "json_size", "mpickle_size"]
    for c in int_cols:
        df_raw[c] = pd.to_numeric(df_raw[c], errors="raise").astype("int64")

    df_raw["ratio"] = pd.to_numeric(df_raw["ratio"], errors="raise")
    df_raw["savings"] = pd.to_numeric(df_raw["savings"], errors="raise")

    df_raw["is_more_efficient"] = (
        df_raw["is_more_efficient"]
        .astype(str).str.strip().str.lower()
        .map({"true": True, "false": False})
    )
    
    # Sorting
    df_raw = df_raw.sort_values(
        ["run", "data_structure_type", "data_type", "size"],
        kind="mergesort"  # stable sort (nice when ties exist)
    ).reset_index(drop=True)

    # Aggregate over runs
    df_agg = aggregate_over_runs(df_raw)

    # Build results_by_type: key = (data_type, data_structure_type)
    results_by_type = OrderedDict()
    for row in df_raw.to_dict(orient="records"):
        key = (row["data_type"], row["data_structure_type"])
        results_by_type.setdefault(key, []).append(row)

    return results_by_type, df_raw, df_agg

def aggregate_over_runs(df: pd.DataFrame) -> pd.DataFrame:
    group_cols = ["data_structure_type", "data_type", "size"]

    agg = (
        df.groupby(group_cols, as_index=False)
          .agg(
              n_runs=("run", "nunique"),
              json_size_mean=("json_size", "mean"),
              json_size_std=("json_size", "std"),
              mpickle_size_mean=("mpickle_size", "mean"),
              mpickle_size_std=("mpickle_size", "std"),
              # fraction of runs where True (0..1)
          )
          .sort_values(group_cols, kind="mergesort")
          .reset_index(drop=True)
    )

    agg["is_more_efficient"] = agg["mpickle_size_mean"] < agg["json_size_mean"]

    return agg

def plot_size_comparison(df_agg_orig, output_dir, file_suffix="dict", plot_format='pdf'):
    #Plot size comparison between JSON and mPickle for all data types

    #Prepare output
    size_comparison_file = Path(output_dir).joinpath(f"size_comparison_{file_suffix}.{plot_format}")
    size_comparison_file.parent.mkdir(parents=True, exist_ok=True)
    
    fig = plt.figure(figsize=(10, 7.5))
    ax = fig.add_subplot(111)
    
    colors = {
        'integer': 'blue',
        'float': 'green',
        'mixed': 'purple',
        'sequential': 'orange'
    }
    
    breakeven_points = {}
    max_inset_x = 0
    max_inset_y = 0
    
    df_agg = df_agg_orig.copy()
    df_agg['mpickle_size_mean'] /= 1000.0
    df_agg['json_size_mean'] /= 1000.0

    results_by_type = {
    (data_type, data_structure_type): (
        g.drop(columns=["data_type", "data_structure_type"])
         .sort_values("size")  # optional
         .to_dict("records")
    )
        for (data_type, data_structure_type), g in df_agg.groupby(["data_type", "data_structure_type"])
    }

    for (data_type, data_structure_type), results in results_by_type.items():
        sizes = [r['size'] for r in results]
        json_sizes = [r['json_size_mean'] for r in results]
        mpickle_sizes = [r['mpickle_size_mean'] for r in results]
        
        color = colors.get(data_type, 'gray')
        
        label_json = f'JSON ({data_type} {data_structure_type})'
        label_mpickle = f'mPickle ({data_type} {data_structure_type})'
        
        ax.plot(sizes, json_sizes, color=color, linestyle=":",
                label=label_json, linewidth=2)
        ax.plot(sizes, mpickle_sizes, color=color, linestyle='-',
                label=label_mpickle, linewidth=2)
        

        # Find and mark crossover point
        efficient_points = [r for r in results if r['is_more_efficient']]
        if efficient_points:
            crossover = min(efficient_points, key=lambda x: x['size'])
            breakeven_points[(data_type, data_structure_type)] = crossover['size']
            ax.scatter([crossover['size']], [crossover['mpickle_size_mean']],
                       color=color, marker='o', s=100, edgecolors='black')
    

    # Create inset zoom
    axins = ax.inset_axes([0.1, 0.55, 0.35, 0.35])  # [x, y, width, height] in axes coordinates

    for (data_type, data_structure_type), results in results_by_type.items():
        sizes = [r['size'] for r in results]
        json_sizes = [r['json_size_mean'] for r in results]
        mpickle_sizes = [r['mpickle_size_mean'] for r in results]
        
        color = colors.get(data_type, 'gray')
        
        axins.plot(sizes, json_sizes, color=color, linestyle='-', linewidth=2)
        axins.plot(sizes, mpickle_sizes, color=color, linestyle=':', linewidth=2)
        
        # Mark crossover points in inset
        efficient_points = [r for r in results if r['is_more_efficient']]
        if efficient_points:
            crossover = min(efficient_points, key=lambda x: x['size'])
            axins.scatter([crossover['size']], [crossover['mpickle_size_mean']],
                        color=color, marker='o', s=50, edgecolors='black')
            if max_inset_x < crossover['size']:
                max_inset_x = crossover['size']
            if max_inset_y < crossover['mpickle_size_mean']:
                max_inset_y = crossover['mpickle_size_mean']


    # Set zoom region (adjust these values based on your data)
    x1, x2, y1, y2 = 1, math.ceil(max_inset_x*1.1), 0, max_inset_y*1.1  # Focus on early crossover points
    axins.set_xlim(x1, x2)
    axins.set_ylim(y1, y2)
    axins.grid(True, alpha=0.3)
    axins.tick_params(axis='both', which='major', labelsize=14)

    # Draw rectangle and connector lines to show zoom region
    ax.indicate_inset_zoom(axins, edgecolor="black")

    # ax.set_title('mPickle vs JSON Size Comparison by Data Type (1-2000 elements)', fontsize=18)
    ax.set_xlabel('Number of Elements', fontsize=18)
    ax.set_ylabel('Serialization Size (kB)', fontsize=18)
    ax.tick_params(axis='both', which='major', labelsize=16)
    ax.grid(True, alpha=0.3)
    ax.legend(fontsize=14, loc='lower right')
    
    plt.tight_layout()
    plt.savefig(size_comparison_file, dpi=600, bbox_inches='tight')
    plt.close()
    
    return breakeven_points, size_comparison_file

def plot_space_savings(df_agg_orig, output_dir, file_suffix='dict', plot_format='pdf'):
    # Plot space savings percentage by data type

    #Prepare output
    space_savings_file = Path(output_dir).joinpath(f"space_savings_{file_suffix}.{plot_format}")
    space_savings_file.parent.mkdir(parents=True, exist_ok=True)

    fig = plt.figure(figsize=(8, 5))
    ax = fig.add_subplot(111)

    df_agg = df_agg_orig.copy()

    df_agg['ratio'] = df_agg['mpickle_size_mean'] / df_agg['json_size_mean']
    df_agg['is_more_efficient'] = df_agg['ratio'] < 1.0
    df_agg['savings'] = (1.0 - df_agg['ratio'])*100.0

    results_by_type = {
    (data_type, data_structure_type): (
        g.drop(columns=["data_type", "data_structure_type"])
         .sort_values("size")  # optional
         .to_dict("records")
    )
        for (data_type, data_structure_type), g in df_agg.groupby(["data_type", "data_structure_type"])
    }
    
    colors = {
        'integer': 'blue',
        'float': 'green',
        'mixed': 'purple',
        'sequential': 'orange'
    }
    
    for (data_type, structure_type), results in results_by_type.items():
        sizes = [r['size'] for r in results]
        savings = [r['savings'] for r in results]
        
        color = colors.get(data_type, 'gray')
        
        label = f'{data_type} {structure_type}'
        plt.semilogx(sizes, savings, color=color, marker="o",
                label=label, linewidth=2, markersize=5)
    
    # ax.set_title('mPickle Space Savings vs JSON - by Data Type', fontsize=16)
    ax.set_xlabel('Number of Elements', fontsize=18)
    ax.set_ylabel('Space Savings (%)', fontsize=18)
    ax.tick_params(axis='both', which='major', labelsize=16)
    ax.set_ylim(top=100)
    plt.grid(True, alpha=0.3)
    plt.legend(fontsize=10, loc='lower right')
    plt.tight_layout()
    
    # Add zero line
    ax.axhline(y=0, color='black', linestyle='--', alpha=0.5)
    
    plt.savefig(space_savings_file, dpi=600, bbox_inches='tight')
    plt.close()

    return space_savings_file

def plot_efficiency_ratio(df_agg_orig, output_dir, file_suffix='dict', plot_format='pdf'):
    # Plot efficiency ratio (mPickle size as % of JSON size) by data type

    #Prepare output
    efficiency_ratio_file = Path(output_dir).joinpath(f"efficiency_ratio_{file_suffix}.{plot_format}")
    efficiency_ratio_file.parent.mkdir(parents=True, exist_ok=True)
    
    fig = plt.figure(figsize=(8, 5))
    ax = fig.add_subplot(111)
    
    colors = {
        'integer': 'blue',
        'float': 'green',
        'mixed': 'purple',
        'sequential': 'orange'
    }

    df_agg = df_agg_orig.copy()
    df_agg['mpickle_size_mean'] /= 1000.0
    df_agg['json_size_mean'] /= 1000.0
    df_agg['ratio'] = df_agg['mpickle_size_mean'] / df_agg['json_size_mean']

    results_by_type = {
    (data_type, data_structure_type): (
        g.drop(columns=["data_type", "data_structure_type"])
         .sort_values("size")  # optional
         .to_dict("records")
    )
        for (data_type, data_structure_type), g in df_agg.groupby(["data_type", "data_structure_type"])
    }

    for (data_type, structure_type), results in results_by_type.items():
        sizes = [r['size'] for r in results]
        ratios = [r['ratio'] for r in results]
        
        color = colors.get(data_type, 'gray')
        
        label = f'{data_type} {structure_type}'
        ax.semilogx(sizes, ratios, color=color, marker='o',
                label=label, linewidth=2, markersize=5)
    
    ax.set_title('mPickle Efficiency Ratio vs JSON by Data Type (1-2000 elements)', fontsize=16)
    ax.set_xlabel('Number of Elements', fontsize=12)
    ax.set_ylabel('mPickle Size / JSON Size', fontsize=12)
    plt.grid(True, alpha=0.3)
    plt.legend(fontsize=12, loc='upper right')
    plt.tight_layout()
    
    # Add 100% line (where mPickle = JSON)
    ax.axhline(y=1, color='black', linestyle='--', alpha=0.5, label='mPickle = JSON')
    
    
    plt.savefig(efficiency_ratio_file, dpi=600, bbox_inches='tight')
    plt.close()
    
    return efficiency_ratio_file

def create_summary_table(df_agg_orig, output_dir):
    # Create a summary table of key findings
    breakeven_points_file = Path(output_dir).joinpath(f"breakeven_points.csv")
    breakeven_points_file.parent.mkdir(parents=True, exist_ok=True)

    df_agg = df_agg_orig.copy()
    df_agg['ratio'] = df_agg['mpickle_size_mean'] / df_agg['json_size_mean']
    df_agg['is_more_efficient'] = df_agg['ratio'] < 1.0
    df_agg['savings'] = (1.0 - df_agg['ratio'])*100.0
    
    results_by_type = {
        (data_type, data_structure_type): (
            g.drop(columns=["data_type", "data_structure_type"])
            .sort_values("size")  # optional
            .to_dict("records")
        )
        for (data_type, data_structure_type), g in df_agg.groupby(["data_type", "data_structure_type"])
    }
    
    print(df_agg.head(10))
    print("\n" + "="*80)
    print("BENCHMARK SUMMARY")
    print("="*80)
    
    all_breakeven_points = {}
    all_max_savings = {}
    all_avg_savings = {}
    breakeven_data = []  # New: collect crossover data for CSV
    
    for (data_type, structure_type), results in results_by_type.items():
        efficient_points = [r for r in results if r['is_more_efficient']]
        
        if efficient_points:
            crossover = min(efficient_points, key=lambda x: x['size'])
            max_savings = max(efficient_points, key=lambda x: x['savings'])
            avg_savings = np.mean([r['savings'] for r in efficient_points])
            
            all_breakeven_points[(data_type, structure_type)] = crossover
            all_max_savings[(data_type, structure_type)] = max_savings
            all_avg_savings[(data_type, structure_type)] = avg_savings
            
            # New: add to crossover data
            breakeven_data.append({
                'data_type': data_type,
                'structure_type': structure_type,
                'breakeven_size': crossover['size'],
                'savings_at_crossover': crossover['savings'],
                'max_savings': max_savings['savings'],
                'max_savings_size': max_savings['size'],
                'avg_savings': avg_savings,
                'num_data_points': len(results)
            })
            
            print(f"\n{data_type.upper()} {structure_type.upper()}:")
            print(f"  Crossover Point: {crossover['size']} elements")
            print(f"  Savings at Crossover: {crossover['savings']:.1f}%")
            print(f"  Maximum Savings: {max_savings['savings']:.1f}% at {max_savings['size']} elements")
            print(f"  Average Savings: {avg_savings:.1f}%")
            print(f"  Data Points: {len(results)}")
        else:
            print(f"\n{data_type.upper()} {structure_type.upper()}:")
            print(f"  mPickle never becomes more efficient")
            print(f"  Data Points: {len(results)}")
    
    # New: save crossover points to CSV
    if breakeven_data:
        breakeven_df = pd.DataFrame(breakeven_data)
        breakeven_df.to_csv(breakeven_points_file, index=False)
        print(f"\nCrossover points saved to: {breakeven_points_file}")
    
    # Overall comparison
    print(f"\nOVERALL COMPARISON:")
    print(f"  Total Configurations: {len(results_by_type)}")
    print(f"  Efficient Configurations: {len(all_breakeven_points)}")
    
    # Find best and worst performers
    if all_max_savings:
        best_config = max(all_max_savings.items(), key=lambda x: x[1]['savings'])
        worst_config = min(all_max_savings.items(), key=lambda x: x[1]['savings'])
        
        print(f"\nBEST PERFORMER:")
        print(f"  {best_config[0][0]} {best_config[0][1]}: {best_config[1]['savings']:.1f}% max savings")
        
        print(f"\nWORST PERFORMER:")
        print(f"  {worst_config[0][0]} {worst_config[0][1]}: {worst_config[1]['savings']:.1f}% max savings")
    
    print("\n" + "="*80)

    return breakeven_points_file

def main():
    parser = argparse.ArgumentParser(description="mPickle vs JSON benchmarking tool")
    parser.add_argument('--results_file',
                        type=str,
                        default=DEFAULT_RESULTS_FILE,
                        help='Input Results file')
    
    parser.add_argument('--output_dir',
                        type=str,
                        default=DEFAULT_OUTPUT_DIR,
                        help='Output directory for plots')
    
    parser.add_argument('--plot_format',
                        type=str,
                        default="pdf",
                        help='Plot format (e.g., pdf, png)')
    
    args = parser.parse_args()
    
    # Load results
    results_by_type, df_raw, df_agg = load_results(filename=args.results_file)
    
    if df_agg.size <= 0:
        print("No results found. Please run run_benchmark.py first.")
        return
    
    # Create plots
    breakeven_points, size_comparison_dict_file = plot_size_comparison(df_agg[df_agg['data_structure_type']=='dict'], args.output_dir, file_suffix='dict', plot_format=args.plot_format)
    breakeven_points, size_comparison_list_file = plot_size_comparison(df_agg[df_agg['data_structure_type']=='list'], args.output_dir, file_suffix='list', plot_format=args.plot_format)

    space_savings_dict_file = plot_space_savings(df_agg[df_agg['data_structure_type']=='dict'], args.output_dir, file_suffix='dict', plot_format=args.plot_format)
    space_savings_list_file = plot_space_savings(df_agg[df_agg['data_structure_type']=='list'], args.output_dir, file_suffix='list', plot_format=args.plot_format)

    efficiency_ration_dict_file = plot_efficiency_ratio(df_agg[df_agg['data_structure_type']=='dict'], args.output_dir, file_suffix='dict', plot_format=args.plot_format)
    efficiency_ration_list_file = plot_efficiency_ratio(df_agg[df_agg['data_structure_type']=='list'], args.output_dir, file_suffix='list', plot_format=args.plot_format)
    
    # Create summary
    breakeven_points_file = create_summary_table(df_agg, args.output_dir)
    
    print("\nBenchmarking plots generated successfully:")
    print(f"  - {size_comparison_dict_file}")
    print(f"  - {size_comparison_list_file}")
    print(f"  - {space_savings_dict_file}")
    print(f"  - {space_savings_list_file}")
    print(f"  - {efficiency_ration_dict_file}")
    print(f"  - {efficiency_ration_list_file}")
    print(f"  - {breakeven_points_file}")
    
    print(f"\nCrossover points identified (when mPickle becomes more efficient):")
    for (data_type, structure_type), size in breakeven_points.items():
        print(f"  {data_type} {structure_type}: {size} elements")

if __name__ == "__main__":
    main()