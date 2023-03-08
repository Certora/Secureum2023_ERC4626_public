// SPDX-License-Identifier: UNLICENSED
pragma solidity >=0.8.0;

import {ERC20} from "../../../src/tokens/ERC20.sol";
import {ERC4626} from "../../../src/mixins/ERC4626.sol";
// import {ERC4626} from "../bugs/ERC4626_burnInRedeemFromSender.sol";
// import {ERC4626} from "../bugs/ERC4626_convToAssetsDivUp.sol";
// import {ERC4626} from "../bugs/ERC4626_noIfInWithdraw.sol";
// import {ERC4626} from "../bugs/ERC4626_notUsingAssetInDeposit.sol";
// import {ERC4626} from "../bugs/ERC4626_previewMintShortReturn.sol";
import {Owned} from "../../../src/auth/Owned.sol";

/// @notice A harness implementation for the ERC4626 vault standard
/// @dev This contract implements the `totalAssets()` function by accounting 
///      every change to the contract's balance. 
///      The owner can account the accrued rewards using the `accrueRewards()` function.
contract ERC4626AccountingHarness is ERC4626, Owned {
    constructor(address _asset) 
        ERC4626(ERC20(_asset), "ERC4626 Harness", "ERC4626H") 
        Owned(msg.sender) 
    {}

    uint public currentBalance;

    function beforeWithdraw(uint256 assets, uint256) internal override {
        currentBalance -= assets;
    }

    function afterDeposit(uint256 assets, uint256) internal override {
        currentBalance += assets;
    }

    /// @notice This function should be called only by the owner, otherwise the 
    ///         first depositor will be able to steal all the other users' funds. 
    ///         This can be done by front-running the deposit transaction and 
    ///         call `accrueRewards()` with enough tokens to zero the shares calculation.
    function accrueRewards(uint rewards) external onlyOwner {
        currentBalance += rewards;
        asset.transferFrom(msg.sender, address(this), rewards);
    }

    function totalAssets() public view override returns (uint256) {
        return currentBalance;
    }
}
