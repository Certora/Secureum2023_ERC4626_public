/*
 * This is a specification file to formally verify BorrowSystem.sol
 * smart contract using the Certora Prover. For more information,
 * visit: https://www.certora.com/
 *
 */


// reference from the spec to additional contracts used in the verification 

using DummyERC20A as ERC20a 
using DummyERC20B as ERC20b 


/*
    Declaration of methods that are used in the rules. envfree indicate that
    the method is not dependent on the environment (msg.value, msg.sender).
    Methods that are not declared here are assumed to be dependent on env.
*/
methods {
    name() returns string envfree;
    symbol() returns string envfree;
    decimals() returns uint8 envfree;
    asset() returns address envfree;

    totalSupply() returns uint256 envfree;
    
    nonces(address) returns uint256 envfree;

    approve(address,uint256) returns bool;
    deposit(uint256,address);
    mint(uint256,address);
    withdraw(uint256,address,address);
    redeem(uint256,address,address);

    totalAssets() returns uint256 envfree;
    userAssets(address) returns uint256 envfree;
    convertToShares(uint256) returns uint256 envfree;
    convertToAssets(uint256) returns uint256 envfree;
    previewDeposit(uint256) returns uint256 envfree;
    previewMint(uint256) returns uint256 envfree;
    previewWithdraw(uint256) returns uint256 envfree;
    previewRedeem(uint256) returns uint256 envfree;

    maxDeposit(address) returns uint256 envfree;
    maxMint(address) returns uint256 envfree;
    maxWithdraw(address) returns uint256 envfree;
    maxRedeem(address) returns uint256 envfree;

    permit(address,address,uint256,uint256,uint8,bytes32,bytes32);
    DOMAIN_SEPARATOR() returns bytes32;

    //// #ERC20 methods
    balanceOf(address) returns uint256 envfree => DISPATCHER(true);
    transfer(address,uint256) returns bool => DISPATCHER(true);
    transferFrom(address,address,uint256) returns bool => DISPATCHER(true);

    ERC20a.balanceOf(address) returns uint256 envfree;
    ERC20a.transferFrom(address,address,uint256) returns bool;
}



////////////////////////////////////////////////////////////////////////////////
////           #  asset To shares mathematical properties                  /////
////////////////////////////////////////////////////////////////////////////////

rule conversionOfZero {
    uint256 convertZeroShares = convertToAssets(0);
    uint256 convertZeroAssets = convertToShares(0);

    assert convertZeroShares == 0,
        "converting zero shares must return zero assets";
    assert convertZeroAssets == 0,
        "converting zero assets must return zero shares";
}

rule convertToAssetsWeakAdditivity() {
    uint256 sharesA; uint256 sharesB;
    require sharesA + sharesB < max_uint128
         && convertToAssets(sharesA) + convertToAssets(sharesB) < max_uint256
         && convertToAssets(sharesA + sharesB) < max_uint256;
    assert convertToAssets(sharesA) + convertToAssets(sharesB) <= convertToAssets(sharesA + sharesB),
        "converting sharesA and sharesB to assets then summing them must yield a smaller or equal result to summing them then converting";
}

rule convertToSharesWeakAdditivity() {
    uint256 assetsA; uint256 assetsB;
    require assetsA + assetsB < max_uint128
         && convertToAssets(assetsA) + convertToAssets(assetsB) < max_uint256
         && convertToAssets(assetsA + assetsB) < max_uint256;
    assert convertToAssets(assetsA) + convertToAssets(assetsB) <= convertToAssets(assetsA + assetsB),
        "converting assetsA and assetsB to shares then summing them must yield a smaller or equal result to summing them then converting";
}

rule conversionWeakMonotonicity {
    uint256 smallerShares; uint256 largerShares;
    uint256 smallerAssets; uint256 largerAssets;

    assert smallerShares < largerShares => convertToAssets(smallerShares) <= convertToAssets(largerShares),
        "converting more shares must yield equal or greater assets";
    assert smallerAssets < largerAssets => convertToShares(smallerAssets) <= convertToShares(largerAssets),
        "converting more assets must yield equal or greater shares";
}

