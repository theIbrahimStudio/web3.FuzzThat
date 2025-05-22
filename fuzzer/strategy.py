from hypothesis import strategies as st
import re


def generate_inputs(input_types):
    return st.tuples(*(get_strategy(t) for t in input_types))


def get_strategy(solidity_type: str):
    # Handle dynamic arrays: e.g., uint256[]
    if match := re.match(r"^(.+)\[\]$", solidity_type):
        base_type = match.group(1)
        return st.lists(get_strategy(base_type), min_size=0, max_size=5)

    # Handle static arrays: e.g., uint256[3]
    if match := re.match(r"^(.+)\[(\d+)\]$", solidity_type):
        base_type = match.group(1)
        length = int(match.group(2))
        return st.lists(get_strategy(base_type), min_size=length, max_size=length)

    # Handle base types
    if solidity_type.startswith("uint"):
        bits = int(solidity_type[4:]) if len(solidity_type) > 4 else 256
        return st.integers(min_value=0, max_value=2**bits - 1)

    if solidity_type.startswith("int"):
        bits = int(solidity_type[3:]) if len(solidity_type) > 3 else 256
        return st.integers(min_value=-(2 ** (bits - 1)), max_value=2 ** (bits - 1) - 1)

    if solidity_type == "bool":
        return st.booleans()

    if solidity_type == "address":
        return st.text(alphabet="0123456789abcdef", min_size=40, max_size=40).map(
            lambda x: "0x" + x
        )

    if solidity_type.startswith("bytes") and solidity_type != "bytes":
        size = int(solidity_type[5:])
        return st.binary(min_size=size, max_size=size)

    if solidity_type == "string":
        return st.text(min_size=0, max_size=50)

    if solidity_type == "bytes":
        return st.binary(min_size=0, max_size=50)

    raise ValueError(f"Unsupported type: {solidity_type}")
