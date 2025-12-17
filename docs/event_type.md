# Event Types Reference

All events by the model log event types in the `event_type` field. 

- Serves to show path for each Aircraft and Part cycles. 
- Helps debugging by tracking 1st, last and all events recorded for a single cycle


## INITIALIZATION PHASE (`initialization.py`)

### 1. event_ic_iz_fs_fe - Initialize Fleet Start
- **Function**: `event_ic_iz_fs_fe()`
- **Event Type**: `IC_IZ_FS_FE`
- **Managers**: part_manager, ac_manager
- **PATH**: fleet_start > fleet_end

### 2. event_ic_ms - Inject Starting MICAP Aircraft
- **Function**: `event_ic_ms()`
- **Event Type**: `IC_MS`
- **Managers**: ac_manager, micap_state
- **PATH**: micap_start

### 3. event_ic_ijd - Inject Depot Parts
- **Function**: `event_ic_ijd()`
- **Event Type**: `IC_IjD`
- **Managers**: part_manager
- **PATH**: depot_start > depot_end

### 4. event_ic_ijcf - Inject Condition F Parts
- **Function**: `event_ic_ijcf()`
- **Event Type**: `IC_IjCF`
- **Managers**: part_manager
- **PATH**: condition_f_start

### 5. event_ic_ijca - Inject Condition A Parts
- **Function**: `event_ic_ijca()`
- **Event Type**: `IC_IjCA`
- **Managers**: part_manager, cond_a_state
- **PATH**: condition_a_start

### 6. eventm_ic_izca_cr - Resolve Initial MICAP with CA Parts
- **Function**: `eventm_ic_izca_cr()`
- **Event Types**:
  - `IC_MS_IE` (ac_manager)
    - **PATH**: micap_start > micap_end > install_start > install_end
  - `IC_CAS_IE` (part_manager)
    - **PATH**: condition_a_start > condition_a_end > install_start > install_end
  - `IC_CAP_FS_FE` (part_manager)
    - **PATH**: install_end > fleet_start > fleet_end
  - `IC_MAC_FS_FE` (ac_manager)
    - **PATH**: install_end > fleet_start > fleet_end

### 7. eventm_ic_fe_cf - Fleet End to Condition F
- **Function**: `eventm_ic_fe_cf()`
- **Event Type**: `IC_FE_CF`
- **Managers**: part_manager
- **PATH**: fleet_end > condition_f_start

---

## SIMULATION ENGINE PHASE (`simulation_engine.py`)

### 8. handle_part_completes_depot - Part Finishes Depot
- **Function**: `handle_part_completes_depot(sim_id)`
- **Triggered by**: `depot_complete` event

**CASE A1: No MICAP**
- **Event Type**: `DE_CA`
- **Managers**: part_manager, cond_a_state
- **PATH**: depot_end > condition_a_start

**CASE A2: MICAP exists**
- **Event Type (Part)**: `DE_DMR_IE`
  - **PATH**: depot_end > install_start > install_end (cycle ends)
- **Event Type (Aircraft)**: `ME_DMR_IE`
  - **PATH**: micap_end > install_start > install_end
- **Event Type (Cycle Restart)**: `DMR_CR_FS_FE`
  - **Managers**: ac_manager, part_manager
  - **PATH**: install_end > fleet_start > fleet_end
  - Indicates AIRCRAFT & PART from MICAP resolved by depot part


---

### 9. handle_aircraft_needs_part - Aircraft Completes Fleet
- **Function**: `handle_aircraft_needs_part(des_id)`
- **Triggered by**: `fleet_complete` event

**CASE B1: Part Available in CA**
- **Event Type (Part)**: `CAE_IE`
  - **PATH**: condition_a_end > install_start > install_end
- **Event Type (Aircraft)**: `FE_IE`
  - **PATH**: fleet_end > install_start > install_end
- **Event Type (Cycle Restart)**: `CAP_CR_FS_FE`
  - **Managers**: part_manager, ac_manager
  - **PATH**: install_end > fleet_start > fleet_end
  - Indicates aircraft received part from Condition A

**CASE B2: No Parts → Aircraft Goes MICAP**
- **Event Type**: `FE_MS`
- **Managers**: ac_manager, micap_state
- **PATH**: fleet_end > micap_start

---

### 10. handle_new_part_arrives - New Part Arrives
- **Function**: `handle_new_part_arrives(part_id)`
- **Triggered by**: `new_part_arrives` event


**PATH 1: No MICAP → Part to Condition A**
- **Event Type**: `NP_CA`
- **Managers**: part_manager, cond_a_state
- **PATH**: condition_a_start

**PATH 2: MICAP exists → Install Directly**
- **Event Type (Part)**: `NP_NMR_IE`
  - **PATH**: condition_a_start > condition_a_end > install_start > install_end
