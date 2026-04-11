from enum import Enum
from typing import TypeVar
from state_machine import StateMachine, AuditContext
from graphable import Graph, Graphable

S = TypeVar("S", bound=Enum)
E = TypeVar("E", bound=Enum)
C = TypeVar("C")


class StateNode[S: Enum](Graphable[S]):
    """A node in the graph representing a state.

    Args:
        state: The Enum value representing the state.
    """

    def __init__(self, state: S):
        super().__init__(state)


class StateMachineGraph[S: Enum, E: Enum, C](Graph[StateNode[S]]):
    """A graph representation of a StateMachine's structure.

    Args:
        sm: The StateMachine instance to visualize.

    Notes:
        Architectural Intent: Provides a static view of all possible
        transitions defined in the state machine.
    """

    def __init__(self, sm: StateMachine[S, E, C]):
        super().__init__()
        self._sm = sm
        self._sync()

    def _get_or_create_node(self, state: S) -> StateNode[S]:
        """Retrieves an existing node for a state or creates a new one."""
        try:
            return self[state]
        except KeyError:
            node = StateNode(state)
            self.add_node(node)
            return node

    def _sync(self):
        """Builds the Graph from the StateMachine's transitions."""
        for (from_state, event), (to_state, _) in self._sm._transitions.items():
            u = self._get_or_create_node(from_state)
            v = self._get_or_create_node(to_state)

            if v in u.dependents:
                attrs = u.edge_attributes(v)
                events = attrs.get("events", [])
                if event not in events:
                    events.append(event)
                u.set_edge_attribute(v, "events", events)
                u.set_edge_attribute(v, "label", ", ".join(e.name for e in events))
            else:
                u.add_dependent(v, events=[event], label=event.name)


class AuditContextGraph[S: Enum, E: Enum, C](Graph[StateNode[S]]):
    """A graph representation of the execution path recorded in an AuditContext.

    Args:
        ctx: The AuditContext instance to visualize.
        sm: Optional StateMachine instance to resolve target states.
            If not provided, target states are inferred from the next entry
            in the audit log, meaning the final transition's target state
            cannot be determined.

    Notes:
        Architectural Intent: Visualizes the actual sequence of states
        visited. Edges are annotated with the sequence of 1-based indices
        from the audit log.
    """

    def __init__(
        self, ctx: AuditContext[S, E], sm: StateMachine[S, E, C] | None = None
    ):
        super().__init__()
        self._ctx = ctx
        self._sm = sm
        self._sync()

    def _get_or_create_node(self, state: S) -> StateNode[S]:
        """Retrieves an existing node for a state or creates a new one."""
        try:
            return self[state]
        except KeyError:
            node = StateNode(state)
            self.add_node(node)
            return node

    def _sync(self):
        """Builds the Graph from the AuditContext's history."""
        audit_data = self._ctx._audit
        for i in range(len(audit_data)):
            from_state, event = audit_data[i]

            to_state = None
            if self._sm:
                # Use StateMachine to find to_state
                try:
                    to_state, _ = self._sm._next_transition(from_state, event)
                except Exception:
                    # If SM doesn't have it, try fallback to inference
                    pass

            if to_state is None and i + 1 < len(audit_data):
                # Fallback to inference from next state
                to_state = audit_data[i + 1][0]

            if to_state is None:
                continue

            u = self._get_or_create_node(from_state)
            v = self._get_or_create_node(to_state)

            # The user requested "index (plus one)" which matches 1-based indexing.
            index = i + 1

            if v in u.dependents:
                attrs = u.edge_attributes(v)
                indices = attrs.get("indices", [])
                indices.append(index)
                u.set_edge_attribute(v, "indices", indices)
                u.set_edge_attribute(
                    v, "label", f"{event.name} ({', '.join(map(str, indices))})"
                )
            else:
                u.add_dependent(v, indices=[index], label=f"{event.name} ({index})")
