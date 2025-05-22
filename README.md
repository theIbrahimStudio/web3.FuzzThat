# Ah, Fuzz that!

**State-Aware Smart Contract Fuzzing for EVM-based Projects.**

A lightweight, open source CLI tool that performs **property-based fuzzing** of Solidity smart contracts using contract **state transitions** to guide input generation.

---

## Why?

Traditional fuzzers throw random inputs at your contracts. This tool:

- **Observes contract state** via storage/method patterns
- **Mutates inputs based on state context**
- **Finds edge cases** other fuzzers may miss

---

## Features

- Fuzzes any public function with type-aware inputs
- Tracks state variable changes per iteration
- Works with Solidity contracts using solc
- CLI-based and extensible

---

## Installation

```bash
git clone https://github.com/theIbrahimStudio/web3.FuzzThat.git FuzzThat
cd FuzzThat
pip install -e .
```

---

## Usage

```bash
fuzzthat examples/Counter.sol increment --iterations 10
```

---

## Project Structure

```
FuzzThat/
├── fuzzer/          # Core fuzzing engine
├── examples/        # Example Solidity contracts
├── tests/           # Unit tests
├── cli.py           # CLI entry point
├── pyproject.toml   # Package metadata
└── README.md
```

---

## Roadmap

- [x] CLI with input flags
- [x] Contract compiler + runner
- [x] Input generation (basic types)
- [x] State delta tracker
- [x] Unit test suite
- [x] Support for arrays/tuples
- [ ] JSON config support
- [ ] ERC20/ERC721 fuzz presets
- [ ] CI/CD + publishing to PyPI

---

## 🤝 Contributing

PRs welcome! Check out the [CONTRIBUTING.md](https://github.com/theIbrahimStudio/.github/blob/main/CONTRIBUTING.md) for guidelines.
