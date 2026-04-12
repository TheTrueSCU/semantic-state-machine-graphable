# semantic-state-machine-graphable

A library for visualizing `semantic-state-machine` structures and `AuditContext` execution paths as graphs using `graphable`.

## Features
- **StateMachineGraph**: Visualize the static structure of a `semantic-state-machine.StateMachine`.
- **AuditContextGraph**: Visualize the execution history of an `AuditContext` as a graph, with edges annotated by transition indices.

## Installation

### For Development
The project is managed with `uv`. To install dependencies:
```bash
uv sync
```

### From PyPI
```bash
pip install semantic-state-machine-graphable
```

## Testing
The project uses `pytest` for testing. Run the test suite with coverage reporting:
```bash
PYTHONPATH=src uv run pytest --cov=semantic_state_machine_graphable --cov-report=term-missing
```

## Usage

### State Machine Visualization
```python
from semantic_state_machine import StateMachine
from semantic_state_machine_graphable.graph import StateMachineGraph

sm = StateMachine(...)
sm.add_transition(...)

graph = StateMachineGraph(sm)
# Now visualize or export the graph
```

### Execution Path Visualization
```python
from semantic_state_machine import AuditedStateMachine, AuditContext
from semantic_state_machine_graphable.graph import AuditContextGraph

sm = AuditedStateMachine(...)
ctx = AuditContext(...)
# ... execute transitions ...

graph = AuditContextGraph(ctx, sm)
# Now visualize or export the execution path graph
```

## License
This project is licensed under the MIT License.
