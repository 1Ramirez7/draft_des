"""
MicapQueue and MicapState Class Structure Guide

Quick reference for understanding what's critical vs flexible in each class.
Helps identify safe-to-modify areas vs core logic that affects the entire model.
"""

# ==============================================================================
# CLASS: MicapQueue
# ==============================================================================

# --- CORE INTERNAL LOGIC (Always Runs / Critical to Class Function) ---
# These must exist and work correctly or the entire queue breaks:

MicapQueue_CORE = [
    "self.queue (deque)",
    "  - Maintains chronological order of MICAP aircraft",
    "  - MUST preserve insertion order (FIFO)",
    "  - Core data structure - if this fails, everything fails",
    
    "self.lookup (dict)",
    "  - Maps ac_id -> record for O(1) removal",
    "  - MUST stay synchronized with self.queue",
    "  - If out of sync, removals will fail or be inconsistent",
    
    "self.active_ids (set)",
    "  - Tracks which ac_ids are currently in queue",
    "  - MUST stay synchronized with self.queue and self.lookup",
    "  - Used for duplicate detection",
    
    "add() - synchronization logic",
    "  - MUST update all three: queue, lookup, active_ids",
    "  - If any one fails to update, data structures become inconsistent",
    
    "remove_by_id() - synchronization logic",
    "  - MUST remove from all three: queue, lookup, active_ids",
    "  - Order matters: lookup first, then cleanup queue and set",
    
    "pop_first() - synchronization logic",
    "  - MUST remove from all three: queue, lookup, active_ids",
    "  - Deque.popleft() is critical for FIFO behavior",
]

# --- USER-CALLABLE METHODS (Not Internally Required) ---
# Can be changed, removed, or have implementation modified without breaking core:

MicapQueue_USER_CALLABLE = [
    "peek_first()",
    "  - Just reads self.queue[0], doesn't modify state",
    "  - Can change return format (dict, Series, custom object)",
    "  - Not used by other methods internally",
    
    "get_by_criteria()",
    "  - Searches queue based on strategy parameter",
    "  - Implementation can change (different sorting, filtering)",
    "  - Just needs to return list of records matching criteria",
    "  - Strategy names ('first', 'random', 'longest_micap') are flexible",
    
    "count()",
    "  - Just returns len(self.queue)",
    "  - Could return from any of the three data structures",
    "  - Not critical, just convenience",
    
    "is_empty()",
    "  - Just checks if queue has items",
    "  - Implementation flexible (check queue, lookup, or active_ids)",
    
    "get_all()",
    "  - Returns copy of entire queue as list",
    "  - Format can change (list, DataFrame, iterator)",
    "  - Not used internally",
]

# --- SPECIFIC CORE TASKS (Algorithmic Heart of the Class) ---
# The "how" can change, but the "what" must stay consistent:

MicapQueue_SPECIFIC_TASKS = [
    "Duplicate detection in add()",
    "  - Currently uses: if ac_id in self.active_ids",
    "  - Could also check: ac_id in self.lookup",
    "  - Must return error dict with success=False if duplicate found",
    "  - Caller (MicapState) expects: {'success': bool, 'error': str}",
    
    "FIFO ordering preservation",
    "  - Currently: deque.append() for add, deque.popleft() for pop_first",
    "  - Could use: list, heapq with counters, or custom linked list",
    "  - Must guarantee: first in = first out",
    
    "O(1) removal by ac_id",
    "  - Currently: dict lookup + deque reconstruction",
    "  - Could use: doubly-linked list, OrderedDict, etc.",
    "  - Performance requirement: fast lookups for large MICAP counts (2000+)",
    
    "get_by_criteria() - 'longest_micap' strategy",
    "  - Currently: calculates (current_time - micap_start) for all, sorts",
    "  - Could use: heapq.nlargest(), sorted() with key, manual scan",
    "  - Must return: aircraft with longest MICAP duration first",
    "  - Needs current_time parameter to calculate duration",
]

# --- EDGE CASE / OPTIONAL HELPERS (Indifferent to Core) ---
# These add safety/convenience but aren't required for basic operation:

MicapQueue_OPTIONAL = [
    "Error return in add()",
    "  - Currently returns {'success': False, 'error': msg}",
    "  - Could raise exception instead",
    "  - Could just return bool",
    "  - MicapState handles the error, so format is flexible",
    
    "Strategy validation in get_by_criteria()",
    "  - Currently raises ValueError for unknown strategy",
    "  - Could return empty list, log warning, or default to 'first'",
    "  - Not critical since caller controls strategy parameter",
    
    "current_time validation in get_by_criteria()",
    "  - Currently raises ValueError if missing for 'longest_micap'",
    "  - Could default to 0, skip sorting, or estimate",
    "  - Safety check but not strictly required",
]


