# Variable Names Reference

Complete reference of all variable names used in the simulation code.

## INPUT PARAMETERS
- `n_total_parts` - Total number of parts in active DES circulation
- `n_total_aircraft` - Total number of aircraft
- `sim_time` - Simulation duration in days
- `sone_mean` - Fleet mean duration
- `sone_sd` - Fleet standard deviation
- `stwo_mean` - Condition F mean duration
- `stwo_sd` - Condition F standard deviation
- `sthree_mean` - Depot mean duration
- `sthree_sd` - Depot standard deviation
- `sfour_mean` - Part Install mean duration
- `sfour_sd` - Part Install standard deviation

## PARAMETER DATAFRAME
- `params_df` - DataFrame storing parameters by period
- `period` - Simulation period/day (1 to sim_time)

## DATAFRAMES
- `condition_a_df` - Parts waiting in Condition A inventory (pandas DataFrame)
- `new_part_df` - Tracking for created replacement parts
- `all_parts_df` - Complete part event log (exported from PartManager at simulation end)
- `all_ac_df` - Complete aircraft event log (exported from AircraftManager at simulation end)

## MANAGER CLASSES (Active Tracking During Simulation)
- `PartManager` - O(1) dictionary-based active part tracking
- `AircraftManager` - O(1) dictionary-based active aircraft tracking
- `MicapState` - MICAP queue management

## DATAFRAME COLUMNS (ENTITY IDs)
- `des_id` - DES event ID (primary key for aircraft events in all_ac_df)
- `ac_id` - Aircraft ID (identifies which physical aircraft)
- `sim_id` - SIM event ID (primary key for part events in all_parts_df)
- `part_id` - Part ID (identifies which physical part)

## DATAFRAME COLUMNS (FOREIGN KEYS)
- `desone_id` - DES ID from fleet cycle (foreign key linking to all_ac_df via des_id)
- `acone_id` - Aircraft ID from fleet cycle
- `destwo_id` - DES ID from Condtion A cycle (foreign key linking to all_ac_df via des_id)
- `actwo_id` - Aircraft ID from Condtion A cycle
- `simone_id` - SIM ID from fleet cycle (foreign key linking to all_parts_df via sim_id)
- `partone_id` - Part ID from fleet cycle
- `simtwo_id` - SIM ID from Condtion A cycle (foreign key linking to all_parts_df via sim_id)
- `parttwo_id` - Part ID from Condtion A cycle

## TEMP VARIBALES FOR NEWLY GENERATED SIM_ID AND DES_ID. (EG. A method can be handling two sim_id)
- `new_sim_id` - New sim_id for cycle restart
- `new_des_id` - New des_id for cycle restart
- `new_sim_id_restart` - sim_id for cycle restart (alternative naming)
- `new_des_id_restart` - des_id for cycle restart (alternative naming)
- `des_id_for_sim` - des_id to use for part's foreign key reference

## DATAFRAME COLUMNS (STATUS & METADATA)
- `micap` - TEMP: Event type describing the event (e.g., "DE_MI", "AFE_CA", "IC_IZ_FS_FE")
- `condemn` - Condemnation status ("yes" or "no")
- `cycle` - Cycle number (cycle is set by user conditions. New part cycle starts at 0)


## DATAFRAME COLUMNS (FLEET)
- `fleet_duration` - Fleet duration
- `fleet_start` - Fleet start time
- `fleet_end` - Fleet end time

## DATAFRAME COLUMNS (CONDITION F)
- `condition_f_duration` - Condition F duration
- `condition_f_start` - Condition F start time
- `condition_f_end` - Condition F end time

## DATAFRAME COLUMNS (DEPOT)
- `depot_duration` - Depot duration
- `depot_start` - Depot start time
- `depot_end` - Depot end time

## DATAFRAME COLUMNS (CONDITION A AVAILABLE)
- `condition_a_duration` - Time part waited Condition A
- `condition_a_start` - When part entered Condition A
- `condition_a_end` - When part left Condition A

## DATAFRAME COLUMNS (PART INSTALL)
- `install_duration` - Part Install duration
- `install_start` - Part Install start time
- `install_end` - Part Install end time

## DATAFRAME COLUMNS (MICAP)
- `micap_duration` - MICAP duration
- `micap_start` - MICAP start time
- `micap_end` - MICAP end time

## PHASE TIMING VARIABLES (use in calcuations)
- `s1_start` - Fleet start time
- `s1_end` - Fleet end time
- `s2_start` - Condition F start time
- `s2_end` - Condition F end time
- `s3_start` - Depot start time
- `s3_end` - Depot end time
- `s4_start` - Condition A start time (unused in current code)
- `s4_end` - Condition A end time (unused in current code)
- `s4_install_start` - Part Install start time
- `s4_install_end` - Part Install end time

## DURATION DRAWS
- `d1` - Fleet duration time. Runs calculation for stage_one to get time ac and part will be in fleet
- `d2` - Condition F duration time. 
- `d3` - Depot duration time. Runs calculation to obtained time in this stage
- `d4_install` - Temp, can remove, always zero. using to record pair of part and aircraft


## MANAGER CLASS VARIABLES
- `part_manager.active` - Dictionary of active parts {sim_id: record}
- `part_manager.part_log` - List of completed part cycles
- `part_manager.next_sim_id` - Auto-incrementing sim_id counter
- `ac_manager.active` - Dictionary of active aircraft {des_id: record}
- `ac_manager.ac_log` - List of completed aircraft cycles
- `ac_manager.next_des_id` - Auto-incrementing des_id counter

## LOOP VARIABLES (Event-Driven Architecture)
- `event_heap` - Priority queue of (time, counter, event_type, entity_id) tuples
- `event_counter` - FIFO tie-breaker for simultaneous events
- `current_time` - Simulation clock (advances only when processing events)
- `event_time` - When the current event occurs
- `event_type` - Type of event ('depot_complete', 'fleet_complete', 'new_part_arrives', 'CF_DE', 'part_fleet_end', 'part_condemn')
- `entity_id` - ID of entity involved in event (sim_id for parts, des_id for aircraft, part_id for new parts)
- `result` - Return dictionary from manager methods (contains generated IDs)

## LOOP VARIABLES
- `ac_record` - Aircraft record from AircraftManager (O(1) lookup)
- `part_row` / `part_record` - Part record from PartManager (O(1) lookup)
- `first_micap` - First MICAP aircraft to resolve (from MicapState)
- `first_available` - First available part to install (from condition_a_df)

## EVENT PROCESSING VARIABLES
- `micap_pa_rm` - MICAP aircraft popped from MicapState queue for part available
- `micap_npa_rm` - MICAP aircraft popped from MicapState queue for new part arrival
- `available_parts` - Parts in condition_a_df inventory
- `n_available` - Number of available parts in condition_a_df
- `has_des_id` - Boolean: whether MICAP aircraft already has a des_id
- `active_parts` - Dictionary of active parts from PartManager
- `active_aircraft` - Dictionary of active aircraft from AircraftManager




## POST-SIMULATION VARIABLES
- `validation_results` - Dictionary containing event_counts
- `event_counts` - Dictionary tracking number of each event type