rule conversionWeakIntegrity() {
    uint256 sharesOrAssets;
    assert convertToShares(convertToAssets(sharesOrAssets)) <= sharesOrAssets,
        "converting shares to assets then back to shares must return shares less than or equal to the original amount";
    assert convertToAssets(convertToShares(sharesOrAssets)) <= sharesOrAssets,
        "converting assets to shares then back to assets must return assets less than or equal to the original amount";
}

rule convertToCorrectness(uint256 amount, uint256 shares)
{
    assert amount >= convertToAssets(convertToShares(amount));
    assert shares >= convertToShares(convertToAssets(shares));
}


////////////////////////////////////////////////////////////////////////////////
////                   #    Unit Test                                      /////
////////////////////////////////////////////////////////////////////////////////

rule depositMonotonicity() {
    env e; storage start = lastStorage;

    uint256 smallerAssets; uint256 largerAssets;
    address receiver;
    require currentContract != e.msg.sender && currentContract != receiver; 

    safeAssumptions(e, e.msg.sender, receiver);

    deposit(e, smallerAssets, receiver);
    uint256 smallerShares = balanceOf(receiver) ;

    deposit(e, largerAssets, receiver) at start;
    uint256 largerShares = balanceOf(receiver) ;

    assert smallerAssets < largerAssets => smallerShares <= largerShares,
            "when supply tokens outnumber asset tokens, a larger deposit of assets must produce an equal or greater number of shares";
}


rule zeroDepositZeroShares(uint assets, address receiver)
{
    env e;
    
    uint shares = deposit(e,assets, receiver);

    assert shares == 0 <=> assets == 0;
}

////////////////////////////////////////////////////////////////////////////////
////                    #    Valid State                                   /////
////////////////////////////////////////////////////////////////////////////////

invariant assetsMoreThanSupply()
    totalAssets() >= totalSupply()
    {
        preserved with (env e) {
            require e.msg.sender != currentContract;
            address any;
            safeAssumptions(e, any , e.msg.sender);
        }
    }

invariant noAssetsIfNoSupply() 
   ( userAssets(currentContract) == 0 => totalSupply() == 0 ) &&
    ( totalAssets() == 0 => ( totalSupply() == 0 ))

    {
        preserved with (env e) {
        address any;
            safeAssumptions(e, any, e.msg.sender);
        }
    }

invariant noSupplyIfNoAssets()
    noSupplyIfNoAssetsDef()     // see defition in "helpers and miscellaneous" section
    {
        preserved with (env e) {
            safeAssumptions(e, _, e.msg.sender);
        }
    }



ghost mathint sumOfBalances {
    init_state axiom sumOfBalances == 0;
}

hook Sstore balanceOf[KEY address addy] uint256 newValue (uint256 oldValue) STORAGE {
    sumOfBalances = sumOfBalances + newValue - oldValue;
}

hook Sload uint256 val balanceOf[KEY address addy] STORAGE {
    require sumOfBalances >= val;
}

invariant totalSupplyIsSumOfBalances()
    totalSupply() == sumOfBalances


/* The following two invariants are just to show how tedious it is to prove the weaker version of totalSupplyIsSumOfBalances */
invariant sumOfBalancePairsBounded(address addy1, address addy2 )
    addy1 != addy2 => balanceOf(addy1) + balanceOf(addy2) <= totalSupply()
    {
        preserved {
            require asset() != currentContract;
            requireInvariant totalSupplyIsSumOfBalances();
        }
        preserved withdraw(uint256 assets, address receiver, address owner) with (env e2) {
            require asset() != currentContract;
            requireInvariant totalSupplyIsSumOfBalances();
            require owner == addy1 || owner == addy2 => balanceOf(addy1) + balanceOf(addy2) <= sumOfBalances;
            require owner != addy1 && owner != addy2 => balanceOf(addy1) + balanceOf(addy2) + balanceOf(owner) <= sumOfBalances;
        }
        preserved redeem(uint256 shares, address receiver, address owner) with (env e3) {
            require asset() != currentContract;
            requireInvariant totalSupplyIsSumOfBalances();
            require owner == addy1 || owner == addy2 => balanceOf(addy1) + balanceOf(addy2) <= sumOfBalances;
            require owner != addy1 && owner != addy2 => balanceOf(addy1) + balanceOf(addy2) + balanceOf(owner) <= sumOfBalances;
        }
        preserved transfer(address to, uint256 amount) with (env e4) {
            require asset() != currentContract;
            requireInvariant totalSupplyIsSumOfBalances();
            require e4.msg.sender == addy1 || e4.msg.sender == addy2 => balanceOf(addy1) + balanceOf(addy2) <= sumOfBalances;
            require e4.msg.sender != addy1 && e4.msg.sender != addy2 => balanceOf(addy1) + balanceOf(addy2) + balanceOf(e4.msg.sender) <= sumOfBalances;
        }
        preserved transferFrom(address from, address to, uint256 amount) with (env e5) {
            require asset() != currentContract;
            requireInvariant totalSupplyIsSumOfBalances();
            require from == addy1 || from == addy2 => balanceOf(addy1) + balanceOf(addy2) <= sumOfBalances;
            require from != addy1 && from != addy2 => balanceOf(addy1) + balanceOf(addy2) + balanceOf(from) <= sumOfBalances;
        }
    }

