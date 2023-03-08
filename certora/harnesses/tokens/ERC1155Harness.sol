// SPDX-License-Identifier: UNLICENSED
pragma solidity >=0.8.0;

import {ERC1155} from "../../../src/tokens/ERC1155.sol";

/// A harness implementation for the ERC1155 standard
/// This contract provides external mint and burn for everyone
contract ERC1155Harness is ERC1155 {

    function mint(
        address to,
        uint256 id,
        uint256 amount,
        bytes memory data
    ) external {
        _mint(to, id, amount, data);
    }

    function batchMint(
        address to,
        uint256[] memory ids,
        uint256[] memory amounts,
        bytes memory data
    ) external {
        _batchMint(to, ids, amounts, data);
    }

    function batchBurn(
        address from,
        uint256[] memory ids,
        uint256[] memory amounts
    ) external {
        _batchBurn(from, ids, amounts);
    }

    function burn(
        address from,
        uint256 id,
        uint256 amount
    ) external {
        _burn(from, id, amount);
    }

    function uri(uint256) public view override returns (string memory) {
        return "";
    }
}
