from enum import Enum, auto
from semantic_state_machine import StateMachine, AuditContext
from semantic_state_machine_graphable.graph import (
    StateNode,
    StateMachineGraph,
    AuditContextGraph,
)


class State(Enum):
    A = auto()
    B = auto()


class Event(Enum):
    E1 = auto()


def test_state_node_initialization():
    node = StateNode(State.A)
    assert node.reference == State.A


def test_state_machine_graph_sync():
    sm = StateMachine[State, Event, None]()
    sm.add_transition(State.A, Event.E1, State.B, lambda ctx: None)

    graph = StateMachineGraph(sm)
    assert len(graph) == 2
    assert State.A in graph
    assert State.B in graph

    node_a = graph[State.A]
    node_b = graph[State.B]
    assert node_b in node_a.dependents

    attrs = node_a.edge_attributes(node_b)
    assert attrs["events"] == [Event.E1]
    assert attrs["label"] == "E1"


def test_audit_context_graph_sync():
    ctx = AuditContext[State, Event]()
    # Manually populate audit to test AuditContextGraph without SM
    ctx.record_transition(State.A, Event.E1)
    # To infer to_state, we need a second entry
    ctx.record_transition(State.B, Event.E1)

    graph = AuditContextGraph(ctx)
    # Should have inferred A -> B from the audit log
    assert len(graph) == 2
    assert State.A in graph
    assert State.B in graph

    node_a = graph[State.A]
    node_b = graph[State.B]
    assert node_b in node_a.dependents
    assert node_a.edge_attributes(node_b)["indices"] == [1]


def test_state_machine_graph_multiple_events():
    StateMachine[State, Event, None]()

    class Event2(Enum):
        E1 = auto()
        E2 = auto()

    # We need to use the same enum for the test to work cleanly with StateMachineGraph
    class MultiEvent(Enum):
        E1 = auto()
        E2 = auto()

    sm2 = StateMachine[State, MultiEvent, None]()
    sm2.add_transition(State.A, MultiEvent.E1, State.B, lambda ctx: None)
    sm2.add_transition(State.A, MultiEvent.E2, State.B, lambda ctx: None)

    graph = StateMachineGraph(sm2)
    node_a = graph[State.A]
    node_b = graph[State.B]

    attrs = node_a.edge_attributes(node_b)
    assert MultiEvent.E1 in attrs["events"]
    assert MultiEvent.E2 in attrs["events"]
    assert "E1, E2" in attrs["label"] or "E2, E1" in attrs["label"]


def test_audit_context_graph_with_sm():
    sm = StateMachine[State, Event, None]()
    sm.add_transition(State.A, Event.E1, State.B, lambda ctx: None)

    ctx = AuditContext[State, Event]()
    ctx.record_transition(State.A, Event.E1)

    graph = AuditContextGraph(ctx, sm)
    assert len(graph) == 2
    assert graph[State.B] in graph[State.A].dependents


def test_audit_context_graph_sm_exception_path():
    sm = StateMachine[State, Event, None]()
    # No transitions added to sm

    ctx = AuditContext[State, Event]()
    ctx.record_transition(State.A, Event.E1)
    ctx.record_transition(State.B, Event.E1)

    # sm._next_transition(State.A, Event.E1) will raise InvalidTransition
    # which is caught and falls back to inference
    graph = AuditContextGraph(ctx, sm)
    assert len(graph) == 2
    assert graph[State.B] in graph[State.A].dependents


def test_state_machine_graph_with_cycle():
    sm = StateMachine[State, Event, None]()
    sm.add_transition(State.A, Event.E1, State.B, lambda ctx: None)
    sm.add_transition(State.B, Event.E1, State.A, lambda ctx: None)

    # Should not raise GraphCycleError now that we use CyclicGraph
    graph = StateMachineGraph(sm)
    assert len(graph) == 2
    assert State.A in graph
    assert State.B in graph
