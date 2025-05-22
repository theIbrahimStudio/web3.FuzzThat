import typer
from fuzzer.runner import fuzz_contract

app = typer.Typer()


@app.command()
def fuzzthat(
    contract: str = typer.Argument(..., help="Path to the Solidity contract file"),
    method: str = typer.Argument(..., help="Method to fuzz"),
    rpc_url: str = typer.Option(
        "http://localhost:8545", help="EVM RPC endpoint (e.g., Anvil or Hardhat)"
    ),
    times: int = typer.Option(10, help="Number of fuzz iterations"),
):
    """Fuzz a Solidity contract function using state-aware input generation."""
    fuzz_contract(
        contract_path=contract, method_name=method, rpc_url=rpc_url, iterations=times
    )


if __name__ == "__main__":
    app()
