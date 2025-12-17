# BRAIN OF MODEL

These events are what makes the simulation run

- depot_complete
- fleet_complete
- new_part_arrives
- part_fleet_end
- part_condemn

All events in the model, including initilization.py are made so parts and aircraft
are always schedule by one of these events. 

initialization.py is made so all parts and aircraft in the model are schedule by
one of the events above before the main simulation starts. 


The event `depot_complete` takes PARTS from `depot_end` to the following

CASE 1 (continue by another event)
- depot_end > condition_a_start
  - event ends here, a different event will finish cycle
  - lets name this partial cycle cas_pending

CASE 2
- depot_end > install_start > install_end > fleet_start
  - Cycle continue by helper function: `event_acp_fs_fe`

NOTE: This event does NOT handle CONDEMNED PARTS




The event `fleet_complete` takes AIRCRAFTS from `fleet_end` to the following


CASE 1
- fleet_end > install_start > install_end > records end of `cycle`
  - continues event for cas_pending or 

- starts new cycle for AIRCRAFT and PART: fleet_start
  - Cycle continue by helper function: `event_acp_fs_fe`


CASE 2 (continue by another event)
- fleet_end > micap_start
  - event ends here, a different event will finish cycle


Helper function: `event_acp_fs_fe`



The event `new_part_arrives` takes NEW PART from `condition_a_start` to the following

CASE 1 - no MICAP aircraft 
- conditon_a_start
  - new part is added to simulation to the following
    - added to active parts by: ` self.part_manager.add_initial_part`
    - added to Condition A active parts by `self.cond_a_state.add_part`
- NOTE this is the first record of the new part and cycle = 0
  - event `fleet_complete` will finish the zero cycle for new part


CASE 2 - MICAP exists
- condition_a_start > condition_a_end > install_start > install_end > records end of `cycle`
  - NOTE that this event added the first log for the new part in active parts
    - Also recorded the end of `cycle`

- Start new cycle for new PART - CYCLE = 1
  - fleet_start
    - Cycle continue by helper function: `event_acp_fs_fe`


The event `part_fleet_end` takes PARTS from `fleet_end` to the following

This event handles the part lifecycle after fleet operation ends. It processes:
1. Condition F (failure state)
2. Depot capacity checking
3. Condemn cycle checking

CASE 1 - Normal Part (not at condemn cycle)
- fleet_end > condition_f_start > condition_f_end > depot_start > depot_end
  - Part enters Condition F (waits for depot capacity if needed)
  - Part enters depot with FULL depot_duration
  - Schedules `depot_complete` event at depot_end
  - Cycle continues by event `depot_complete`

CASE 2 - Condemned Part (cycle == condemn_cycle)
- fleet_end > condition_f_start > condition_f_end > depot_start > depot_end > CONDEMN
  - Part enters Condition F (waits for depot capacity if needed)
  - Part enters depot with REDUCED depot_duration (depot_duration * condemn_depot_fraction)
  - Schedules `part_condemn` event at depot_end
  - Cycle continues by event `part_condemn`

NOTE: 
- Depot capacity is checked FIRST before condemn decision
- If depot is full, part waits in Condition F until capacity available
- Condemn check happens AFTER depot_start is determined


The event `part_condemn` takes CONDEMNED PART at `depot_end` to the following

This event handles the end of a condemned part's lifecycle and orders a replacement.

CASE 1 (only case - always orders new part)
- depot_end > CONDEMN (old part lifecycle ENDS here)
  - Old condemned part is logged and cycle completes
  - New replacement part is ordered with part_id = old_part_id
  - New part has cycle = 0 (starts fresh)
  - Schedules `new_part_arrives` event after part_order_lag delay
  - New part lifecycle begins when `new_part_arrives` event fires

NOTE:
- This event ENDS the old part's lifecycle completely
- The old part is NOT reused or tracked further
- A brand new part is created
- The new part arrival is handled by `new_part_arrives` event



from simulation_engine.py 


if event_type == 'depot_complete':
    # EVENT TYPE: Part Completes Depot
    self.handle_part_completes_depot(entity_id)

    # EVENT TYPE: Aircraft Completes Fleet
elif event_type == 'fleet_complete':
    self.handle_aircraft_needs_part(entity_id)

    # EVENT TYPE: New Part Arrives
elif event_type == 'new_part_arrives':
    self.handle_new_part_arrives(entity_id)

    # EVENT TYPE:
elif event_type == 'part_fleet_end':
    self.event_p_cfs_de(entity_id)

    # EVENT TYPE:
elif event_type == 'part_condemn':
    self.event_p_condemn(entity_id)