# ==============================================================================
# CLASS: MicapState
# ==============================================================================

# --- CORE INTERNAL LOGIC (Always Runs / Critical to Class Function) ---
# These must exist and work correctly or model integration breaks:

MicapState_CORE = [
    "self.active_queue (MicapQueue instance)",
    "  - Stores all currently-active MICAP aircraft",
    "  - MUST exist for add/remove operations to work",
    "  - All MICAP operations route through this",
    
    "self.micap_log (list)",
    "  - Stores resolved MICAP history",
    "  - MUST be list (or appendable collection)",
    "  - Appended to in remove_aircraft() - if missing, logging fails",
    
    "add_aircraft() - record creation",
    "  - MUST create dict with all required keys:",
    "    'des_id', 'ac_id', 'event_path', 'fleet_duration', 'fleet_start',",
    "    'fleet_end', 'micap_start', 'micap_duration', 'micap_end'",
    "  - Keys must match what simulation engine expects",
    "  - Missing keys will break downstream DataFrame conversion",
    
    "remove_aircraft() - logging integration",
    "  - MUST call active_queue.remove_by_id()",
    "  - MUST append to micap_log before returning",
    "  - MUST calculate micap_duration and set micap_end",
    "  - Order matters: remove from queue, update record, log, return",
    
    "get_first_aircraft() - pandas Series conversion",
    "  - MUST return pd.Series (not dict) for backward compatibility",
    "  - Simulation engine expects Series with .iloc[0] style access",
    "  - If returns None when empty, engine must handle it",
]

# --- USER-CALLABLE METHODS (Not Internally Required) ---
# Can be changed, removed, or have implementation modified:

MicapState_USER_CALLABLE = [
    "remove_multiple()",
    "  - Batch removal for future event-driven removals",
    "  - Not used by current simulation engine",
    "  - Implementation can change (parallel processing, different strategies)",
    
    "get_active_aircraft()",
    "  - Returns DataFrame of active MICAP",
    "  - Used for compatibility/debugging",
    "  - Could return different format in future (dict, custom object)",
    "  - Sorting by ['micap_start', 'ac_id'] is implementation detail",
    
    "get_log_dataframe()",
    "  - Converts micap_log to DataFrame",
    "  - Not called during simulation",
    "  - Format flexible - could return JSON, dict, or custom format",
    
    "get_errors()",
    "  - Returns copy of self.errors list",
    "  - External monitoring only",
    "  - Could change to generator, iterator, or filtered view",
    
    "clear_errors()",
    "  - Resets error list",
    "  - Not required for simulation to run",
    
    "has_critical_errors()",
    "  - Convenience check for error list",
    "  - Could be property, method, or removed entirely",
    
    "count_active()",
    "  - Delegates to active_queue.count()",
    "  - Just convenience wrapper",
    
    "is_empty()",
    "  - Delegates to active_queue.is_empty()",
    "  - Just convenience wrapper",
]

# --- SPECIFIC CORE TASKS (Connection Points to Simulation Model) ---
# These connect MicapState to the rest of the simulation:

MicapState_SPECIFIC_TASKS = [
    "add_aircraft() - parameter contract",
    "  - Receives: des_id, ac_id, micap_type, fleet_duration, etc.",
    "  - Doesn't care HOW these values were calculated",
    "  - Only cares they exist and are correct types",
    "  - Example: fleet_duration could be from normal dist, uniform, constant",
    "  - As long as it's a float >= 0, add_aircraft() doesn't care",
    
    "remove_aircraft() - return contract",
    "  - MUST return dict with updated micap_end and micap_duration",
    "  - Caller (handle_part_completes_depot, etc.) expects these fields",
    "  - If None returned, caller knows aircraft wasn't in MICAP",
    "  - micap_duration calculation: micap_end - micap_start (can change formula)",
    
    "get_first_aircraft() - return format",
    "  - MUST return pd.Series or None",
    "  - Engine uses: first_micap['ac_id'], first_micap['des_id'], etc.",
    "  - Internal queue storage (dict) doesn't matter to caller",
    "  - Conversion to Series is MicapState's job, not caller's",
    
    "Error tracking - self.errors structure",
    "  - Currently: list of dicts with 'type', 'message', 'ac_id', etc.",
    "  - External error handler expects this structure",
    "  - Could change to custom Error objects, logging, or exceptions",
    "  - Key point: errors don't stop simulation, just logged",
]

