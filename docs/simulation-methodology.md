# Simulation Methodology

## Overview

The Discrete Event Simulation models the lifecycle of aircraft parts through 
multiple stages, tracking both parts and aircraft through the system.

## Implementation: Event-Driven DES

Priority queue (heap) processes events at exact times in chronological order. 
Events scheduled when durations complete (`depot_end`, `fleet_end`, `new_part_arrival`), processed from heap until simulation time limit reached.

## Part Lifecycle Stages

| Stage | Description | Duration |
|-------|-------------|----------|
| **Fleet** | Part operating on aircraft | Configurable distribution (Normal or Weibull) |
| **Condition F** | Waiting for depot slot | Variable (0 if depot available, >0 if depot at capacity) |
| **Depot** | Repair in progress | Configurable distribution (Normal or Weibull), capacity-limited |
| **Condition A** | Available in inventory | Waiting time until aircraft needs part |
| **Install** | Installation on aircraft | Instant (duration = 0) |

## Aircraft Lifecycle

**Normal**: One part assigned, operates until failure, needs replacement on failure

**MICAP**: Waiting for part (entered on failure with no replacement), resolved when part available, FIFO processing

## Distribution Parameters

### Fleet Stage
- `sone_dist`: Distribution type ("Normal" or "Weibull")
- `sone_mean`: Mean (Normal) or Shape parameter (Weibull)
- `sone_sd`: Std Dev (Normal) or Scale parameter (Weibull)

### Depot Stage
- `sthree_dist`: Distribution type ("Normal" or "Weibull")
- `sthree_mean`: Mean (Normal) or Shape parameter (Weibull)
- `sthree_sd`: Std Dev (Normal) or Scale parameter (Weibull)

## Constraints

### 1:1 Plane:Part
- Each aircraft has exactly one part at a time
- Initial pairing: first n_aircraft parts paired 1-to-1
- Leftover parts are allocated based on initial condition parameters (`parts_in_depot`, `parts_in_cond_f`, `parts_in_cond_a`)

### Depot Capacity
- Maximum parts in depot simultaneously
- Parts wait in Condition F if depot at capacity

### Condemnation
- Parts condemned after reaching `condemn_cycle` limit
- Condemned parts trigger new part order with `part_order_lag` lead time
- `condemn_depot_fraction` determines depot time before condemnation decision

## Initial Conditions

Configurable allocation of parts at simulation start:
- `parts_in_depot`: Parts starting in depot repair
- `parts_in_cond_f`: Parts starting in Condition F
- `parts_in_cond_a`: Parts starting in available inventory
- Remaining parts: On aircraft in fleet stage

## Random Number Generation

NumPy random generator with configurable seed for reproducibility.

Duration draws:
- Normal: `max(0, np.random.normal(mean, sd))`
- Weibull: `scale * np.random.weibull(shape)`

## Validation

### Data Integrity Checks
- No duplicate IDs (sim_id, des_id unique)
- Valid timing (start ≤ end for all stages)
- Continuity (fleet_start = previous install_end)
- 1:1 constraint maintained

### Output Validation
- Cycle counts within limits
- All events processed
- No orphaned records

## Output Data

| DataFrame | Content |
|-----------|---------|
| `all_parts_df` | Complete part history (all cycles, all stages) |
| `all_ac_df` | Complete aircraft history (all cycles) |
| `wip_df` | Work-in-progress snapshots over time |
