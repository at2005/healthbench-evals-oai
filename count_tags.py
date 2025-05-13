#!/usr/bin/env python3
import json
import sys
from collections import Counter

def count_tag_combinations(jsonl_file):
    """Count the frequency of theme-category combinations in a JSONL file."""
    combo_counter = Counter()
    
    with open(jsonl_file, 'r') as f:
        for line in f:
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
                    
                    # Create and count the combination if both are present
                    if theme and category:
                        combo = f"{theme}-{category}"
                        combo_counter[combo] += 1
            except json.JSONDecodeError:
                print(f"Warning: Could not parse line as JSON, skipping")
                continue
    
    return combo_counter

def print_combinations_frequencies(counter):
    """Print the theme-category combination frequencies sorted by count (descending)."""
    print("Theme-Category Combinations:")
    print("-" * 60)
    
    for combo, count in counter.most_common():
        print(f"{combo}: {count}")
    
    print("-" * 60)
    print(f"Total unique combinations: {len(counter)}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <jsonl_file>")
        sys.exit(1)
    
    jsonl_file = sys.argv[1]
    combo_counter = count_tag_combinations(jsonl_file)
    print_combinations_frequencies(combo_counter) 