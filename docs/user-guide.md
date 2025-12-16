# User Guide

## Quick Start

```bash
cd streamlit_app
python run_streamlit_app.py
```

Opens at `http://localhost:8501`

## Using the Application

The application has two modes accessible from the landing page:

- **Solo Run**: Run a single simulation with full visualization and detailed results
- **Scenarios**: Run multiple simulations varying parameters (separate documentation)

## Using Solo Run

Navigate to Solo Run, configure parameters in the sidebar, then click **"Run Simulation"**.

### Basic Parameters

| Parameter | Description |
|-----------|-------------|
| Total Parts | Number of parts in the system |
| Total Aircraft | Number of aircraft in the fleet |
| Simulation Time (days) | Duration of simulation |
| Depot Capacity | Max parts that can be repaired simultaneously |
| Random Seed | For reproducibility |
| Mission Capable Rate | Target percentage of aircraft with parts |

### Initial Allocation

| Parameter | Description |
|-----------|-------------|
| Parts in Depot | Parts starting in repair |
| Parts in Condition F | Parts starting in failure queue |
| Parts in Condition A | Parts starting in available inventory |

### Stage Durations

**Fleet Stage** (time part operates on aircraft):
- Distribution: Normal or Weibull
- Mean/Shape parameter
- Std Dev/Scale parameter

**Depot Stage** (repair time):
- Distribution: Normal or Weibull
- Mean/Shape parameter
- Std Dev/Scale parameter

### Condemnation Parameters

| Parameter | Description |
|-----------|-------------|
| Condemn at Cycle | Cycle count when part is condemned |
| Depot Time Fraction | Fraction of depot time before condemn decision |
| Part Order Lag (days) | Lead time for replacement part |

## Results Displayed

### Statistics Tab
- Total event counts by type
- Row counts for output DataFrames

### Simulation Results Tab
- Sample data (first rows of each DataFrame)
- Duration distribution plots

### WIP Plots Tab
- Work-in-progress over simulation time
- MICAP count over time
- Parts in each stage over time

## Export

Click **"Download Results"** to export:
- `all_parts_df` - Complete part event log
- `all_ac_df` - Complete aircraft event log
- `wip_df` - Work-in-progress history
- Parameters used

### Output Columns

**all_parts_df** (Part Event Log):

| Column | Description |
|--------|-------------|
| `sim_id` | Unique event ID |
| `part_id` | Part identifier |
| `cycle` | Current cycle number |
| `fleet_start`, `fleet_end` | Fleet stage times |
| `condition_f_start`, `condition_f_end` | Condition F times |
| `depot_start`, `depot_end` | Depot repair times |
| `condition_a_start`, `condition_a_end` | Available inventory times |
| `install_start`, `install_end` | Installation times |
| `desone_id`, `acone_id` | Aircraft at fleet start |
| `destwo_id`, `actwo_id` | Aircraft at install |
| `condemn` | Whether part was condemned |

**all_ac_df** (Aircraft Event Log):

| Column | Description |
|--------|-------------|
| `des_id` | Unique event ID |
| `ac_id` | Aircraft identifier |
| `fleet_start`, `fleet_end` | Fleet operation times |
| `micap_start`, `micap_end` | MICAP waiting times |
| `install_start`, `install_end` | Installation times |
| `partone_id`, `parttwo_id` | Part IDs (before/after) |
| `simone_id`, `simtwo_id` | Part event IDs |

## Tips & FAQ

### Tips
- Use the same random seed for reproducibility when comparing scenarios
- Start with shorter simulation times for initial testing
- Verify initial allocation parameters sum correctly before running

### FAQ

| Question | Answer |
|----------|--------|
| Why is simulation slow? | Larger simulations (more parts, longer time) require more computation. This is expected behavior. |
| Results don't match expectations? | Verify parameter values match your intended configuration. Check that initial allocation (parts in depot, Condition F, Condition A) is set correctly. |
| Application shows error/stops responding? | Streamlit has memory limits. Very large simulations may exceed available memory. If this occurs, reduce simulation size. Exports will work if the simulation completes successfully. |
