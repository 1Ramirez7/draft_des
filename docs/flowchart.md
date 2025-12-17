# Simulation Flow Diagrams

testing 1 

This document shows the business logic flow of the aircraft parts simulation system, which tracks two interconnected lifecycles: **Part Lifecycle** and **Aircraft Lifecycle**.

## System Overview

The simulation tracks two interconnected lifecycles that work together to model aircraft maintenance and parts availability:

- **Part Lifecycle**: Tracks parts from operation through maintenance back to availability
- **Aircraft Lifecycle**: Tracks aircraft from operation through MICAP (Mission Capability) status

## Part Lifecycle Flow

```mermaid
flowchart TD
    A[Fleet Stage<br/>Part on aircraft] -->|fleet_end event| B[Condition F<br/>Failure detected]
    
    B --> C{Depot Capacity<br/>Available?}
    
    C -->|YES| D[Enter Depot<br/>depot_start = fleet_end]
    C -->|NO| W[Wait for slot<br/>depot_start delayed]
    W --> D
    
    D --> E{Cycle == Condemn Cycle?}
    
    E -->|NO - Normal Part| F1[Depot Repair<br/>Full duration]
    E -->|YES - Condemned| F2[Depot Processing<br/>Reduced duration]
    
    F1 -->|depot_complete event| G{Any MICAP<br/>Aircraft?}
    
    F2 -->|part_condemn event| H[Order New Part<br/>part_order_lag delay]
    H --> I[New Part Arrives<br/>new_part_arrives event]
    I --> J{Any MICAP<br/>Aircraft?}
    
    G -->|YES| K1[Install on MICAP AC<br/>Resolve MICAP]
    G -->|NO| L1[Condition A<br/>Wait in inventory]
    
    J -->|YES| K2[Install on MICAP AC<br/>Resolve MICAP]
    J -->|NO| L2[Condition A<br/>Wait in inventory]
    
    L1 --> M[Wait for aircraft need]
    L2 --> M
    M -->|Aircraft fleet_complete| N[Install]
    
    K1 --> O[New Cycle<br/>cycle + 1]
    K2 --> P[New Cycle<br/>cycle = 1 for new part]
    N --> O
    
    O --> A
    P --> A
    
    style A fill:#e1f5fe
    style K1 fill:#c8e6c9
    style K2 fill:#c8e6c9
    style N fill:#c8e6c9
    style L1 fill:#fff3e0
    style L2 fill:#fff3e0
    style H fill:#ffeb3b
    style I fill:#c5e1a5
    style F2 fill:#ffcdd2
```

**Key Points:**
- Depot capacity is checked **first** when part enters Condition F
- Condemn decision is made **after depot_start is determined** based on `cycle == condemn_cycle`
- Condemned parts use reduced depot time (`depot_duration * condemn_depot_fraction`)
- The **old condemned part's lifecycle ends** at `part_condemn` event
- A **new replacement part** is created with `cycle=0` and arrives after `part_order_lag`

## Aircraft Lifecycle Flow

```mermaid
flowchart TD
    A[Fleet Stage<br/>Part operating] -->|fleet_complete event| B{Part Available<br/>in Condition A?}
    
    B -->|YES| C[Install Part<br/>From inventory]
    B -->|NO| D[Enter MICAP<br/>Wait for part]
    
    D --> E{Part Becomes<br/>Available?}
    
    E -->|depot_complete| F1[Part from Depot<br/>Resolves MICAP]
    E -->|new_part_arrives| F2[New Part<br/>Resolves MICAP]
    
    F1 --> G[Install]
    F2 --> G
    C --> G
    
    G --> H[New Cycle]
    H --> A
    
    style A fill:#e1f5fe
    style C fill:#c8e6c9
    style G fill:#c8e6c9
    style D fill:#ffcdd2
```

## Combined System Flow (Simplified)

