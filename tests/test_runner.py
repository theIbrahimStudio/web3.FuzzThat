from fuzzer import strategy
from fuzzer.runner import compile_contract
import os

EXAMPLE_CONTRACT = os.path.join(os.path.dirname(__file__), "../examples/Counter.sol")


def test_compile_contract():
    abi, bytecode = compile_contract(EXAMPLE_CONTRACT)
    assert isinstance(abi, list)
    assert isinstance(bytecode, str)
    assert len(bytecode) > 0


def test_generate_inputs_basic_types():
    types = ["uint256", "int128", "bool", "address", "string"]
    inputs = strategy.generate_inputs(types)
    assert len(inputs) == len(types)
    assert isinstance(inputs[0], int)
    assert isinstance(inputs[1], int)
    assert isinstance(inputs[2], bool)
    assert isinstance(inputs[3], str) and inputs[3].startswith("0x")
    assert isinstance(inputs[4], str)


def test_generate_inputs_unsupported_type():
    types = ["bytes32"]
    inputs = strategy.generate_inputs(types)
    assert inputs[0] is None
