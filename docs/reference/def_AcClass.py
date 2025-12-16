"""
Steps for adding function to mgr_ac.py

"""



"""
Here are some ideas for methods
"""


    # ===========================================================
    # CORE OPERATIONS: LIFECYCLE/COMPLETE AIRCRAFT CYCLES
    # ===========================================================

def complete_ac_cycle_with_validation(self, des_id, ac_id):
    """
    Log completed cycle for an aircraft with extra validation.
    
    Validates that the ac_id in the active record matches the provided ac_id
    before completing the cycle.
    
    Args:
        des_id (int): DES event ID of the aircraft completing its cycle
        ac_id (int): Aircraft ID to validate against
        
    Returns:
        dict or None: Completed aircraft record if found and valid, None if not found
    
    Notes: 
        Method complete_ac_cycle could have been used, this function adds 
        an extra check to make sure transitions do not corrupt des_id & ac_id pair
        
    Raises:
        ValueError: If ac_id in active record does not match provided ac_id
    """
    record = self.active.get(des_id)
    if not record:
        return None
        
    if record['ac_id'] != ac_id:
        raise ValueError(
            f"Aircraft ID mismatch for des_id {des_id}: "
            f"Active record has {record['ac_id']}, "
            f"provided ac_id is {ac_id}"
        )
        
    return self.complete_ac_cycle(des_id)


# ===========================================================
# UTILITY: QUERY METHODS
# ===========================================================

def get_aircraft_by_ac_id(self, ac_id):
    """
    Get all active aircraft records for a specific aircraft (ac_id).
    
    Useful when you need to find all active cycles for a single aircraft.
    Note: In most cases, an aircraft should only have one active cycle at a time.
    
    Args:
        ac_id (int): Aircraft identifier to search for
        
    Returns:
        list: List of aircraft records with matching ac_id
    """
    return [record for record in self.active.values() if record['ac_id'] == ac_id]

def get_aircraft_in_fleet(self, current_time):
    """
    Get all aircraft currently in fleet stage at a given time.
    
    Args:
        current_time (float): Current simulation time
        
    Returns:
        list: List of aircraft records currently in fleet
    """
    return [
        record for record in self.active.values()
        if (pd.notna(record['fleet_start']) and 
            record['fleet_start'] <= current_time and
            (pd.isna(record['fleet_end']) or record['fleet_end'] > current_time))
    ]

def count_active(self):
    """
    Get count of currently active aircraft.
    
    Returns:
        int: Number of active aircraft records
    """
    return len(self.active)

