from web3 import Web3
from fuzzer.strategy import generate_inputs
from fuzzer.state_tracker import get_state, compare_state


def compile_contract(source_path):
    from solcx import compile_standard, install_solc

    install_solc("0.8.20")
    with open(source_path, "r") as file:
        source = file.read()
    compiled = compile_standard(
        {
            "language": "Solidity",
            "sources": {"Contract.sol": {"content": source}},
            "settings": {
                "outputSelection": {
                    "*": {"*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]}
                }
            },
        },
        solc_version="0.8.20",
    )
    contract_name = list(compiled["contracts"]["Contract.sol"].keys())[0]
    abi = compiled["contracts"]["Contract.sol"][contract_name]["abi"]
    bytecode = compiled["contracts"]["Contract.sol"][contract_name]["evm"]["bytecode"][
        "object"
    ]
    return abi, bytecode


def deploy_contract(w3, abi, bytecode):
    acct = w3.eth.accounts[0]
    contract = w3.eth.contract(abi=abi, bytecode=bytecode)
    tx_hash = contract.constructor().transact({"from": acct})
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    return w3.eth.contract(address=tx_receipt.contractAddress, abi=abi)


def fuzz_contract(contract_path, method_name, rpc_url, iterations):
    print(f"Connecting to {rpc_url}...")
    w3 = Web3(Web3.HTTPProvider(rpc_url))
    assert w3.is_connected(), "Failed to connect to RPC"

    print("Compiling contract...")
    abi, bytecode = compile_contract(contract_path)

    print("Deploying contract...")
    contract = deploy_contract(w3, abi, bytecode)

    print(f"Fuzzing method '{method_name}' for {iterations} iterations...")
    method = getattr(contract.functions, method_name)

    input_types = []
    for item in contract.abi:
        if item.get("name") == method_name and item["type"] == "function":
            input_types = [inp["type"] for inp in item["inputs"]]
            break

    for i in range(iterations):
        try:
            args = generate_inputs(input_types)
            pre_state = get_state(contract)
            tx = method(*args).transact({"from": w3.eth.accounts[0]})
            w3.eth.wait_for_transaction_receipt(tx)
            post_state = get_state(contract)
            changes = compare_state(pre_state, post_state)
            print(
                f"[✓] Iteration {i+1}: Called {method_name}({args}) → State changes: {changes}"
            )
        except Exception as e:
            print(f"[!] Iteration {i+1} failed: {e}")