/* just to show how tedious it is to prove the weaker version of totalSupplyIsSumOfBalances */

invariant singleBalanceBounded(address addy )
    balanceOf(addy) <= totalSupply()
    {
        preserved {
            require asset() != currentContract;
            requireInvariant totalSupplyIsSumOfBalances();
        }
        preserved withdraw(uint256 assets, address receiver, address owner) with (env e2) {
            require asset() != currentContract;
            requireInvariant totalSupplyIsSumOfBalances();
            require addy == owner => balanceOf(addy)<= sumOfBalances;
            require addy != owner => balanceOf(addy) + balanceOf(owner) <= sumOfBalances;
        }
        preserved redeem(uint256 shares, address receiver, address owner) with (env e3) {
            require asset() != currentContract;
            requireInvariant totalSupplyIsSumOfBalances();
            require addy == owner => balanceOf(addy)<= sumOfBalances;
            require addy != owner => balanceOf(addy) + balanceOf(owner) <= sumOfBalances;
        }
        preserved transfer(address to, uint256 amount) with (env e4) {
            require asset() != currentContract;
            requireInvariant totalSupplyIsSumOfBalances();
            require addy == e4.msg.sender => balanceOf(addy) <= sumOfBalances;
            require addy != e4.msg.sender => balanceOf(addy) + balanceOf(e4.msg.sender) <= sumOfBalances;
        }
        preserved transferFrom(address from, address to, uint256 amount) with (env e5) {
            require asset() != currentContract;
            requireInvariant totalSupplyIsSumOfBalances();
            require addy == from => balanceOf(addy) <= sumOfBalances;
            require addy != from => balanceOf(addy) + balanceOf(from) <= sumOfBalances;
        }
    }


////////////////////////////////////////////////////////////////////////////////
////                    #     State Transition                             /////
////////////////////////////////////////////////////////////////////////////////


rule totalsMonotonicity() {
    method f; env e; calldataarg args;
    require e.msg.sender != currentContract; 
    uint256 totalSupplyBefore = totalSupply();
    uint256 totalAssetsBefore = totalAssets();
    address receiver;
    safeAssumptions(e, receiver, e.msg.sender);
    callReceiverFunctions(f, e, receiver);

    uint256 totalSupplyAfter = totalSupply();
    uint256 totalAssetsAfter = totalAssets();
    
    // possibly assert totalSupply and totalAssets must not change in opposite directions
    assert totalSupplyBefore < totalSupplyAfter  <=> totalAssetsBefore < totalAssetsAfter,
        "if totalSupply changes by a larger amount, the corresponding change in totalAssets must remain the same or grow";
    assert totalSupplyAfter == totalSupplyBefore => totalAssetsBefore == totalAssetsAfter,
        "equal size changes to totalSupply must yield equal size changes to totalAssets";
}

rule underlyingCannotChange() {
    address originalAsset = asset();

    method f; env e; calldataarg args;
    f(e, args);

    address newAsset = asset();

    assert originalAsset == newAsset,
        "the underlying asset of a contract must not change";
}

////////////////////////////////////////////////////////////////////////////////
////                    #   High Level                                    /////
////////////////////////////////////////////////////////////////////////////////

