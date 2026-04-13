from enum import IntEnum
from hypothesis import strategies as st, given
from semantic_state_machine import StateMachine
from semantic_state_machine_graphable import StateMachineGraph


# Strategy to create arbitrary IntEnum classes at runtime
def enum_strategy(name: str):
    return st.builds(
        lambda members: IntEnum(name, members),
        st.fixed_dictionaries({f"member_{i}": st.just(i) for i in range(1, 5)}),
    )


# Strategy for the State Machine itself
@st.composite
def state_machine_strategy(draw):
    StateEnum = draw(enum_strategy("State"))
    EventEnum = draw(enum_strategy("Event"))

    sm = StateMachine[StateEnum, EventEnum, None]()

    # Generate transitions
    num_transitions = draw(st.integers(min_value=1, max_value=10))
    for _ in range(num_transitions):
        from_s = draw(st.sampled_from(list(StateEnum)))
        to_s = draw(st.sampled_from(list(StateEnum)))
        event = draw(st.sampled_from(list(EventEnum)))

        # Avoid creating duplicate transitions
        if (from_s, event) not in sm.transitions:
            sm.add_transition(from_s, event, to_s, lambda ctx: None)

    return sm


@given(state_machine_strategy())
def test_graph_properties(sm):
    # Property 1: Graph generation should never raise an exception
    graph = StateMachineGraph(sm)

    # Property 2: Every transition in the SM must exist as an edge in the graph
    for (from_state, _), (to_state, _) in sm.transitions:
        assert from_state in graph
        assert to_state in graph
