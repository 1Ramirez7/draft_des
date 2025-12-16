# Event Types Reference



## INITIALIZATION PHASE (`initialization.py`)

### 1. event_ic_iz_fs_fe - Initialize Fleet Start old event_ic_iz_fs_fe
- `IC_IZ_FS_FE` = part_manager, ac_manager
- PATH: fleet_start > fleet_end

### 2. event_ic_ms - Inject Starting MICAP Aircraft
- `IC_MS` = ac_manager, micap_state
- PATH: micap_start

### 3. event_ic_ijd - Inject Depot Parts
- `IC_IjD` = part_manager
- PATH: depot_start > depot_end

### 4. event_ic_ijcf - Inject Condition F Parts
- `IC_IjCF` = part_manager
- path: condition_f_start

### 5. event_ic_ijca - Inject Condition A Parts
- `IC_IjCA` = part_manager, cond_a_state
- path: condition_a_start

### 6. eventm_ic_izca_cr - Resolve Initial MICAP with CA Parts
- `IC_MS_IE` = ac_manager
- PATH: micap_start > micap_end > install_start > install_end
- `IC_CAS_IE` = part_manager
- path:condition_a_start > condition_a_end > install_start > install_end
- `IC_CAP_FS_FE` = part_manager
- PATH: install_end > fleet_start > fleet_end
- `IC_MAC_FS_FE` = ac_manager
- PATH: install_end > fleet_start > fleet_end

### 7. eventm_ic_fe_cf - Fleet End to Condition F
- `IC_FE_CF` = part_manager
- PATH: fleet_end > fleet_start

---

## SIMULATION ENGINE PHASE (`simulation_engine.py`)



### 9. handle_part_completes_depot - Part Finishes Depot

No MICAP 
- `DE_CA` = part_manager, cond_a_state
- PATH: depot_end > condition_a_start

MICAP
- `DE_DMR_IE` = part_manager
- PATH: depot_end > install_start > install_end (cycle ends)
- `ME_DMR_IE` = ac_manager
- PATH: micap_End > install_start > install_end

- `DMR_CR_FS_FE` = ac_manager, part_manager
- PATH: fleet_start > fleet_end
- To indicate AIRCRAFT & PART was from MICAP resolved by DE part


---

### 10. handle_aircraft_needs_part - Aircraft Completes Fleet

**CASE B1: Part Available in CA**
- `CAE_IE` = part_manager
- PATH: condition_a_end > install_start > install_end
- `FE_IE` = ac_manager
- PATH: fleet_end > install_start > install_end
- `CAP_CR_FS_FE` = part_manager, ac_manager
- PATH: Fleet_start > fleet_end
- to indicate AIRCRAFT received PART from condition_a

**CASE B2: No Parts → Aircraft Goes MICAP**
- `FE_MS` = ac_manager
- PATH: fleet_end > micap_start

---


### 11. handle_new_part_arrives - New Part Arrives


**PATH 1: No MICAP → Part to Condition A**
- `NP_CA` = part_manager, cond_a_state
- PATH: condition_a_start

**PATH 2: MICAP exists → Install Directly**
- `NP_NMR_IE` = part_manager
- PATH: new_part > condition_a_start > condition_a_end > install_start > install_end
- `ME_NMR_IE` = ac_manager
- PATH: micap_end > install_start > install_end

- `NMR_CR_FS_FE` = part_manager, ac_manager
- PATH: fleet_start > fleet_end
- To indicate AIRCRAFT & PART was from MICAP resolved by NEW PART arrival



---

### 12. event_cf_de - Condition F to Depot
- `CF_DE` = part_manager
- PATH: condition_f_start > condition_f_end > depot_start > depot_end
- schedules `depot_complete`

---

### 13. event_acp_fs_fe - Fleet Start to Fleet End
- no event type assigned
- PATH: install_end > fleet_start > fleet_end
- updates fleet_end in part_manager and ac_manager
- schedules `fleet_complete` and `part_fleet_end`

---

### 14. event_p_cfs_de - Part Fleet End to Depot End

- `CFS_CFE` = part_manager (part has event regardless if condemn or not)
- PATH: fleet_end > condition_f_start > condition_f_end

**Condemned Part:** old CONDEMN
- `DS_DE_CONDEMN` = part_manager
- PATH: depot_start > depot_end > CONDEMN
- schedules `part_condemn`

**Normal Part:**
- `DS_DE` = part_manager
- PATH: depot_start > depot_end
- schedules `depot_complete`


### 15. event_p_condemn - Handle/schedule new part arrival

- this function schedules and logs old part and new part info for debugging
- event type handle by engine.handle_new_part_arrives



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


IS =install_start
IE = install_end