# Development Guide

## Setup

### Prerequisites

- Python 3.12+
- Git
- VS Code (recommended)

### Initial Setup

1. Clone the repository
2. Create virtual environment: `py -3.12 -m venv .venv`
3. Activate environment: `.venv\Scripts\activate` (PowerShell) or `source .venv/Scripts/activate` (Git Bash)
4. Install dependencies: `pip install -r requirements.txt`

### VS Code Configuration

Create `.vscode/settings.json`:

```json
{
  "python.defaultInterpreterPath": "C:/path/to/fa25_hafb/.venv/Scripts/python.exe",
  "python.terminal.activateEnvironment": true
}
```

**IMPORTANT**: Update the path to match your local repository location.

## Project Structure

```
fa25_hafb/
├── main.py                  # Landing page (entry point)
├── run_streamlit_app.py     # Application launcher
├── simulation_engine.py     # Core simulation logic
├── initialization.py        # Initial conditions setup
├── parameters.py            # Centralized parameter management
├── post_sim.py              # Post-simulation handling
├── entity_part.py           # PartManager class
├── entity_ac.py             # AircraftManager class
├── ph_micap.py              # MicapState class
├── ph_cda.py                # ConditionAState class
├── ph_new_part.py           # NewPart class
├── session_manager.py       # Streamlit session handling
├── utils.py                 # Utility functions
├── sc_utils.py              # Scenario utilities
├── pages/                   # Streamlit pages
│   ├── solo_run.py          # Single simulation page
│   └── scenarios.py         # Multiple simulation scenarios page
├── ds/                      # Data science modules
│   ├── __init__.py
│   ├── data_science.py      # DataSets class
│   └── helpers.py           # Helper functions
├── ui/                      # UI components
│   ├── ui_components.py     # Solo Run sidebar widgets
│   ├── dist_plots.py        # Distribution plots
│   ├── wip_plots.py         # WIP plots
│   ├── stats.py             # Statistics display
│   ├── downloads.py         # Export functionality
│   ├── sc_sidebar.py        # Scenarios sidebar
│   ├── sc_loop.py           # Scenario loop controls
│   ├── sc_results.py        # Scenario results display
│   └── sc_tabs.py           # Scenario tabs
├── docs/                    # Documentation
│   ├── architecture.md      # System architecture
│   ├── flowchart.md         # Business logic diagrams
│   ├── uml-classes.md       # Class structure
│   ├── event_type.md        # Event naming reference
│   ├── user-guide.md        # User documentation
│   └── reference/           # Code reference materials
├── tests/                   # Test files
│   └── test_simulation.py   # Simulation validation tests
└── requirements.txt         # Dependencies
```

## Code Style

### Python Style

- Follow PEP 8
- Use type hints where possible
- Preserve existing code patterns

### Documentation

- Use Google-style docstrings
- Document complex logic
- Keep comments concise

### Naming Conventions

- Variables: `snake_case`
- Classes: `PascalCase`
- Constants: `UPPER_SNAKE_CASE`

## Testing

### Running Validation Tests

```bash
python tests/test_simulation.py
```

Or from project root:

```bash
python _test_simulation.py
```

### Test Structure

The test file runs a complete simulation and validates:
- Timing consistency (fleet/depot/install durations)
- ID uniqueness (no duplicate sim_id, des_id)
- Continuity checks (fleet_start = previous install_end)
- Cycle limits (parts not exceeding condemn cycle)

## Adding Features

### Adding New Parameters

1. Add to `PARAM_METADATA` in `parameters.py`
2. Add UI input in `ui/ui_components.py`
3. Use via `params['param_name']` in engine

### Adding New Event Types

1. Add event handler method in `simulation_engine.py`
2. Schedule event with `schedule_event(time, 'event_name', entity_id)`
3. Add case in main event loop in `run()`
4. Document in `docs/event_type.md`

## Debugging

**Common Issues**:
- Virtual env not activated (check VS Code interpreter)
- Import errors (ensure project root in path)
- Simulation errors (check parameters, run validation tests)

**Tools**:
- VS Code debugger
- Print statements
- Streamlit error display
- Validation functions in test file

**Check Python Environment**:
```bash
python --version
which python   # Git Bash
Get-Command python   # PowerShell
```

## Performance

- Dictionary-based entity tracking (O(1) lookups)
- Complexity: O(events × log(events)) for priority queue operations

## Documentation

Keep docs in sync with code:
- `README.md` - Quick start
- `docs/` - Detailed documentation
- Code docstrings - API reference
