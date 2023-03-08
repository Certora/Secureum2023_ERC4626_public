// SPDX-License-Identifier: UNLICENSED
pragma solidity >=0.8.0;

import {ERC1155, ERC1155TokenReceiver} from "../../../src/tokens/ERC1155.sol";

/// @notice An implementation for an ERC1155 receiver
contract ERC1155Receiver is ERC1155TokenReceiver {
    function sweepToken(
        address tokenAddr,
        address from,
        address to,
        uint256 id,
        uint256 amount,
        bytes calldata data
    ) external {
        ERC1155(tokenAddr).safeTransferFrom(from, to, id, amount, data);
    }

    function batchSweepToken(
        address tokenAddr,
        address from,
        address to,
        uint256[] calldata ids,
        uint256[] calldata amounts,
        bytes calldata data
    ) external {
        ERC1155(tokenAddr).safeBatchTransferFrom(from, to, ids, amounts, data);
    }
}