# --- EDGE CASE / OPTIONAL HELPERS (Indifferent to Core) ---
# Safety checks and conveniences that could be removed:

MicapState_OPTIONAL = [
    "n_total_aircraft validation in add_aircraft()",
    "  - Checks: count_active() >= n_total_aircraft",
    "  - Logs error but still adds aircraft (non-blocking)",
    "  - Could raise exception, skip add, or remove check entirely",
    "  - Duplicate of validation that should happen before calling add",
    
    "Duplicate detection error logging in add_aircraft()",
    "  - Logs to self.errors when queue returns success=False",
    "  - Could just ignore duplicates silently",
    "  - Or raise exception to halt simulation",
    "  - Current behavior: log and continue",
    
    "removal_type parameter in remove_aircraft()",
    "  - Logged to micap_log for debugging/analysis",
    "  - Not used by simulation logic",
    "  - Could remove or make it required instead of optional",
    
    "self._counter in __init__()",
    "  - Tracks total MICAP events (active + resolved)",
    "  - Debugging/metrics only",
    "  - Not used in any logic decisions",
    
    "DataFrame column ordering in get_active_aircraft()",
    "  - Returns specific column order for consistency",
    "  - Could return columns in any order",
    "  - Pandas will handle it as long as column names match",
]


# ==============================================================================
# MODIFICATION SAFETY ZONES
# ==============================================================================

SAFE_TO_MODIFY = """
Safe to change without affecting simulation:
- Data structure implementations (deque → heapq, dict → OrderedDict)
- Return formats (dict → Series → custom object) AS LONG AS interface matches
- Error handling approach (log vs raise vs silent)
- Calculation methods (FIFO vs priority) AS LONG AS result is consistent
- Removal strategies (random, longest, etc.) - these are user-controlled
- Internal variable names (self.queue, self.lookup, etc.)
- Logging/debugging features (errors, counters, etc.)
"""

REQUIRES_COORDINATION = """
Changes that require updates elsewhere in the model:
- add_aircraft() parameters - affects all callers (handle_aircraft_needs_part, etc.)
- remove_aircraft() return structure - affects MICAP resolution handlers
- get_first_aircraft() return type - affects depot/part completion logic
- Record dict keys - affects DataFrame conversion and engine expectations
- initialize_from_dataframe() column names - affects DataFrameManager
"""

CORE_INVARIANTS = """
These MUST be maintained or everything breaks:
- FIFO ordering: first aircraft to enter MICAP is first to be resolved
- Synchronization: queue, lookup, active_ids must always match
- Record completeness: all required keys must exist in aircraft records
- Logging integrity: resolved MICAP must be logged before record is lost
- Return contracts: get_first_aircraft() returns Series/None, remove returns dict/None
"""



# remove this methods from both classes since they are not being use now
# can be re-added as needed (when adding option to add/remove MICAP aircraft)


# MicapQueue CLASS methods 

def remove_by_id(self, ac_id):
    """
    Remove aircraft by ac_id (O(1) lookup).
    
    Returns
    -------
    dict or None
        Removed record or None if not found
    """
    if ac_id not in self.lookup:
        return None
    
    record = self.lookup.pop(ac_id)
    self.active_ids.remove(ac_id)
    
    # Remove from deque (O(n) but only over active MICAP count)
    new_queue = deque(r for r in self.queue if r['ac_id'] != ac_id)
    self.queue = new_queue
    
    return record

def peek_first(self):
    """
    Get first aircraft without removing.
    
    Returns
    -------
    dict or None
        First aircraft record or None if empty
    """
    return self.queue[0] if self.queue else None


def get_by_criteria(self, count, strategy, current_time=None):
    """
    Get multiple aircraft by selection criteria.
    
    Parameters
    ----------
    count : int
        Number of aircraft to get
    strategy : str
        'first', 'random', 'longest_micap', or 'specific_ids'
    current_time : float, optional
        Current simulation time (needed for 'longest_micap')
    
    Returns
    -------
    list
        List of aircraft records
    """
    available = min(count, len(self.queue))
    if available == 0:
        return []
    
    queue_list = list(self.queue)
    
    if strategy == 'first':
        return queue_list[:available]
    
    elif strategy == 'random':
        return random.sample(queue_list, available)
    
    elif strategy == 'longest_micap':
        if current_time is None:
            raise ValueError("current_time required for 'longest_micap' strategy")
        
        # Calculate time in MICAP for each aircraft
        with_duration = [
            (current_time - r['micap_start'], r) 
            for r in queue_list
        ]
        # Sort by longest duration first
        with_duration.sort(key=lambda x: x[0], reverse=True)
        return [r for _, r in with_duration[:available]]
    
    else:
        raise ValueError(f"Unknown strategy: {strategy}")
    
