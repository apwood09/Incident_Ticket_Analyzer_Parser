import argparse
from ingestion import parse_tickets_csv
from analyzer import calculate_mttr

def generate_report(metrics: dict):
    """Constructs a clean, text-based dashboard layout using aligned f-strings."""
    # print top decorative border & centered dashboard title
    print("=" * 60)
    print(f"{'SYSTEM PERFORMANCE DASHBOARD':^60}")
    print("=" * 60)
    # print table headers with lt & rt alignment padding
    print(f"{'Metric Name':<35} | {'Value':>20}")
    print("-" * 60)

    # iterate through each metric, formatting the dictionary keys for readability
    for key, value in metrics.items():
        # replace underscores with spaces & capitalize words (e.g., 'mean_time' -> 'Mean Time')
        formatted_key = key.replace("_", " ").title()
        print(f"{formatted_key:<35} | {value:>20}")
    
    # print bottom closing border
    print("=" * 60)

def main():
    # initialize command-line argument parser
    parser = argparse.ArgumentParser(description="Generate a terminal-based performance dashboard.")
    # define required '--file' argument to accept the target data path
    parser.add_argument()
    parser.add_argument(
        "--file", 
        type=str, 
        required=True, 
        help="Path to the target data file for ingestion."
    )

    # parse arguments provided via command line
    args = parser.parse_args()

    # execute data processing pipeline: parse CSV -> calculate metrics -> display report
    raw_data = parse_tickets_csv(args.file)
    metrics = calculate_mttr(raw_data)
    generate_report(metrics)

# standard entry point guard to run the main function when executed as a script
if __name__ == "__main__":
    main()