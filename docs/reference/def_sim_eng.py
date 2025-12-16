"""
Simulation Engine for DES Simulation
Handles simulation logic, formulas, and event processing.
"""



def initialize_depot(self):
    """
    Continuation of definition/documentation

    `valid_idx` Requirements
    ------------------------
    * Select parts with defined `condition_f_start` and `depot_start` is NaN.
        * Can get rid of this by using event-name
    * Sort strictly by `condition_f_start` to enforce chronological order.
    * Pass parts to heapq in this exact order.
    * Prevent reprocessing of any part with an assigned `depot_start`.
    * Ensure no earlier cf_start appears after this function runs, since heapq won't correct out-of-order inputs.

    Dependency and Independency Handles for HEAPQ
    ----------------------------------
    A. `heapq` Dependency (The Order):
    * **Cronological Order is External:**
    * The `heapq` logic is entirely dependent on the order provided by `valid_idx`.
    * Processes each part individually in the order it was received. 
    * Does not account for parts who will/have a lower cf_start then current part.
    * If `valid_idx` passes parts in a non-sequential time order, heapq <br>
        will use that non-sequential order for assignment.

    B. Independency (Heap Calculation is Atomic): Calculation
    * The `heapq` processes each part **individually**. 
    * For any given part `i`, the calculation of `d_start` is **independent** of the <br>
    `condition_f_start` time of both *preceding* or *subsequent* process/ed part. 
    * It only depends on:
        1. The current part's `Condition F start` time. 
        2. The earliest available time in the depot `earliest = heapq.heappop`
        3. The `max(cf_start, earliest)` ensures that the part either starts depot <br>
            when it's ready, or when a slot is free, whichever time is *later*.
    * **Heap Abstraction:** The `heapq` abstracts the entire depot capacity constraint. 
        * Only needs to know the *earliest* available *slot* time. 
        * as it only processes one part at a time. 

    NOTES
    ---------

    Processing Order:
    * IMPORTANT: Events with earlier cf_start times than current cf_starts 
    may not have been processed by other events like MICAP and or fleet.
    * For example, aircraft starting in MICAP could have lower fleet duration
    than aircraft that started in fleet, but depending on initial conditions
    MICAP aircraft may not have processed yet. 
        * Parts starting in depot and only pushed to depot_end when this function is run. 
        * After this function is ran, and depot_end parts are processed, it will clear MICAP, <br>
        there is a probability for MICAP aircraft to finish fleet earlier than some of <br>
        the starting fleet aircraft. <br>
        That results in MICAP aircraft having earlier cf_start time but valid_idx missed it <br>
        in its first run, resulting in parts that have greater cf_start time to be proccessed <br>
        through depot first. 
        * results in the violation of the Chronological logic of the DES model. 
    """


# How to add New Event Handler

"""
1. Schedule Event/s using: `_schedule_initial_events`
1.1 make index holding all desire events
1.2 feed to the following to `schedule_event`
1.2.1 `event_time` = ex. depot_end, fleet_end etc
1.2.2 `event_type` = ex. new_part_arrives, IC_IjCF, fleet_complete
1.2.3 `entity_id` = sim_id, des_id, part_id (how it knows which one df row to edit)

2. Add New EVENT handler in run()
2.1 Follow same structure for existing events.

3. ADd/Create new EVENT HANDLER
3.1 examples
    * `handle_part_completes_depot`
    * `handle_aircraft_needs_part`

So far thats it. 

I'm doubtful of scheduling events in batches
* Was thinking of doing similar to how `process_new_cycle_stages`
* just one line of code: `self.schedule_event(s3_end, 'depot_complete', new_sim_id)`
* This would have required me to add this code to initialization.py 
    * Since all event scheduling in `_schedule_initial_events` deals with initial conditons
    * Decided keep it there for now to keep all main event handling in one place for now

"""

