

# Steps for Adding New User Input to ui_components.py for use in calculate_initial_allocation():
 
"""
Steps for adding new user input that feeds into utils.py - calculate_initial_allocation():

1. Add user input in `ui_components.py`:
   - Add st.sidebar.number_input() (or other input widget)
   - Add to return dict at end of render_sidebar()

2. Update `utils.py` - calculate_initial_allocation():
   - Add new parameter to function signature
   - Update docstring with parameter description
   - Use parameter in function logic (if needed for calculations)
   - Add to return dict (if this value needs to be returned)

3. Update `main.py`:
   - Pass new parameter from params dict to calculate_initial_allocation()
   - Example: new_param=params['new_param']

4. Update `test_simulation.py`:
   - Add hardcoded value for new parameter
   - Pass hardcoded value to calculate_initial_allocation()
   - Example: new_param=5
"""

# Steps for Adding New UI Rendering Function (like render_allocation_inputs):
"""
Steps for adding a new UI rendering function to be called in ui_components.py:

1. Write function in `utils.py`:
   - Function signature: def render_function_name(param1, param2, ...):
   - Import streamlit as st inside function
   - Import numpy as np inside function (if needed)
   - Add all st.sidebar.* calls for that UI section
   - Return tuple or dict of values collected from UI inputs
   - Add docstring explaining parameters and return values

2. Update `ui_components.py` - render_sidebar():
   - Import the new function: from utils import render_function_name
   - Calculate any required input values the function needs
   - Call function and capture return values
   - Example: value1, value2 = render_function_name(param1, param2)
   - Add returned values to the return dict at end of render_sidebar()

3. Update `main.py` (if needed):
   - Usually no changes needed if values are in params dict
   - Pass new params to downstream functions as needed

4. Update `test_simulation.py` (if needed):
   - Add hardcoded values for any new parameters
   - Test file skips UI functions entirely, uses manual values

Note: UI rendering functions keep ui_components.py clean by grouping related 
UI elements together. The function can be reused anywhere UI is needed.
"""