- **Event Type (Aircraft)**: `ME_NMR_IE`
  - **PATH**: micap_end > install_start > install_end
- **Event Type (Cycle Restart)**: `NMR_CR_FS_FE`
  - **Managers**: part_manager, ac_manager
  - **PATH**: install_end > fleet_start > fleet_end
  - Indicates AIRCRAFT & PART from MICAP resolved by new part arrival



---

### 11. event_cf_de - Condition F to Depot
- **Function**: `event_cf_de(sim_id)`
- **Triggered by**: `CF_DE` event
- **Event Type**: `CF_DE`
- **Managers**: part_manager
- **PATH**: condition_f_start > condition_f_end > depot_start > depot_end
- **Schedules**: `depot_complete` event
- **Note**: Only used for initial condition parts (`IC_IjCF` or `IC_IZ_FS_FE, IC_FE_CF`)

---

### 12. event_acp_fs_fe - Fleet Start to Fleet End
- **Function**: `event_acp_fs_fe(s4_install_end, new_sim_id, new_des_id)`
- **Event Type**: None (internal function, no event type assigned)
- **Managers**: part_manager, ac_manager
- **PATH**: install_end > fleet_start > fleet_end
- **Updates**: fleet_end in part_manager and ac_manager
- **Schedules**: `fleet_complete` and `part_fleet_end` events

---

### 13. event_p_cfs_de - Part Fleet End to Depot End
- **Function**: `event_p_cfs_de(sim_id)`
- **Triggered by**: `part_fleet_end` event

**Step 1: Condition F (all parts)**
- **Event Type**: `CFS_CFE`
- **Managers**: part_manager
- **PATH**: fleet_end > condition_f_start > condition_f_end

**Step 2a: Condemned Part**
- **Event Type**: `DS_DE_CONDEMN`
- **Managers**: part_manager
- **PATH**: depot_start > depot_end > CONDEMN
- **Schedules**: `part_condemn` event

**Step 2b: Normal Part**
- **Event Type**: `DS_DE`
- **Managers**: part_manager
- **PATH**: depot_start > depot_end
- **Schedules**: `depot_complete` event


### 14. event_p_condemn - Handle/Schedule New Part Arrival
- **Function**: `event_p_condemn(sim_id)`
- **Triggered by**: `part_condemn` event
- **Schedules**: `new_part_arrives` event (after `part_order_lag` delay)
- **Note**: This function schedules and logs old part and new part info for debugging. The actual new part arrival is handled by `handle_new_part_arrives()`
---

## Event Type Abbreviations

CFS = condition_f_start
CFE = condition_f_end

DS = depot_start
DE = depot_end 

CAS = condition_a_start
CAE = condition_a_end
CAP = use in cycle restart to indicate part came from condition_a

MS = micap_start
ME = micap_end
MAC = use in cycle restart to indicate ac came from MICAP (unique to initial conditions)
DMR = to indicate MICAP resolved via depot_end 
NMR = to indicate MICAP resolved via new_part arrive


IS = install_start
IE = install_end

---

## Complete Lifecycle Paths

This section documents all possible complete event paths observed in the simulation for both parts and aircraft cycles.

### Part Lifecycle Paths

All possible event_path sequences for part cycles (alphabetical order):

- **CAP_CR_FS_FE, CFS_CFE, DS_DE**
  - **PATH**: install_end > fleet_start > fleet_end > condition_f_start > condition_f_end > depot_start > depot_end
  - Part from Condition A resolves aircraft need, operates in fleet, fails, enters Condition F, enters depot (simulation ends while in depot)

- **CAP_CR_FS_FE, CFS_CFE, DS_DE, DE_CA, CAE_IE**
  - **PATH**: install_end > fleet_start > fleet_end > condition_f_start > condition_f_end > depot_start > depot_end > condition_a_start > condition_a_end > install_start > install_end
  - Part from Condition A resolves aircraft need, operates in fleet, fails, goes through repair depot, returns to Condition A, then installs on aircraft needing part

- **CAP_CR_FS_FE, CFS_CFE, DS_DE, DE_DMR_IE**
  - **PATH**: install_end > fleet_start > fleet_end > condition_f_start > condition_f_end > depot_start > depot_end > install_start > install_end
  - Part from Condition A resolves aircraft need, operates in fleet, fails, goes through repair depot, directly installs on MICAP aircraft

- **CAP_CR_FS_FE, CFS_CFE, DS_DE_CONDEMN**
  - **PATH**: install_end > fleet_start > fleet_end > condition_f_start > condition_f_end > depot_start > depot_end > CONDEMN
  - Part from Condition A resolves aircraft need, operates in fleet, fails, enters depot and is condemned at end of cycle

