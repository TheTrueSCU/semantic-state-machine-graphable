from enum import Enum, auto
from semantic_state_machine import AuditedStateMachine, AuditContext
from semantic_state_machine_graphable.graph import StateMachineGraph, AuditContextGraph


class TrafficLightState(Enum):
    RED = auto()
    GREEN = auto()
    YELLOW = auto()


class TrafficLightEvent(Enum):
    NEXT = auto()


def test_traffic_light_lifecycle():
    # 1. Setup State Machine
    sm = AuditedStateMachine[
        TrafficLightState,
        TrafficLightEvent,
        AuditContext[TrafficLightState, TrafficLightEvent],
    ]()

    @sm.transition(
        TrafficLightState.RED, TrafficLightEvent.NEXT, TrafficLightState.GREEN
    )
    def to_green(ctx):
        pass

    @sm.transition(
        TrafficLightState.GREEN, TrafficLightEvent.NEXT, TrafficLightState.YELLOW
    )
    def to_yellow(ctx):
        pass

    @sm.transition(
        TrafficLightState.YELLOW, TrafficLightEvent.NEXT, TrafficLightState.RED
    )
    def to_red(ctx):
        pass

    # 2. Visualize State Machine Structure
    structure_graph = StateMachineGraph(sm)
    assert len(structure_graph) == 3
    for state in TrafficLightState:
        assert state in structure_graph

    # Check edges in structure
    assert (
        structure_graph[TrafficLightState.GREEN]
        in structure_graph[TrafficLightState.RED].dependents
    )
    assert (
        structure_graph[TrafficLightState.YELLOW]
        in structure_graph[TrafficLightState.GREEN].dependents
    )
    assert (
        structure_graph[TrafficLightState.RED]
        in structure_graph[TrafficLightState.YELLOW].dependents
    )

    # 3. Execute transitions
    ctx = AuditContext[TrafficLightState, TrafficLightEvent]()

    state = TrafficLightState.RED
    state = sm.handle_transition(ctx, state, TrafficLightEvent.NEXT)  # -> GREEN (1)
    state = sm.handle_transition(ctx, state, TrafficLightEvent.NEXT)  # -> YELLOW (2)
    state = sm.handle_transition(ctx, state, TrafficLightEvent.NEXT)  # -> RED (3)
    state = sm.handle_transition(ctx, state, TrafficLightEvent.NEXT)  # -> GREEN (4)

    # 4. Visualize Execution Path
    execution_graph = AuditContextGraph(ctx, sm)
    assert len(execution_graph) == 3  # RED, GREEN, YELLOW

    # Check execution path annotations
    # RED -> GREEN happened at index 1 and 4
    red_to_green = execution_graph[TrafficLightState.RED].edge_attributes(
        execution_graph[TrafficLightState.GREEN]
    )
    assert sorted(red_to_green["indices"]) == [1, 4]

    # GREEN -> YELLOW happened at index 2
    green_to_yellow = execution_graph[TrafficLightState.GREEN].edge_attributes(
        execution_graph[TrafficLightState.YELLOW]
    )
    assert green_to_yellow["indices"] == [2]

    # YELLOW -> RED happened at index 3
    yellow_to_red = execution_graph[TrafficLightState.YELLOW].edge_attributes(
        execution_graph[TrafficLightState.RED]
    )
    assert yellow_to_red["indices"] == [3]
