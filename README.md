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
The project employs a tiered testing strategy:
- **Unit & Integration:** Run with `pytest`.
- **Property-based Fuzzing:** Run with `pytest tests/hypothesis`. These are powered by `hypothesis` and provide robust edge-case coverage.

Run the full test suite:
```bash
uv run pytest tests
```

## Usage

### State Machine Visualization
```python
from semantic_state_machine_graphable import StateMachineGraph

graph = StateMachineGraph(sm)
# Export to DOT format
dot_output = graph.to_dot()
print(dot_output)

# To visualize with Graphviz, you can use the command line:
# echo '...' | dot -Tpng -o state_machine.png
```

### Execution Path Visualization
```python
from semantic_state_machine_graphable import AuditContextGraph

graph = AuditContextGraph(ctx, sm)
# Export to DOT format
dot_output = graph.to_dot()
print(dot_output)

# To visualize with Graphviz:
# echo '...' | dot -Tpng -o audit_path.png
```

## License
This project is licensed under the MIT License.
