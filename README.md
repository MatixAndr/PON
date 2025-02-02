# Python Object Notation

PON - Python Object Notation is a better JSON made for Python

## TODO / Feature List

- [ ] Dynamic Dates (`date.dynamic`)
  - Changes date with every read.
  - Mathematical operations on dates (e.g., `1d+1mo+1y-3mo`).
  
- [ ] Static Dates (`date.static`)
  - A fixed date that does not change once saved.

- [ ] Support for Date Operations
  - Add an `offset` argument to `date.dynamic` for performing operations.

- [ ] Two Date Modes: Dynamic and Static
  - `date.dynamic` – changes with every read.
  - `date.static` – remains unchanged.

- [ ] Support for Python Objects (`obj()`, `class()`)
  - Serialization of Python objects and their instances.

- [ ] Support for Aliases (`alias()`)
  - References to other objects to save memory.

- [ ] Cyclic References (`ref()`)
  - Prevent infinite recursion with references.
  - Implement `max_depth` and lazy evaluation.

- [ ] Support for Expressions (`expr()`)
  - Ability to perform mathematical operations in data.

- [ ] Support for Binary, Decimal, and UUID Types
  - Types: `bytes()`, `decimal()`, `uuid()`.

- [ ] JSON Compatibility Mode (`pon_mode: "json_compatible"`)
  - Export to JSON format.

- [ ] Macros (`macro()`)
  - Definitions of reusable data.

- [ ] Lazy Loading of Data
  - Load data only when it's actually needed.

- [ ] Checkpoints
  - Define checkpoints using the syntax `"$= name here =$"`.
  - Checkpoints allow loading only specific data from memory.

- [ ] Lazy Evaluation and Cycle Prevention in `ref()`
  - Prevent infinite cycles.
