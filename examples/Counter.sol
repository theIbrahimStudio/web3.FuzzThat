// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract Counter {
    uint public count = 0;

    function increment() public {
        count += 1;
    }

    function decrement() public {
        require(count > 0, "Underflow");
        count -= 1;
    }
}
