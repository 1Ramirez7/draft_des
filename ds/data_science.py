import pandas as pd
import matplotlib.pyplot as plt


class DataSets:
    """
    Container for post-simulation datasets ready for data science/analysis.
    Created after simulation finishes.

    TLDR Implementation Steps:
    1. Created DataSets class in ds/data_science.py with build_part_ac_df method.
    2. simulation_engine.py: Added datasets parameter to __init__, set self.datasets = datasets, called build_part_ac_df in run().
    3. main.py: Added import 'from ds.data_science import DataSets'.
    4. main.py: Created 'datasets = DataSets()' after df_manager creation.
    5. main.py: Added 'datasets=datasets' to SimulationEngine call.
    6. main.py: Updated Excel export to use 'datasets.all_parts_df' and 'datasets.aircraft_df'.
    """
    def __init__(self, warmup_periods, closing_periods, sim_time, use_buffer=False):
        self.all_parts_df = None
        self.all_ac_df = None
        self.wip_df = None
        self.wip_raw = None
        self.wip_ac_df = None
        self.wip_ac_raw = None
        self.warmup_periods = warmup_periods
        self.closing_periods = closing_periods
        self.sim_time = sim_time
        self.use_buffer = use_buffer
        self.interval = 1
        # Add more datasets as needed

    def build_part_ac_df(self, get_all_parts_data_df, get_ac_df_func,
                         get_wip_end, get_wip_raw,
                         get_wip_ac_end, get_wip_ac_raw,
                         sim_time):
        """
        Populate datasets at end of simulation (end of engine.run).
        If use_buffer is True, applies filter_by_remove_days to remove warmup/closing periods.
        """
        self.all_parts_df = get_all_parts_data_df()
        self.all_ac_df = get_ac_df_func()
        self.wip_df = get_wip_end(sim_time, self.interval)
        self.wip_raw = get_wip_raw()
        self.wip_ac_df = get_wip_ac_end(sim_time, self.interval)
        self.wip_ac_raw = get_wip_ac_raw()
        
        # Only filter if buffer time is enabled
        if self.use_buffer:
            self.filter_by_remove_days()

    def filter_by_remove_days(self):
        """
        Filter out rows where the earliest start time > remove_days or < warmup_periods.
        
        For parts: Uses the earliest available start time (fleet_start, depot_start, 
        condition_f_start, or condition_a_start) since parts may not all start in fleet.
        For aircraft: Uses the earliest available start time (fleet_start or micap_start).
        """
        import pandas as pd
        
        remove_days = self.sim_time - self.closing_periods
        
        # Get the minimum start time for each PART
        start_cols = ['fleet_start', 'depot_start', 'condition_f_start', 'condition_a_start']
        earliest_start = self.all_parts_df[start_cols].min(axis=1)
        
        self.all_parts_df = self.all_parts_df[
            (earliest_start >= self.warmup_periods) & 
            (earliest_start <= remove_days)]
        
        # # Get the minimum start time for each AIRCRAFT
        start_cols = ['fleet_start', 'micap_start']
        earliest_start = self.all_ac_df[start_cols].min(axis=1)
        
        self.all_ac_df = self.all_ac_df[
            (earliest_start >= self.warmup_periods) & 
            (earliest_start <= remove_days)]
        
        # WIP data filtering remains the same (based on sim_time)
        self.wip_df = self.wip_df[(self.wip_df['sim_time'] >= self.warmup_periods) & (self.wip_df['sim_time'] <= remove_days)]
        self.wip_raw = self.wip_raw[(self.wip_raw['sim_time'] >= self.warmup_periods) & (self.wip_raw['sim_time'] <= remove_days)]
        self.wip_ac_df = self.wip_ac_df[(self.wip_ac_df['sim_time'] >= self.warmup_periods) & (self.wip_ac_df['sim_time'] <= remove_days)]
        self.wip_ac_raw = self.wip_ac_raw[(self.wip_ac_raw['sim_time'] >= self.warmup_periods) & (self.wip_ac_raw['sim_time'] <= remove_days)]

