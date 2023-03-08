// SPDX-License-Identifier: UNLICENSED
pragma solidity >=0.8.0;

import {ERC20} from "../../../src/tokens/ERC20.sol";
import {ERC4626} from "../../../src/mixins/ERC4626.sol";
// import {ERC4626} from "../bugs/ERC4626_burnInRedeemFromSender.sol";
// import {ERC4626} from "../bugs/ERC4626_convToAssetsDivUp.sol";
// import {ERC4626} from "../bugs/ERC4626_noIfInWithdraw.sol";
// import {ERC4626} from "../bugs/ERC4626_notUsingAssetInDeposit.sol";
// import {ERC4626} from "../bugs/ERC4626_previewMintShortReturn.sol";

/// @notice A harness implementation for the ERC4626 vault standard
/// @dev This contract implements the `totalAssets()` function by simply 
///      returning the contract's balance. 
/// @notice This contract is open to an attack where the first depositor 
///         can steal all the other users' funds.
///         This can be done by front-running the deposit transaction and 
///         transferring enough tokens to zero the shares calculation.
contract ERC4626BalanceOfHarness is ERC4626 {
    constructor(address _asset) ERC4626(ERC20(_asset), "ERC4626 Harness", "ERC4626H") {}

    function totalAssets() public view override returns (uint256) {
        return asset.balanceOf(address(this));
    }

    function userAssets(address user) public view returns (uint256) { // harnessed
        return asset.balanceOf(user);
    }
}
