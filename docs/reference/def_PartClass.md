

# PartManager Data Storage Examples - How Data Actually Looks

## 1. self.active (Dictionary storage)

```python
self.active = {
    0: {
        'sim_id': 0, 'part_id': 0, 'cycle': 1, 'event_path': 'IC_IZ_FS_FE',
        'fleet_start': 0.0, 'fleet_end': 350.5, 'fleet_duration': 350.5,
        'condition_f_start': 350.5, 'condition_f_end': 352.1, 'condition_f_duration': 1.6,
        'depot_start': 352.1, 'depot_end': 392.1, 'depot_duration': 40.0,
        'condition_a_start': nan, 'condition_a_end': nan, 'condition_a_duration': nan,
        'install_start': nan, 'install_end': nan, 'install_duration': nan,
        'desone_id': 0, 'acone_id': 0, 'destwo_id': nan, 'actwo_id': nan, 'condemn': 'no'
    },
    1: {
        'sim_id': 1, 'part_id': 1, 'cycle': 1, 'event_path': 'IC_IZ_FS_FE',
        'fleet_start': 0.0, 'fleet_end': 420.3, 'fleet_duration': 420.3,
        'condition_f_start': nan, 'condition_f_end': nan, 'condition_f_duration': nan,
        'depot_start': nan, 'depot_end': nan, 'depot_duration': nan,
        'condition_a_start': nan, 'condition_a_end': nan, 'condition_a_duration': nan,
        'install_start': nan, 'install_end': nan, 'install_duration': nan,
        'desone_id': 1, 'acone_id': 1, 'destwo_id': nan, 'actwo_id': nan, 'condemn': 'no'
    }
}
```

## 2. self.part_log (List of completed cycles)

```python
self.part_log = [
    {
        'sim_id': 5, 'part_id': 5, 'cycle': 1, 'event_path': 'AFE_CA_CR',
        'fleet_start': 10.5, 'fleet_end': 360.2, 'fleet_duration': 349.7,
        'condition_f_start': nan, 'condition_f_end': nan, 'condition_f_duration': nan,
        'depot_start': nan, 'depot_end': nan, 'depot_duration': nan,
        'condition_a_start': 360.2, 'condition_a_end': 360.2, 'condition_a_duration': 0.0,
        'install_start': 360.2, 'install_end': 360.2, 'install_duration': 0.0,
        'desone_id': 5, 'acone_id': 5, 'destwo_id': 3, 'actwo_id': 3, 'condemn': 'no'
    },
    {
        'sim_id': 7, 'part_id': 7, 'cycle': 2, 'event_path': 'DE_CA_CR',
        'fleet_start': 360.2, 'fleet_end': 710.8, 'fleet_duration': 350.6,
        'condition_f_start': 710.8, 'condition_f_end': 712.0, 'condition_f_duration': 1.2,
        'depot_start': 712.0, 'depot_end': 752.0, 'depot_duration': 40.0,
        'condition_a_start': 752.0, 'condition_a_end': 752.0, 'condition_a_duration': 0.0,
        'install_start': 752.0, 'install_end': 752.0, 'install_duration': 0.0,
        'desone_id': 8, 'acone_id': 8, 'destwo_id': 9, 'actwo_id': 9, 'condemn': 'no'
    }
]
```

## 3. part_manager.get_part(sim_id) returns

**Input:** `get_part(0)`

**Returns:** Single dictionary record
```python
{
    'sim_id': 0, 'part_id': 0, 'cycle': 1, 'event_path': 'IC_IZ_FS_FE',
    'fleet_start': 0.0, 'fleet_end': 350.5, 'fleet_duration': 350.5,
    'condition_f_start': 350.5, 'condition_f_end': 352.1, 'condition_f_duration': 1.6,
    'depot_start': 352.1, 'depot_end': 392.1, 'depot_duration': 40.0,
    'condition_a_start': nan, 'condition_a_end': nan, 'condition_a_duration': nan,
    'install_start': nan, 'install_end': nan, 'install_duration': nan,
    'desone_id': 0, 'acone_id': 0, 'destwo_id': nan, 'actwo_id': nan, 'condemn': 'no'
}
```

## 4. update_fields(sim_id, updates) - Input and Result

**Input:** `update_fields(0, {'condition_a_start': 392.1, 'condition_a_end': 392.1, 'install_start': 392.1})`

**BEFORE update** - `self.active[0]`:
```python
{
    'sim_id': 0, 'part_id': 0, 'cycle': 1, 'event_path': 'IC_IZ_FS_FE',
    'condition_a_start': nan, 'condition_a_end': nan, 'install_start': nan
    # ... other fields unchanged
}
```

