// SPDX-License-Identifier: UNLICENSED
pragma solidity >=0.8.0;

import {ERC721} from "../../../src/tokens/ERC721.sol";

/// A harness implementation for the ERC721 standard
/// This contract provides external mint and burn for everyone
contract ERC721Harness is ERC721 {
    constructor() ERC721("ERC721 Harness", "ERC721H") {}

    function mint(address to, uint tokenId) external {
        _mint(to, tokenId);
    }
    function burn(uint tokenId) external {
        _burn(tokenId);
    }

    function safeMint(address to, uint tokenId) external {
        _safeMint(to, tokenId);
    }

    function safeMint(address from, uint tokenId, bytes memory data) external {
        _safeMint(from, tokenId, data);
    }

    function tokenURI(uint256) public view override returns (string memory) {
        return "";
    }
}
