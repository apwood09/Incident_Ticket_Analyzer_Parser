import argparse
from ingestion import parse_tickets_csv
from analyzer import calculate_mttr

def generate_report(metrics: dict):
    """Constructs a clean, text-based dashboard layout using aligned f-strings."""
    print("=" * 60)
    print(f"{'SYSTEM PERFORMANCE DASHBOARD':^60}")
    print("=" * 60)
    print(f"{'Metric Name':<35} | {'Value':>20}")
    print("-" * 60)

    for key, value in metrics.items():
        formatted_key = key.replace("_", " ").title()
        print(f"{formatted_key:<35} | {value:>20}")
    
    print("=" * 60)

def main():
    parser = argparse.ArgumentParser(description="Generate a terminal-based performance dashboard.")
    parser.add_argument(
        "--file", 
        type=str, 
        required=True, 
        help="Path to the target data file for ingestion."
    )

    args = parser.parse_args()

    # Execute data processing pipeline 
    raw_data = parse_tickets_csv(args.file)
    metrics = calculate_mttr(raw_data)
    generate_report(metrics)

if __name__ == "__main__":
    main()