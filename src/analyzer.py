from collections import defaultdict 
from typing import Dict, List, Any 

def group_tickets_by(tickets: List[Dict[str, Any]], key: str) ->Dict[str, List[Dict[str, Any]]]: 
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

def calculate_mttr(tickets: List[Dict[str, Any]], resolution_time_key: str = 'resolution_time_hours') -> float: 
    """computes Mean Time to Resolution (MTTR) for given dataset of resolved tickets"""
    # extract resolution times, ensuring key exists & its value is not None
    resolved_times = [
        ticket[resolution_time_key] for ticket in tickets
        if resolution_time_key in ticket and ticket[resolution_time_key] is not None 
    ]
    # guard clause: return 0.0 if the list is empty to prevent a ZeroDivisionError
    if not resolved_times: 
        return 0.0 
    # compute & return the average resolution time
    return sum(resolved_times) / len(resolved_times)