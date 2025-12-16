# System Architecture

## Overview

The Discrete Event Simulation system models aircraft parts lifecycle through multiple stages using a discrete event simulation approach.

## Current Architecture

### Core Components

| Component | File | Purpose |
|-----------|------|---------|
| **Landing Page** | `streamlit_app/main.py` | Application entry point, navigation to Solo Run or Scenarios |
| **Solo Run Page** | `streamlit_app/pages/solo_run.py` | Single simulation with full visualization |
| **Simulation Engine** | `streamlit_app/simulation_engine.py` | Core simulation logic, event processing |
| **Initialization** | `streamlit_app/initialization.py` | Initial conditions setup |
| **Parameters** | `streamlit_app/parameters.py` | Centralized parameter management |
| **PostSim** | `streamlit_app/post_sim.py` | Post-simulation statistics and figure generation |

### Entity Managers

| Component | File | Purpose |
|-----------|------|---------|
| **PartManager** | `streamlit_app/entity_part.py` | O(1) part tracking with dictionary lookups |
| **AircraftManager** | `streamlit_app/entity_ac.py` | O(1) aircraft tracking with dictionary lookups |

### State Managers

| Component | File | Purpose |
|-----------|------|---------|
| **MicapState** | `streamlit_app/ph_micap.py` | MICAP queue management (aircraft waiting for parts) |
| **ConditionAState** | `streamlit_app/ph_cda.py` | Available parts inventory |
| **NewPart** | `streamlit_app/ph_new_part.py` | Condemned part replacement tracking |

### Data & UI

| Component | File | Purpose |
|-----------|------|---------|
| **DataSets** | `streamlit_app/ds/data_science.py` | Output data storage and export |
| **UI Components** | `streamlit_app/ui/ui_components.py` | Streamlit sidebar widgets for Solo Run |
| **Session Manager** | `streamlit_app/session_manager.py` | Streamlit session state handling |
| **Stats** | `streamlit_app/ui/stats.py` | Statistics display components |
| **Distribution Plots** | `streamlit_app/ui/dist_plots.py` | Duration distribution visualizations |
| **WIP Plots** | `streamlit_app/ui/wip_plots.py` | Work-in-progress visualizations |

## Simulation Approach

**Event-Driven DES**: Priority queue (heap) processes events at exact times in chronological order. Events scheduled when durations complete, processed from heap until simulation time limit reached.

## Data Structures

### Entity Tracking (Dictionary-based)

**PartManager.active**: Active parts keyed by `sim_id`
```python
{sim_id: {part_id, cycle, fleet_start, fleet_end, ...}}
```

**AircraftManager.active**: Active aircraft keyed by `des_id`
```python
{des_id: {ac_id, fleet_start, fleet_end, micap_start, ...}}
```

### Output DataFrames

| DataFrame | Description |
|-----------|-------------|
| `all_parts_df` | Complete part event log (sim_id, part_id, durations, times, cycle) |
| `all_ac_df` | Complete aircraft event log (des_id, ac_id, part assignments, MICAP times) |
| `wip_df` | Work-in-progress snapshots over simulation time |

### Constraints

- **1:1 plane:part**: Each aircraft has exactly one part at a time
- **Initial pairing**: First n_aircraft parts paired 1-to-1 with aircraft
- **Leftover parts**: Start in Condition A (available inventory)

## System Flow

```
Part Lifecycle: Fleet → Condition F → Depot → Condition A → Install → Fleet (repeat)
Aircraft: Normal → Needs Part → MICAP (if no part) → Normal (when part installed)
```

**Event Types**:
- **depot_complete**: Part finishes depot → MICAP exists? install : Condition A
- **fleet_complete**: Aircraft finishes fleet → Part available? install : MICAP
- **new_part_arrives**: Condemned replacement arrives → MICAP exists? install : Condition A

## State Management

**Queues**:
- MICAP (aircraft waiting, FIFO via MicapState)
- Condition A (available parts via ConditionAState)

**Constraints**:
- Depot capacity (max parts simultaneously, enforced via priority queue)
- Condemn cycle limit (parts condemned after N cycles)

## Data Flow

```
User Input → Parameters → SimulationEngine → Event Processing → State Updates → DataSets → Visualization/Export
```

## Related Documentation

- [Flowchart Diagrams](flowchart.md) - Visual representation of business logic
- [Class Architecture](uml-classes.md) - UML class diagram and responsibilities
- [Event Types Reference](event_type.md) - Event naming conventions