def is_empty(self):
    """Check if queue is empty."""
    return len(self.queue) == 0

def get_all(self):
    """Return all aircraft as list (copy)."""
    return list(self.queue)


# MicapSate CLASS methods 


def add_aircraft(self, des_id, ac_id, micap_type, fleet_duration, 
                fleet_start, fleet_end, micap_start):
    """
    This is an existin method, just remove this code.
    this code is meant to check n_total_aircraft with active MICAP
    if ACTIVE MICAP is > n_total_aircraft then something is wrong
    """
    # Check aircraft count limit
    if (self.n_total_aircraft is not None and 
        self.count_active() >= self.n_total_aircraft):
        error = f"MICAP count ({self.count_active()}) would exceed total aircraft ({self.n_total_aircraft})"
        self.errors.append({
            'type': 'MICAP_COUNT_EXCEEDED',
            'message': error,
            'ac_id': ac_id,
            'current_count': self.count_active()
        }) # Error handling, can remove if issue handle else where. 

def remove_aircraft(self, ac_id, micap_end=None, event_type='PART_AVAILABLE'):
    """
    Remove aircraft from MICAP state and log the resolution.
    
    # See if needed it since pop_and_remove_first is doing this already.
    # also why does this remove by ac_id, i guess since it first peek to make sure it uses same id? 

    Parameters
    ----------
    ac_id : int
        Aircraft ID to remove
    micap_end : float, optional
        Time when MICAP was resolved
    event_type : str
        Type of removal ('PART_AVAILABLE', 'NEW_PART', 'FORCED_REMOVAL')
    
    Returns
    -------
    dict or None
        Removed aircraft record with updated micap_end/duration, or None if not found
    """
    record = self.active_queue.remove_by_id(ac_id)
    
    if record is None:
        return None # this is an untrack error, as none should not happen
    
    # Calculate micap_duration and set micap_end
    if micap_end is not None:
        record['micap_end'] = micap_end
        record['micap_duration'] = micap_end - record['micap_start']
    
    # Log the exit event
    log_entry = record.copy()
    log_entry['event'] = 'EXIT_MICAP'
    log_entry['event_type'] = event_type
    log_entry['micap_count'] = self.count_active()  # Count after removal
    log_entry['event_time'] = micap_end if micap_end is not None else np.nan
    self.micap_log.append(log_entry)
    
    return record

def get_first_aircraft(self):
    """
    Get first aircraft in MICAP queue without removing.
    
    #NOT USE BY MODEL NOW, WHEN MICAP STATE IS CALLED, ITS 100% of the time use
    Returns
    -------
    dict or None
        First aircraft record or None if empty
    """
    record = self.active_queue.peek_first()
    if record is None:
        return None
    
    # Convert to pandas Series for compatibility with existing code
    return pd.Series(record)

def get_active_aircraft(self):
    """
    Get all active MICAP aircraft as DataFrame for compatibility.
    
    Returns
    -------
    pd.DataFrame
        Active aircraft sorted chronologically
    """
    records = self.active_queue.get_all()
    if not records:
        return pd.DataFrame(columns=[
            'des_id', 'ac_id', 'event_path', 'fleet_duration', 'fleet_start', 
            'fleet_end', 'micap_duration', 'micap_start', 'micap_end'
        ])
    
    df = pd.DataFrame(records)
    # Sort by micap_start, then ac_id for tie-breaking (same as original)
    df = df.sort_values(['micap_start', 'ac_id']).reset_index(drop=True)
    return df

def get_dataframe(self):
    """
    Get active MICAP aircraft as DataFrame for debug or as needed.
    
    Returns
    -------
    pd.DataFrame
        Active MICAP aircraft DataFrame
    """
    return self.get_active_aircraft()

def is_empty(self):
    """
    Check if no aircraft are currently in MICAP.
    
    Returns
    -------
    bool
        True if no active MICAP aircraft, False otherwise
    """
    return self.active_queue.is_empty()

def get_errors(self):
    """
    Get list of critical errors for external monitoring.
    
    Returns
    -------
    list
        List of error dictionaries with type, message, and context
    """
    return self.errors.copy()

def clear_errors(self):
    """Clear the errors list after handling."""
    self.errors.clear()

def has_critical_errors(self):
    """
    Check if any critical errors exist.
    
    Returns
    -------
    bool
        True if critical errors exist
    """
    return len(self.errors) > 0

