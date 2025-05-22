from hypothesis import given
from hypothesis.strategies import data
from fuzzer import strategy
from fuzzer.runner import compile_contract
import os

EXAMPLE_CONTRACT = os.path.join(os.path.dirname(__file__), "../examples/Counter.sol")


def test_compile_contract():
    abi, bytecode = compile_contract(EXAMPLE_CONTRACT)
    assert isinstance(abi, list)
    assert isinstance(bytecode, str)
    assert len(bytecode) > 0


# Basic type test
@given(data())
def test_generate_basic_types(data):
    types = ["uint256", "bool", "address"]
    inputs = strategy.generate_inputs(types)
    values = data.draw(inputs)

    assert len(values) == 3
    assert isinstance(values[0], int)
    assert isinstance(values[1], bool)
    assert isinstance(values[2], str)
    assert values[2].startswith("0x")


# Dynamic array test
@given(data())
def test_generate_dynamic_array(data):
    types = ["uint256[]"]
    inputs = strategy.generate_inputs(types)
    values = data.draw(inputs)

    assert isinstance(values[0], list)
    assert all(isinstance(x, int) for x in values[0])


# Static array test
@given(data())
def test_generate_static_array(data):
    types = ["bool[3]"]
    inputs = strategy.generate_inputs(types)
    values = data.draw(inputs)

    assert isinstance(values[0], list)
    assert len(values[0]) == 3
    assert all(isinstance(x, bool) for x in values[0])
