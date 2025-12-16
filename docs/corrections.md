

`file`

# Development Guide

- see if we have time to update this file as it is missing a lot of information

## Git Workflow
- LLM was hollucinating and made up branches that never existed 
- it looks like this section was LLM generated pointing to nothing specific in our repo

- development.md has very little information, if have time work on this


``file``

## Mathematical Specification

### Parameters 
- section is not updated. (has old params)

### 3.1 Depot Capacity Constraint
- error in format

Implementation Note: This is not a classical M/M/c queue because:
- no reason to include this. 


### 3.3 Condition A Inventory
- error in latex formula

### 4.4 Transition Probabilities
Most transitions are deterministic given the current state. The only stochastic element is the duration of each state, not the destination.

- We should specify and not use "Most transitions". Documentation here
- this is a documentation file so its here they know which are deterministic, not find "Most"

### 5.2 Condition F Timing (Depot Wait)
- then >= 0 is not needed. 
- A message saying D_CF will always be zero if depot has capacity at cdf_start


## 7. Conservation Laws
- error in latex formula


### 8.2 Event Priority
- need to explain as this is the BRAIN of the model


### 8.3 Main Loop
- need to explain as this is the BRAIN of handling all schedule events



## 11. Weibull Distribution Notes

- Change this to relate to our model not infant mortality failure



`file`

## simulation-methodology.md 

incorrect secitons: 

| **Condition F** | Failure detection/removal | Instant (duration = 0) |

- Leftover parts start in Condition A or other stages (partially wrong)


`file`

user-guide.md can be updated. 
- some tips are for developers beyond control of streamlit interface
- some error checking is not ideal "Unexpected results"
  - I guess this is more of not getting expected results because incorrect user inputs were used
    - unrelated to troubleshooting?
- "Slow simulation" 
  - Unrelated to the model, more like Q&A why model is taking longer
- "Export issues" 
  - Streamlit will disable the app if memory limit is reached
    - app will display 404 type error letting user know memory limit was hit
  - This will happen during simulation and or post-processing 
    - If the simulation finishes then export should always work
  - This can be misleading if there is an actual error with exports
- "Import errors" - This is more from a developers perspective 
  - common issues mix with user-dummy-proofing and developer level issues 
    - import libraries will only happen file edits required import edits
      - so if import issue made it to deployment, dev did not test the code b/ deploying