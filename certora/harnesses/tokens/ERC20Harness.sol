// SPDX-License-Identifier: UNLICENSED
pragma solidity >=0.8.0;

import {ERC20} from "../../../src/tokens/ERC20.sol";

/// A harness implementation for the ERC20 standard
/// This contract provides external mint and burn for everyone
contract ERC20Harness is ERC20 {
    constructor() ERC20("ERC20 Harness", "ERC20H", 18) {}

    function mint(address to, uint amount) external {
        _mint(to, amount);
    }

    function burn(address from, uint amount) external {
        _burn(from, amount);
    }
}
