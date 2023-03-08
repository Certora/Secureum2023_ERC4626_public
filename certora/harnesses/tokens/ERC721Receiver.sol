// SPDX-License-Identifier: UNLICENSED
pragma solidity >=0.8.0;

import {ERC721, ERC721TokenReceiver} from "../../../src/tokens/ERC721.sol";

/// @notice An implementation for an ERC721 receiver
contract ERC721Receiver is ERC721TokenReceiver {
    function sweepToken(address tokenAddr, uint tokenId) external {
        ERC721(tokenAddr).safeTransferFrom(address(this), msg.sender, tokenId);
    }
}