**AFTER update** - `self.active[0]`:
```python
{
    'sim_id': 0, 'part_id': 0, 'cycle': 1, 'event_path': 'IC_IZ_FS_FE',
    'condition_a_start': 392.1, 'condition_a_end': 392.1, 'install_start': 392.1
    # ... other fields unchanged
}
```

## 5. add_initial_part() - Input and Final Record

**Input:** `add_initial_part(part_id=5, cycle=1, micap='IC_IZ_FS_FE', fleet_start=0.0, fleet_end=350.2)`

**Process:**
- Auto-generates sim_id = 5 (from self.next_sim_id)
- Creates complete record with defaults for missing fields

**Final record added to self.active[5]:**
```python
{
    'sim_id': 5, 'part_id': 5, 'cycle': 1, 'event_path': 'IC_IZ_FS_FE',
    'fleet_start': 0.0, 'fleet_end': 350.2, 'fleet_duration': nan,
    'condition_f_start': nan, 'condition_f_end': nan, 'condition_f_duration': nan,
    'depot_start': nan, 'depot_end': nan, 'depot_duration': nan,
    'condition_a_start': nan, 'condition_a_end': nan, 'condition_a_duration': nan,
    'install_start': nan, 'install_end': nan, 'install_duration': nan,
    'desone_id': nan, 'acone_id': nan, 'destwo_id': nan, 'actwo_id': nan, 'condemn': 'no'
}
```

**Returns:** `{'sim_id': 5, 'success': True, 'error': None}`

## 6. get_all_active_parts() returns

**Returns:** Copy of entire self.active dictionary
```python
{
    0: {'sim_id': 0, 'part_id': 0, 'cycle': 1, 'event_path': 'IC_IZ_FS_FE', 'fleet_start': 0.0, ...},
    1: {'sim_id': 1, 'part_id': 1, 'cycle': 1, 'event_path': 'IC_IZ_FS_FE', 'fleet_start': 0.0, ...},
    5: {'sim_id': 5, 'part_id': 5, 'cycle': 1, 'event_path': 'IC_IZ_FS_FE', 'fleet_start': 0.0, ...}
}
```

## 7. export_active_parts() returns

**Returns:** pandas DataFrame of active parts
```
   sim_id  part_id  cycle    micap  fleet_start  fleet_end  fleet_duration  ...
0       0        0      1  IC_IZ_FS_FE          0.0      350.5           350.5
1       1        1      1  IC_IZ_FS_FE          0.0      420.3           420.3  
2       5        5      1  IC_IZ_FS_FE          0.0      350.2             NaN
```

## 8. export_completed_cycles() returns

**Returns:** pandas DataFrame of completed cycles
```
   sim_id  part_id  cycle      micap  fleet_start  fleet_end  fleet_duration  ...
0       5        5      1  AFE_CA_CR         10.5      360.2           349.7
1       7        7      2   DE_CA_CR        360.2      710.8           350.6
```

## 9. get_all_parts_data() - Process and Result

Combines `self.part_log` + `self.active` into single dictionary

**Input sources:**
- `self.part_log` = [completed cycles as shown above]
- `self.active` = {active parts as shown above}

**Process:** Creates all_parts dictionary with ALL sim_ids
```python
all_parts = {
    # From part_log (completed):
    5: {'sim_id': 5, 'part_id': 5, 'cycle': 1, 'event_path': 'AFE_CA_CR', 'fleet_start': 10.5, ...},
    7: {'sim_id': 7, 'part_id': 7, 'cycle': 2, 'event_path': 'DE_CA_CR', 'fleet_start': 360.2, ...},
    # From active (still in progress):
    0: {'sim_id': 0, 'part_id': 0, 'cycle': 1, 'event_path': 'IC_IZ_FS_FE', 'fleet_start': 0.0, ...},
    1: {'sim_id': 1, 'part_id': 1, 'cycle': 1, 'event_path': 'IC_IZ_FS_FE', 'fleet_start': 0.0, ...}
}
```

## 10. get_all_parts_data_df() - Input and Output

**Input:** Uses all_parts dictionary from `get_all_parts_data()`
**Process:** `pd.DataFrame(list(all_parts.values()))`

**Returns:** pandas DataFrame with ALL parts (completed + active)
```
   sim_id  part_id  cycle      micap  fleet_start  fleet_end  fleet_duration  ...
0       5        5      1  AFE_CA_CR         10.5      360.2           349.7   [completed]
1       7        7      2   DE_CA_CR        360.2      710.8           350.6   [completed]  
2       0        0      1    IC_IZ_FS_FE          0.0      350.5           350.5   [active]
3       1        1      1    IC_IZ_FS_FE          0.0      420.3           420.3   [active]
```

