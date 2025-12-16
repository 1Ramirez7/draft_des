# TODO Items


- Explain condition F

## Simulation Logic Documentation


### Extended Simulation Time

**DONE** Added `buffer time` allowing to exclude warmup and closing periods



## Documentation/NOTES/HELP/Q&As

IMPORTANT COMMENT for parts starting `CONDITION F`

Not a current issue but future edits must consider when using depot constraint `heapq`

A. ANY EVENT/FUNCTION that handles parts in CONDITON F pending depot constraint
* Function is atomic to the current state of the sim

B. VIOLATION OF CHRONOLOGICAL MODEL LOGIC
* future part_id's MUST NOT have an earlier cf_start time then those processed in this function call
* IF this rule is broken, the DES model's chronological logic is VIOLATED.
  * So long as we use heapq's FIFO model "First In, First Out" 
    * this must be taken into account. (was a hard bug to find and fix)
* The model can have parts added to conditoon_f_start at any point in the model
  * but they must be process in chronological order to depot constraint

