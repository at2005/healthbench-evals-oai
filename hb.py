#!/usr/bin/env python
"""
Example script to run HealthBench evaluations using a local consensus.jsonl file.
"""

import argparse
import subprocess
from pathlib import Path
from dotenv import load_dotenv

def main():
    load_dotenv()
    
    parser = argparse.ArgumentParser(description="Run HealthBench with local file")
    parser.add_argument(
        "--input_file", 
        type=str, 
        default="data/healthbench_consensus.jsonl",
        help="Path to local jsonl file containing evaluation examples"
    )
    parser.add_argument(
        "--examples", 
        type=int, 
        help="Number of examples to run"
    )
    parser.add_argument(
        "--n-threads",
        type=int,
        default=7,
        help="Number of threads to run",
    )
    parser.add_argument(
        "--model",
        type=str,
        help="Model to evaluate (if not provided, will prompt)",
    )
    args = parser.parse_args()
    
    # Make sure the input file exists
    input_path = Path(args.input_file)
    if not input_path.exists():
        print(f"Error: Input file {input_path} does not exist.")
        return
        
    # Construct command
    cmd = [
        "python", "-m", "healthbench-evals-oai.healthbench_eval",
        "--custom_input_path", str(input_path),
    ]
    
    # Add optional arguments
    if args.examples:
        cmd.extend(["--examples", str(args.examples)])
    if args.n_threads:
        cmd.extend(["--n-threads", str(args.n_threads)])
        
    # Run command
    print(f"Running: {' '.join(cmd)}")
    subprocess.run(cmd)
    
if __name__ == "__main__":
    main() 