//// #  This rules timeout - we will show how to deal with timeouts 
/* rule totalAssetsOfUser(method f, address user ) {
    env e;
    calldataarg args;
    safeAssumptions(e, e.msg.sender, user);
    require user != currentContract;
    mathint before = userAssets(user) + maxWithdraw(user); 

    // need to ignore cases where user is msg.sender but someone else the receiver 
    address receiver; 
    require e.msg.sender != user;
    uint256 assets; uint256 shares;
    callFunctionsWithReceiverAndOwner(e, f, assets, shares, receiver, e.msg.sender);
    mathint after = userAssets(user) + maxWithdraw(user); 
    assert after >= before; 
}
*/

rule dustFavorsTheHouse(uint assetsIn )
{
    env e;
        
    require e.msg.sender != currentContract;
    safeAssumptions(e,e.msg.sender,e.msg.sender);
    uint256 totalSupplyBefore = totalSupply();

    uint balanceBefore = ERC20a.balanceOf(currentContract);

    uint shares = deposit(e,assetsIn, e.msg.sender);
    uint assetsOut = redeem(e,shares,e.msg.sender,e.msg.sender);

    uint balanceAfter = ERC20a.balanceOf(currentContract);

    assert balanceAfter >= balanceBefore;
}

////////////////////////////////////////////////////////////////////////////////
////                       #   Risk Analysis                           /////////
////////////////////////////////////////////////////////////////////////////////


invariant vaultSolvency()
    totalAssets() >= totalSupply()  && userAssets(currentContract) >= totalAssets()  {
      preserved with(env e){
            requireInvariant totalSupplyIsSumOfBalances();
            require e.msg.sender != currentContract;
            require currentContract != asset(); 
        }
    }



rule redeemingAllValidity() { 
    address owner; 
    uint256 shares; require shares == balanceOf(owner);
    
    env e; safeAssumptions(e, _, owner);
    redeem(e, shares, _, owner);
    uint256 ownerBalanceAfter = balanceOf(owner);
    assert ownerBalanceAfter == 0;
}


////////////////////////////////////////////////////////////////////////////////
////               # stakeholder properties  (Risk Analysis )         //////////
////////////////////////////////////////////////////////////////////////////////

rule contributingProducesShares(method f)
filtered {
    f -> f.selector == deposit(uint256,address).selector
      || f.selector == mint(uint256,address).selector
}
{
    env e; uint256 assets; uint256 shares;
    address contributor; require contributor == e.msg.sender;
    address receiver;
    require currentContract != contributor
         && currentContract != receiver;

    require previewDeposit(assets) + balanceOf(receiver) <= max_uint256; // safe assumption because call to _mint will revert if totalSupply += amount overflows
    require shares + balanceOf(receiver) <= max_uint256; // same as above

    safeAssumptions(e, contributor, receiver);

    uint256 contributorAssetsBefore = userAssets(contributor);
    uint256 receiverSharesBefore = balanceOf(receiver);

    callContributionMethods(e, f, assets, shares, receiver);

    uint256 contributorAssetsAfter = userAssets(contributor);
    uint256 receiverSharesAfter = balanceOf(receiver);

    assert contributorAssetsBefore > contributorAssetsAfter <=> receiverSharesBefore < receiverSharesAfter,
        "a contributor's assets must decrease if and only if the receiver's shares increase";
}

rule onlyContributionMethodsReduceAssets(method f) {
    address user; require user != currentContract;
    uint256 userAssetsBefore = userAssets(user);

    env e; calldataarg args;
    safeAssumptions(e, user, _);

    f(e, args);

    uint256 userAssetsAfter = userAssets(user);

    assert userAssetsBefore > userAssetsAfter =>
        (f.selector == deposit(uint256,address).selector ||
         f.selector == mint(uint256,address).selector),
        "a user's assets must not go down except on calls to contribution methods";
}

