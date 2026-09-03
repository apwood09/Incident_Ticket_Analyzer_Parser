# ingestion.py
# implements cross-platform safe paths & native parsing for ITIL data layout

import csv
from pathlib import Path 
from typing import List, Dict

def parse_tickets_csv(file_path_str: str = "sample_tickets.csv") -> List[Dict[str, str]]:
    # point script -> csv location relative to execution folder
    file_path = Path(file_path_str)

    # fallback -> if not found, automatically resolve relative to the project root folder
    if not file_path.is_file():
        project_root_path = Path(__file__).resolve().parent.parent / file_path_str
        if project_root_path.is_file():
            file_path = project_root_path

    # open csv file safely -> standard conetxt manager & error handling 
    if not file_path.is_file(): 
        raise FileNotFoundError(f"Target data file not found at: {file_path.resolve()}")
    
    ticket_dataset = []

    with open(file_path, mode="r", encoding="utf-8", newline="") as csv_file: 
        # convert text blocks -> structural row dictionaries mapping headers as keys 
        csv_reader = csv.DictReader(csv_file)

        # pack all generated dictionary elements together into singular array list 
        for row in csv_reader: 
            # clean structural trailing spaces automatcially if present 
            clean_row = {str(k).strip(): str(v).strip() for k, v in row.items() if k is not None}
            ticket_dataset.append(clean_row)
    
    return ticket_dataset