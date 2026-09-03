# analyzer.py 

from collections import defaultdict 
from typing import Dict, List, Any 
from datetime import datetime, timezone

def group_tickets_by(tickets: List[Dict[str, Any]], key: str) -> Dict[str, List[Dict[str, Any]]]: 
    """Groups List of ticket dictionaries by specific attribute (e.g 'priority', 'resolved_time_hours')"""
    # initialize defaultdict with lists to auto group items without raising KeyErrors
    # append current ticket dictionary into its corresponding group list
    grouped = defaultdict(list)
    for ticket in tickets: 
        # fetch value for the specified key; default to 'Unknown' if the key doesn't exist
        grouped[ticket.get(key, 'Unknown')].append(ticket)
    # convert defaultdict back to a standard Python dictionary before returning
    return dict(grouped)

def filter_tickets(tickets: List[Dict[str, Any]], criteria: Dict[str, Any]) -> List[Dict[str, Any]]: 
    """Filter tickets based on key-value criteria pairs"""
    # use list comprehension to evaluate every ticket against all conditions in the criteria dictionary
    return [
        ticket for ticket in tickets
        if all(ticket.get(k) == v for k, v in criteria.items())
    ]

def count_by_attribute(tickets: List[Dict[str, Any]], attribute: str) -> Dict[str, int]: 
    """counts frequency of tickets across given attribute (e.g counting tickets by prioerity)"""
    # initialize a defaultdict with integers (defaults to 0) to track frequencies safely
    counts = defaultdict(int)
    for ticket in tickets: 
        # retrieve attribute value or fallback to 'Unknown'
        val = ticket.get(attribute, 'Unknown')
        # increment count for that specific attribute value
        counts[val] += 1
    # convert back to standard dictionary
    return dict(counts)

def calculate_mttr(tickets: List[Dict[str, Any]], resolution_time_key: str = 'resolution_time_hours') -> dict: 
    """computes Mean Time to Resolution (MTTR) for given dataset of resolved tickets"""
    total_hours = 0.0
    resolved_count = 0

    for ticket in tickets:
        # sample_tickets.csv column headers
        created_str = ticket.get("created_at")
        resolved_str = ticket.get("resolved_at")

        if created_str and resolved_str and resolved_str.strip():
            try:
                # strip the 'Z' suffix & parse as a naive datetime, then attach UTC timezone
                clean_created = created_str.replace('Z', '')
                clean_resolved = resolved_str.replace('Z', '')

                # parse date strings 
                created_dt = datetime.strptime(clean_created, "%Y-%m-%dT%H:%M:%S").replace(tzinfo=timezone.utc)
                resolved_dt = datetime.strptime(clean_resolved, "%Y-%m-%dT%H:%M:%S").replace(tzinfo=timezone.utc)
                
                # calculate hours between creation and resolution
                duration_hours = (resolved_dt - created_dt).total_seconds() / 3600
                if duration_hours >= 0:
                    total_hours += duration_hours
                    resolved_count += 1
            except ValueError as e:
                # print -> error
                print(f"Debug - Date parsing failed for row {ticket.get('ticket_id')}: {e} (Value: {created_str} / {resolved_str})")
                continue

    # compute final mean time to resolution
    mttr = (total_hours / resolved_count) if resolved_count > 0 else 0.0

    # return dictionary matching keys to your reporter table format
    return {
        "mean_time_to_resolution_hours": round(mttr, 2),
        "total_tickets_processed": len(tickets)
    }