```mermaid
flowchart TD
    subgraph "Part Lifecycle"
        P1[Fleet] --> P2[Condition F]
        P2 --> P2A{Depot Capacity?}
        P2A -->|YES| P2B[Enter Depot]
        P2A -->|NO| P2C[Wait]
        P2C --> P2B
        P2B --> P2D{Condemned?}
        P2D -->|NO| P3[Depot Repair]
        P2D -->|YES| P3B[Depot + Condemn]
        P3B --> P3C[Order New Part]
        P3C --> P3D[New Part Arrives]
        P3 --> P4{Any MICAP?}
        P3D --> P4
        P4 -->|YES| P5[Install]
        P4 -->|NO| P6[Condition A]
        P6 --> P7[Wait]
        P7 --> P5
        P5 --> P1
    end
    
    subgraph "Aircraft Lifecycle"
        A1[Fleet] --> A2{Part in CA?}
        A2 -->|YES| A3[Install]
        A2 -->|NO| A4[MICAP]
        A4 --> A5[Wait for Part]
        A5 --> A3
        A3 --> A1
    end
    
    P5 -.->|Resolves| A4
    A4 -.->|Triggers| P5
    
    style P1 fill:#e1f5fe
    style A1 fill:#e1f5fe
    style P5 fill:#c8e6c9
    style A3 fill:#c8e6c9
    style A4 fill:#ffcdd2
    style P3B fill:#ffcdd2
    style P3C fill:#ffeb3b
    style P3D fill:#c5e1a5
```

## Event Types and Flow

### Main Event Loop Events

| Event | Handler | Trigger |
|-------|---------|---------|
| `fleet_complete` | `handle_aircraft_needs_part()` | Aircraft completes fleet stage |
| `depot_complete` | `handle_part_completes_depot()` | Normal part completes repair |
| `new_part_arrives` | `handle_new_part_arrives()` | Replacement part arrives |
| `part_fleet_end` | `event_p_cfs_de()` | Part's fleet stage ends, enters CF→Depot flow |
| `CF_DE` | `event_cf_de()` | Part moves from Condition F to Depot |
| `part_condemn` | `event_p_condemn()` | Condemned part triggers new part order |

### Event Flow by Scenario

**Normal Part Completes Depot (No MICAP):**
```
depot_complete → handle_part_completes_depot() → Part to Condition A
```

**Normal Part Completes Depot (MICAP exists):**
```
depot_complete → handle_part_completes_depot() → Install on MICAP AC → event_acp_fs_fe() → Schedule fleet_complete + part_fleet_end
```

**Aircraft Needs Part (Available):**
```
fleet_complete → handle_aircraft_needs_part() → Take from Condition A → event_acp_fs_fe() → Schedule fleet_complete + part_fleet_end
```

**Aircraft Needs Part (None Available):**
```
fleet_complete → handle_aircraft_needs_part() → Enter MICAP queue
```

**Condemned Part:**
```
part_fleet_end → event_p_cfs_de() [depot capacity check THEN condemn check] → Schedule part_condemn
part_condemn → event_p_condemn() → Order new part → Schedule new_part_arrives
new_part_arrives → handle_new_part_arrives() → [Same as depot_complete logic]
```

## Depot Capacity Management

The depot uses a **heap-based scheduling** approach, not a waiting loop:

```python
# FIRST: Check depot capacity
if len(active_depot) < depot_capacity:
    depot_start = fleet_end  # Start immediately
else:
    earliest_free = heapq.heappop(active_depot)
    depot_start = max(fleet_end, earliest_free)  # Start when slot opens

# THEN: Check condemn cycle
if cycle == condemn_cycle:
    # Condemned path...
else:
    # Normal path...
```

- Parts don't "wait in a queue" - their `depot_start` time is calculated based on when capacity becomes available
- The `active_depot` heap tracks when each depot slot will free up
- Condition F duration = `depot_start - fleet_end` (waiting time, can be 0)
- Condemn check happens **after** depot_start is determined

## Condemnation Logic

Condemnation is **deterministic based on cycle count**, checked **after depot capacity**:

```python
# In event_p_cfs_de() - order matters!

# 1. FIRST: Calculate depot_start based on capacity
if len(self.active_depot) < self.params['depot_capacity']:
    s3_start = s1_end
else:
    earliest_free = heapq.heappop(self.active_depot)
    s3_start = max(s1_end, earliest_free)

# 2. THEN: Check condemn cycle
if cycle == params['condemn_cycle']:
    condemn = "yes"
    depot_duration = calculate_depot_duration() * condemn_depot_fraction
    schedule_event(depot_end, 'part_condemn', sim_id)
else:
    depot_duration = calculate_depot_duration()
    schedule_event(depot_end, 'depot_complete', sim_id)
```

- A part is condemned when `cycle == condemn_cycle` (e.g., condemn at cycle 5)
- Condemned parts use reduced depot time (inspection before disposal)
- At `part_condemn`, a new replacement part is ordered
- The **old part's lifecycle ends** - it is not reused
- The **new part** starts at `cycle=0`
