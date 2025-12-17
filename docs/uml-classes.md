# Class Architecture

**[Download PDF to see Mermaid diagrams](https://github.com/1Ramirez7/draft_des/raw/main/docs/uml-classes.pdf)**
 
This document describes the class structure of the simulation system.

## Method Naming Conventions

Method names use abbreviations for stages and events:

| Abbreviation | Meaning |
|--------------|---------|
| `IC` | Initial Condition (initialization phase) |
| `IZ` | Initialize |
| `FS` | Fleet Start |
| `FE` | Fleet End |
| `CF` | Condition F |
| `CFS` / `CFE` | Condition F Start / End |
| `DE` | Depot End |
| `DS` | Depot Start |
| `CA` / `CAS` / `CAE` | Condition A / Start / End |
| `MS` / `ME` | MICAP Start / End |
| `IE` | Install End |
| `CR` | Cycle Restart |
| `Ij` | Inject (add initial parts/aircraft) |
| `DMR` | Depot MICAP Resolve |
| `NMR` | New Part MICAP Resolve |
| `NP` | New Part |

**Example:** `event_ic_iz_fs_fe` = Initial Condition, Initialize, Fleet Start to Fleet End

## UML Class Diagram

```mermaid
classDiagram
    class SimulationEngine {
        +Parameters params
        +dict allocation
        +list active_depot
        +list event_heap
        +int event_counter
        +MicapState micap_state
        +PartManager part_manager
        +AircraftManager ac_manager
        +ConditionAState cond_a_state
        +NewPart new_part_state
        +DataSets datasets
        +dict event_counts
        +calculate_fleet_duration()
        +calculate_depot_duration()
        +schedule_event()
        +handle_part_completes_depot()
        +handle_aircraft_needs_part()
        +handle_new_part_arrives()
        +event_cf_de()
        +event_acp_fs_fe()
        +event_p_cfs_de()
        +event_p_condemn()
        +_schedule_initial_events()
        +run()
    }
    
    class Parameters {
        -dict _params
        +set(key, value)
        +set_all(params_dict)
        +get(key, default)
        +keys()
        +to_dict()
        +get_params_df()
    }
    
    class Initialization {
        +SimulationEngine engine
        +run_initialization()
        +event_ic_iz_fs_fe()
        +event_ic_ms()
        +event_ic_ijd()
        +event_ic_ijcf()
        +event_ic_ijca()
        +eventm_ic_izca_cr()
        +eventm_ic_fe_cf()
    }
    
    class PartManager {
        +dict active
        +list part_log
        +int next_sim_id
        +get_next_sim_id()
        +add_part()
        +add_initial_part()
        +get_part()
        +get_all_active_parts()
        +update_fields()
        +complete_part_cycle()
        +complete_pca_cycle()
        +get_all_parts_data_df()
        +get_wip_end()
        +get_wip_raw()
    }
    
    class AircraftManager {
        +dict active
        +list ac_log
        +int next_des_id
        +int micap_count
        +list micap_log
        +get_next_des_id()
        +add_ac()
        +add_initial_ac()
        +get_ac()
        +get_all_active_ac()
        +update_fields()
        +complete_ac_cycle()
        +get_all_ac_data_df()
        +track_micap_wip()
        +get_micap_log()
        +get_wip_ac_end()
        +get_wip_ac_raw()
    }
    
    class MicapState {
        +MicapQueue active_queue
        +list micap_log
        +add_aircraft()
        +pop_and_rm_first()
        +count_active()
        +get_log_dataframe()
        +get_micap_wip_df()
    }
    
    class MicapQueue {
        +deque queue
        +dict lookup
        +set active_ids
        +add()
        +pop_first()
        +count()
        +is_empty()
    }
    
    class ConditionAState {
        +deque queue
        +dict lookup
        +list condition_a_log
        +add_part()
        +pop_first_available()
        +count_active()
        +is_empty()
        +get_log_dataframe()
    }
    
    class NewPart {
        +dict active
        +int next_part_id
        +list condemn_log
        +get_next_part_id()
        +add_new_part()
        +get_part()
        +get_all_active()
        +remove_part()
        +count_active()
        +log_condemnation()
        +get_condemn_log_dataframe()
    }
    
    class DataSets {
        +DataFrame all_parts_df
        +DataFrame all_ac_df
        +DataFrame wip_df
        +DataFrame wip_raw
        +DataFrame wip_ac_df
        +DataFrame wip_ac_raw
        +build_part_ac_df()
    }
    
    class PostSim {
        +DataSets datasets
        +dict event_counts
        +Parameters params
        +dict allocation
        +bool render_plots
        +dict dist_figs
        +dict wip_figs
        +compute_stats()
        +generate_dist_figures()
        +generate_wip_figures()
        +has_wip_data()
    }
    
    SimulationEngine --> Parameters : uses
    SimulationEngine *-- PartManager : creates
    SimulationEngine *-- AircraftManager : creates
    SimulationEngine *-- MicapState : creates
    SimulationEngine *-- ConditionAState : creates
    SimulationEngine *-- NewPart : creates
    SimulationEngine *-- DataSets : creates
    SimulationEngine *-- PostSim : creates
    SimulationEngine ..> Initialization : creates & runs
    PostSim --> DataSets : uses
    MicapState *-- MicapQueue : contains
```

## Class Responsibilities

### Core Classes

| Class | File | Purpose |
|-------|------|---------|
| `SimulationEngine` | `simulation_engine.py` | Main simulation loop, event processing, coordination |
| `Parameters` | `parameters.py` | Centralized parameter storage with dict-style access |
| `Initialization` | `initialization.py` | Initial conditions setup (fleet start, depot injection, etc.) |
| `PostSim` | `post_sim.py` | Post-simulation statistics and figure generation |
| `DataSets` | `ds/data_science.py` | Output data storage (DataFrames for export) |

### Entity Managers (O(1) Dictionary Lookups)

| Class | File | Purpose |
|-------|------|---------|
| `PartManager` | `entity_part.py` | Track active parts, log completed cycles |
| `AircraftManager` | `entity_ac.py` | Track active aircraft, log completed cycles |

### State Managers (Queue-based)

| Class | File | Purpose |
|-------|------|---------|
| `MicapState` | `ph_micap.py` | MICAP queue (FIFO), aircraft waiting for parts |
| `MicapQueue` | `ph_micap.py` | Internal queue implementation for MicapState |
| `ConditionAState` | `ph_cda.py` | Available parts inventory (FIFO) |
| `NewPart` | `ph_new_part.py` | Condemned part replacement tracking |

## Method Explanations

### SimulationEngine Methods

| Method | Purpose |
|--------|---------|
| `calculate_fleet_duration()` | Draw random fleet stage duration (Normal or Weibull) |
| `calculate_depot_duration()` | Draw random depot repair duration (Normal or Weibull) |
| `schedule_event(time, type, id)` | Add event to priority queue (heap) |
| `handle_part_completes_depot(sim_id)` | Part finishes depot: check MICAP or go to Condition A |
| `handle_aircraft_needs_part(des_id)` | Aircraft needs part: take from CA or enter MICAP |
| `handle_new_part_arrives(part_id)` | New part arrives: check MICAP or go to Condition A |
| `event_cf_de(sim_id)` | Condition F to Depot End (schedules depot_complete) |
| `event_acp_fs_fe(...)` | Aircraft-Part Fleet Start to Fleet End (new cycle start) |
| `event_p_cfs_de(sim_id)` | Part Condition F Start to Depot End (depot capacity check, then condemn check) |
| `event_p_condemn(sim_id)` | Handle condemned part, order replacement |
| `_schedule_initial_events()` | Schedule all events after initialization phase |
| `run()` | Main event loop - process heap until time limit |

### Initialization Methods

| Method | Purpose |
|--------|---------|
| `run_initialization()` | Orchestrate all initialization steps |
| `event_ic_iz_fs_fe()` | Initialize parts/aircraft in Fleet (paired 1:1) |
| `event_ic_ms()` | Inject aircraft starting in MICAP status |
| `event_ic_ijd()` | Inject parts starting in Depot |
| `event_ic_ijcf()` | Inject parts starting in Condition F |
| `event_ic_ijca()` | Inject parts starting in Condition A |
| `eventm_ic_izca_cr()` | Resolve initial MICAP with available CA parts |
| `eventm_ic_fe_cf()` | Handle initial fleet_end to condition_f transitions |

## Output DataFrames

| DataFrame | Description |
|-----------|-------------|
| `all_parts_df` | Complete part event log (all cycles, all stages) |
| `all_ac_df` | Complete aircraft event log (all cycles) |
| `wip_df` | Work-in-progress snapshots (parts by stage over time) |
| `wip_raw` | Raw WIP data before aggregation |
| `wip_ac_df` | Aircraft WIP snapshots over time |
| `wip_ac_raw` | Raw aircraft WIP data |

## Key Design Patterns

### Dictionary-based Entity Tracking
Both `PartManager` and `AircraftManager` use dictionaries keyed by ID (`sim_id`, `des_id`) for O(1) lookups.

### Queue-based State Management
`MicapState` and `ConditionAState` use `deque` + `dict` combinations for:
- FIFO ordering (chronological processing)
- O(1) lookups by ID
- Event logging for debugging

### Event-Driven Architecture
The simulation uses a priority queue (heap) to process events chronologically:
- Events scheduled with `(time, counter, event_type, entity_id)`
- Counter ensures FIFO for same-time events
- Each handler schedules future events

### Composition Pattern
`SimulationEngine` creates and owns all manager classes:
- Creates `PartManager`, `AircraftManager`, `MicapState`, `ConditionAState`, `NewPart`, `DataSets` in `__init__`
- Creates `Initialization` in `run()` and passes `self` reference
- Managers don't know about each other - engine coordinates
