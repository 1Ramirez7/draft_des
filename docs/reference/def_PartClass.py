

"""
Steps for adding function to part_manager.py


"""





"""
Here are some ideas for methods
"""

def get_active_count(self):
    """
    Get count of currently active parts. Simple count of dict size.
    
    Returns:
        int: Number of parts currently in active tracking
    """
    return len(self.active)

def get_completed_count(self):
    """
    Get count of completed part cycles.
    
    Returns:
        int: Number of parts that have completed their cycles
    """
    return len(self.part_log)

def clear_logs(self):
    """
    Clear completed cycle logs (for memory management in long simulations).
    
    Note: Use with caution as this removes historical data.
    """
    self.part_log.clear()

def validate_active_parts(self):
    """
    Validate that all active parts have required fields.
    key =sim_id, if in future edits add_row is use to modify active row then this should theorerically catch it
    
    Returns:
        dict: {'valid': bool, 'errors': list of error messages}
    """
    errors = []
    required_fields = ['sim_id', 'part_id', 'cycle']
    
    for sim_id, record in self.active.items():
        # Check that sim_id in record matches dictionary key
        if record.get('sim_id') != sim_id:
            errors.append(f"sim_id mismatch: key={sim_id}, record={record.get('sim_id')}")
        
        # Check required fields are present
        for field in required_fields:
            if field not in record or record[field] is None:
                errors.append(f"sim_id {sim_id} missing required field '{field}'")
    
    return {'valid': len(errors) == 0, 'errors': errors}

