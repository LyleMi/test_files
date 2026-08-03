#!/usr/bin/env python3
"""AriadneBench starter: replace the empty result with your general parser."""
import argparse
import json
from pathlib import Path

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--artifacts", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    # The evaluator owns --output. Always create it, even when no APIs are found.
    args.output.write_text(json.dumps({"schema_version": "3.0", "apis": []}) + "\n", encoding="utf-8")

if __name__ == "__main__": main()