- **DMR_CR_FS_FE**
  - **PATH**: install_end > fleet_start > fleet_end
  - Part that resolved MICAP from depot starts new fleet cycle (simulation ends during fleet operation)

- **DMR_CR_FS_FE, CFS_CFE, DS_DE**
  - **PATH**: install_end > fleet_start > fleet_end > condition_f_start > condition_f_end > depot_start > depot_end
  - Part that resolved MICAP from depot, operates in fleet, fails, enters Condition F, enters depot (simulation ends while in depot)

- **DMR_CR_FS_FE, CFS_CFE, DS_DE, DE_CA, CAE_IE**
  - **PATH**: install_end > fleet_start > fleet_end > condition_f_start > condition_f_end > depot_start > depot_end > condition_a_start > condition_a_end > install_start > install_end
  - Part that resolved MICAP from depot, operates in fleet, fails, goes through repair depot, returns to Condition A, then installs on aircraft needing part

- **DMR_CR_FS_FE, CFS_CFE, DS_DE, DE_DMR_IE**
  - **PATH**: install_end > fleet_start > fleet_end > condition_f_start > condition_f_end > depot_start > depot_end > install_start > install_end
  - Part that resolved MICAP from depot, operates in fleet, fails, goes through repair depot, directly installs on MICAP aircraft

- **DMR_CR_FS_FE, CFS_CFE, DS_DE_CONDEMN**
  - **PATH**: install_end > fleet_start > fleet_end > condition_f_start > condition_f_end > depot_start > depot_end > CONDEMN
  - Part that resolved MICAP from depot, operates in fleet, fails, enters depot and is condemned at end of cycle

- **IC_CAP_FS_FE, IC_FE_CF**
  - **PATH**: install_end > fleet_start > fleet_end > condition_f_start
  - Initial Condition A part resolves initial MICAP, operates in fleet, fails and enters Condition F (simulation ends before depot entry)

- **IC_IjCA, IC_CAS_IE**
  - **PATH**: condition_a_start > condition_a_end > install_start > install_end
  - Part starts in Condition A during initialization, immediately resolves initial MICAP aircraft during initialization phase

- **IC_IjCF, CF_DE, DE_CA, CAE_IE**
  - **PATH**: condition_f_start > condition_f_end > depot_start > depot_end > condition_a_start > condition_a_end > install_start > install_end
  - Part starts in Condition F during initialization, moves through depot, returns to Condition A, then installs on aircraft needing part

- **IC_IjD, DE_CA, CAE_IE**
  - **PATH**: depot_start > depot_end > condition_a_start > condition_a_end > install_start > install_end
  - Part starts in depot during initialization, completes repair, goes to Condition A, then installs on aircraft needing part

- **IC_IjD, DE_DMR_IE**
  - **PATH**: depot_start > depot_end > install_start > install_end
  - Part starts in depot during initialization, completes repair, directly installs on MICAP aircraft

- **IC_IZ_FS_FE, IC_FE_CF, CF_DE, DE_CA, CAE_IE**
  - **PATH**: fleet_start > fleet_end > condition_f_start > condition_f_end > depot_start > depot_end > condition_a_start > condition_a_end > install_start > install_end
  - Part starts operating in fleet during initialization, fails, goes through Condition F and depot, returns to Condition A, then installs on aircraft needing part

- **IC_IZ_FS_FE, IC_FE_CF, CF_DE, DE_DMR_IE**
  - **PATH**: fleet_start > fleet_end > condition_f_start > condition_f_end > depot_start > depot_end > install_start > install_end
  - Part starts operating in fleet during initialization, fails, goes through Condition F and depot, directly installs on MICAP aircraft

- **NMR_CR_FS_FE**
  - **PATH**: install_end > fleet_start > fleet_end
  - New part that resolved MICAP starts new fleet cycle (simulation ends during fleet operation)

- **NMR_CR_FS_FE, CFS_CFE, DS_DE**
  - **PATH**: install_end > fleet_start > fleet_end > condition_f_start > condition_f_end > depot_start > depot_end
  - New part that resolved MICAP, operates in fleet, fails, enters Condition F, enters depot (simulation ends while in depot)

- **NMR_CR_FS_FE, CFS_CFE, DS_DE, DE_DMR_IE**
  - **PATH**: install_end > fleet_start > fleet_end > condition_f_start > condition_f_end > depot_start > depot_end > install_start > install_end
  - New part that resolved MICAP, operates in fleet, fails, goes through repair depot, directly installs on MICAP aircraft

- **NP_NMR_IE**
  - **PATH**: condition_a_start > condition_a_end > install_start > install_end
  - New part arrives after condemnation, immediately installs on waiting MICAP aircraft (cycle ends at installation)

### Aircraft Lifecycle Paths

