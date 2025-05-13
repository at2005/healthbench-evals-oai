#!/usr/bin/env python
"""
Example script to run HealthBench evaluations using a local consensus.jsonl file.
"""

import argparse
import subprocess
from pathlib import Path
from dotenv import load_dotenv
import os
import sys
from sampler.ai_sdk_sampler import AISDKSampler

def main():
    load_dotenv()
    
    parser = argparse.ArgumentParser(description="Run HealthBench with local file")
    parser.add_argument(
        "--input_file", 
        type=str, 
        default="data/consensus_short.jsonl",
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
        default="gpt-4.1",
        help="Model to evaluate",
    )
    parser.add_argument(
        "--temperature",
        type=float,
        default=1.0,
        help="Temperature for sampling",
    )
    parser.add_argument(
        "--max_tokens",
        type=int,
        default=1024,
        help="Maximum tokens for generation",
    )
    parser.add_argument(
        "--api_url",
        type=str,
        default="http://localhost:3000/api/chat-buffer",
        help="API URL for AI SDK sampler",
    )
    args = parser.parse_args()
    
    # Make sure the input file exists
    input_path = Path(args.input_file)
    if not input_path.exists():
        print(f"Error: Input file {input_path} does not exist.")
        return
    
    # Initialize the AISDKSampler
    sampler = AISDKSampler(
        model=args.model,
        temperature=args.temperature,
        max_tokens=args.max_tokens,
        api_url=args.api_url,
    )
    
    # Set environment variables for the sampler configuration
    os.environ["AI_SDK_MODEL"] = args.model
    os.environ["AI_SDK_TEMPERATURE"] = str(args.temperature)
    os.environ["AI_SDK_MAX_TOKENS"] = str(args.max_tokens)
    os.environ["AI_SDK_API_URL"] = args.api_url
    
    # Construct command
    cmd = [
        "python", "-m", "healthbench_eval",
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