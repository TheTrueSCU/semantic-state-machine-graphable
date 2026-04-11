# state-machine-graphable

A library for visualizing `state-machine` structures and `AuditContext` execution paths as graphs using `graphable`.

## Features
- **StateMachineGraph**: Visualize the static structure of a `state-machine.StateMachine`.
- **AuditContextGraph**: Visualize the execution history of an `AuditContext` as a graph, with edges annotated by transition indices.

## Installation
The project is managed with `uv`. To install dependencies:
```bash
uv sync
```

## Testing
The project uses `pytest` for testing. Run the test suite with coverage reporting:
```bash
PYTHONPATH=src uv run pytest --cov=state_machine_graphable --cov-report=term-missing
```

## Usage

### State Machine Visualization
```python
from state_machine import StateMachine
from state_machine_graphable.graph import StateMachineGraph

sm = StateMachine(...)
sm.add_transition(...)

graph = StateMachineGraph(sm)
# Now visualize or export the graph
```

### Execution Path Visualization
```python
from state_machine import AuditedStateMachine, AuditContext
from state_machine_graphable.graph import AuditContextGraph

sm = AuditedStateMachine(...)
ctx = AuditContext(...)
# ... execute transitions ...

graph = AuditContextGraph(ctx, sm)
# Now visualize or export the execution path graph
```
