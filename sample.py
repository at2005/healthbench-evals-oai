#!/usr/bin/env python3
import json
import sys
import random
from collections import defaultdict

def sample_by_theme_category(input_file, output_file, samples_per_combo=3):
    """
    Sample up to 3 JSONL lines for each unique theme-category combination.
    
    Args:
        input_file (str): Path to the input JSONL file
        output_file (str): Path to write the sampled output JSONL
        samples_per_combo (int): Number of samples to take for each combination
    """
    # Dictionary to store entries by theme-category combination
    entries_by_combo = defaultdict(list)
    
    # Read input file and group by theme-category
    with open(input_file, 'r') as f:
        for line_num, line in enumerate(f, 1):
            try:
                # Parse the JSON line
                data = json.loads(line.strip())
                
                # Extract tags if the example_tags field exists
                if "example_tags" in data and isinstance(data["example_tags"], list):
                    theme = None
                    category = None
                    
                    # Find theme and category tags
                    for tag in data["example_tags"]:
                        if tag.startswith("theme:"):
                            theme = tag.replace("theme:", "")
                        elif tag.startswith("physician_agreed_category:"):
                            category = tag.replace("physician_agreed_category:", "")
                    
                    # Store the entry if both theme and category are present
                    if theme and category:
                        combo = f"{theme}-{category}"
                        # Store the original line and its line number
                        entries_by_combo[combo].append((line.strip(), line_num))
            except json.JSONDecodeError:
                print(f"Warning: Could not parse line {line_num} as JSON, skipping")
                continue
    
    # Sample entries and write to output file
    with open(output_file, 'w') as out_f:
        combos_found = 0
        samples_written = 0
        
        for combo, entries in sorted(entries_by_combo.items()):
            # Sample up to N entries (or all if fewer than N)
            sample_size = min(samples_per_combo, len(entries))
            sampled_entries = random.sample(entries, sample_size)
            combos_found += 1
            samples_written += sample_size
            
            # Write the sampled entries to the output file
            for line, line_num in sampled_entries:
                out_f.write(line + "\n")  # Add newline after each JSON line
    
    print(f"Found {combos_found} unique theme-category combinations")
    print(f"Wrote {samples_written} sample entries to {output_file}")
    
    # Print the counts for each combination
    print("\nEntries per combination:")
    print("-" * 60)
    for combo, entries in sorted(entries_by_combo.items(), key=lambda x: len(x[1]), reverse=True):
        print(f"{combo}: {len(entries)} entries, sampled {min(samples_per_combo, len(entries))}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} <input_jsonl> <output_jsonl>")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    
    sample_by_theme_category(input_file, output_file) 