rule reclaimingProducesAssets(method f)
filtered {
    f -> f.selector == withdraw(uint256,address,address).selector
      || f.selector == redeem(uint256,address,address).selector
}
{
    env e; uint256 assets; uint256 shares;
    address receiver; address owner;
    require currentContract != e.msg.sender
         && currentContract != receiver
         && currentContract != owner;

    safeAssumptions(e, receiver, owner);

    uint256 ownerSharesBefore = balanceOf(owner);
    uint256 receiverAssetsBefore = userAssets(receiver);

    callReclaimingMethods(e, f, assets, shares, receiver, owner);

    uint256 ownerSharesAfter = balanceOf(owner);
    uint256 receiverAssetsAfter = userAssets(receiver);

    assert ownerSharesBefore > ownerSharesAfter <=> receiverAssetsBefore < receiverAssetsAfter,
        "an owner's shares must decrease if and only if the receiver's assets increase";
}



////////////////////////////////////////////////////////////////////////////////
////                        # helpers and miscellaneous                //////////
////////////////////////////////////////////////////////////////////////////////

definition noSupplyIfNoAssetsDef() returns bool = 
    ( userAssets(currentContract) == 0 => totalSupply() == 0 ) &&
    ( totalAssets() == 0 => ( totalSupply() == 0 ));

// definition noSupplyIfNoAssetsStrongerDef() returns bool =                // fails for ERC4626BalanceOfHarness as explained in the readme
//     ( userAssets(currentContract) == 0 => totalSupply() == 0 ) &&
//     ( totalAssets() == 0 <=> ( totalSupply() == 0 ));


function safeAssumptions(env e, address receiver, address owner) {
    require currentContract != asset(); // Although this is not disallowed, we assume the contract's underlying asset is not the contract itself
    requireInvariant totalSupplyIsSumOfBalances();
    requireInvariant vaultSolvency();
    requireInvariant noAssetsIfNoSupply();
    requireInvariant noSupplyIfNoAssets();
    requireInvariant assetsMoreThanSupply(); 

    //// # Note : we don't want to use singleBalanceBounded and singleBalanceBounded invariants 
    /* requireInvariant sumOfBalancePairsBounded(receiver, owner );
    requireInvariant singleBalanceBounded(receiver);
    requireInvariant singleBalanceBounded(owner);
    */
    ///// # but, it safe to assume that a single balance is less than sum of balances
    require ( (receiver != owner => balanceOf(owner) + balanceOf(receiver) <= totalSupply())  && 
                balanceOf(receiver) <= totalSupply() &&
                balanceOf(owner) <= totalSupply());
}


// A helper function to set the receiver 
function callReceiverFunctions(method f, env e, address receiver) {
    uint256 amount;
    if (f.selector == deposit(uint256,address).selector) {
        deposit(e, amount, receiver);
    } else if (f.selector == mint(uint256,address).selector) {
        mint(e, amount, receiver);
    } else if (f.selector == withdraw(uint256,address,address).selector) {
        address owner;
        withdraw(e, amount, receiver, owner);
    } else if (f.selector == redeem(uint256,address,address).selector) {
        address owner;
        redeem(e, amount, receiver, owner);
    } else {
        calldataarg args;
        f(e, args);
    }
}


function callContributionMethods(env e, method f, uint256 assets, uint256 shares, address receiver) {
    if (f.selector == deposit(uint256,address).selector) {
        deposit(e, assets, receiver);
    }
    if (f.selector == mint(uint256,address).selector) {
        mint(e, shares, receiver);
    }
}

function callReclaimingMethods(env e, method f, uint256 assets, uint256 shares, address receiver, address owner) {
    if (f.selector == withdraw(uint256,address,address).selector) {
        withdraw(e, assets, receiver, owner);
    }
    if (f.selector == redeem(uint256,address,address).selector) {
        redeem(e, shares, receiver, owner);
    }
}

function callFunctionsWithReceiverAndOwner(env e, method f, uint256 assets, uint256 shares, address receiver, address owner) {
    if (f.selector == withdraw(uint256,address,address).selector) {
        withdraw(e, assets, receiver, owner);
    }
    if (f.selector == redeem(uint256,address,address).selector) {
        redeem(e, shares, receiver, owner);
    } 
    if (f.selector == deposit(uint256,address).selector) {
        deposit(e, assets, receiver);
    }
    if (f.selector == mint(uint256,address).selector) {
        mint(e, shares, receiver);
    }
     if (f.selector == transferFrom(address,address,uint256).selector) {
        transferFrom(e, owner, receiver, shares);
    }
    else {
        calldataarg args;
        f(e, args);
    }
}