All possible event_path sequences for aircraft cycles (alphabetical order):

- **CAP_CR_FS_FE, FE_IE**
  - **PATH**: install_end > fleet_start > fleet_end > install_start > install_end
  - Aircraft receives part from Condition A, operates in fleet, completes operation and receives another part from Condition A

- **CAP_CR_FS_FE, FE_MS, ME_DMR_IE**
  - **PATH**: install_end > fleet_start > fleet_end > micap_start > micap_end > install_start > install_end
  - Aircraft receives part from Condition A, operates in fleet, part fails and no parts available so enters MICAP, resolved by depot part

- **CAP_CR_FS_FE, FE_MS, ME_NMR_IE**
  - **PATH**: install_end > fleet_start > fleet_end > micap_start > micap_end > install_start > install_end
  - Aircraft receives part from Condition A, operates in fleet, part fails and no parts available so enters MICAP, resolved by new part

- **DMR_CR_FS_FE**
  - **PATH**: install_end > fleet_start > fleet_end
  - Aircraft MICAP resolved by depot part, starts new fleet cycle (simulation ends during fleet operation)

- **DMR_CR_FS_FE, FE_IE**
  - **PATH**: install_end > fleet_start > fleet_end > install_start > install_end
  - Aircraft MICAP resolved by depot part, operates in fleet, completes operation and receives part from Condition A

- **DMR_CR_FS_FE, FE_MS**
  - **PATH**: install_end > fleet_start > fleet_end > micap_start
  - Aircraft MICAP resolved by depot part, operates in fleet, part fails and enters MICAP (simulation ends while in MICAP)

- **DMR_CR_FS_FE, FE_MS, ME_DMR_IE**
  - **PATH**: install_end > fleet_start > fleet_end > micap_start > micap_end > install_start > install_end
  - Aircraft MICAP resolved by depot part, operates in fleet, part fails and no parts available so enters MICAP, resolved by depot part

- **DMR_CR_FS_FE, FE_MS, ME_NMR_IE**
  - **PATH**: install_end > fleet_start > fleet_end > micap_start > micap_end > install_start > install_end
  - Aircraft MICAP resolved by depot part, operates in fleet, part fails and no parts available so enters MICAP, resolved by new part

- **IC_IZ_FS_FE, FE_IE**
  - **PATH**: fleet_start > fleet_end > install_start > install_end
  - Aircraft starts operating in fleet during initialization, completes operation and receives part from Condition A

- **IC_IZ_FS_FE, FE_MS, ME_DMR_IE**
  - **PATH**: fleet_start > fleet_end > micap_start > micap_end > install_start > install_end
  - Aircraft starts operating in fleet during initialization, part fails and no parts available so enters MICAP, resolved by depot part

- **IC_MAC_FS_FE, FE_IE**
  - **PATH**: install_end > fleet_start > fleet_end > install_start > install_end
  - Aircraft initial MICAP resolved during initialization, operates in fleet, completes operation and receives part from Condition A

- **IC_MAC_FS_FE, FE_MS, ME_DMR_IE**
  - **PATH**: install_end > fleet_start > fleet_end > micap_start > micap_end > install_start > install_end
  - Aircraft initial MICAP resolved during initialization, operates in fleet, part fails and no parts available so enters MICAP, resolved by depot part

- **IC_MS, IC_MS_IE**
  - **PATH**: micap_start > micap_end > install_start > install_end
  - Aircraft starts in MICAP during initialization, immediately resolved by Condition A part during initialization phase

- **IC_MS, ME_DMR_IE**
  - **PATH**: micap_start > micap_end > install_start > install_end
  - Aircraft starts in MICAP during initialization, resolved by depot part completing repair

- **NMR_CR_FS_FE**
  - **PATH**: install_end > fleet_start > fleet_end
  - Aircraft MICAP resolved by new part, starts new fleet cycle (simulation ends during fleet operation)

- **NMR_CR_FS_FE, FE_MS**
  - **PATH**: install_end > fleet_start > fleet_end > micap_start
  - Aircraft MICAP resolved by new part, operates in fleet, part fails and enters MICAP (simulation ends while in MICAP)

- **NMR_CR_FS_FE, FE_MS, ME_DMR_IE**
  - **PATH**: install_end > fleet_start > fleet_end > micap_start > micap_end > install_start > install_end
  - Aircraft MICAP resolved by new part, operates in fleet, part fails and no parts available so enters MICAP, resolved by depot part

- **NMR_CR_FS_FE, FE_MS, ME_NMR_IE**
  - **PATH**: install_end > fleet_start > fleet_end > micap_start > micap_end > install_start > install_end
  - Aircraft MICAP resolved by new part, operates in fleet, part fails and no parts available so enters MICAP, resolved by new part