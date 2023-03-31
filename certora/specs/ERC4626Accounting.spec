import "ERC4626.spec"

use rule conversionOfZero
use rule convertToAssetsWeakAdditivity
use rule convertToSharesWeakAdditivity
use rule conversionWeakMonotonicity
use rule conversionWeakIntegrity
use rule convertToCorrectness
use rule depositMonotonicity
use rule zeroDepositZeroShares
use invariant assetsMoreThanSupply
use invariant noAssetsIfNoSupply 
use invariant noSupplyIfNoAssets
use invariant totalSupplyIsSumOfBalances
use invariant sumOfBalancePairsBounded
use invariant singleBalanceBounded
use rule totalsMonotonicity
use rule underlyingCannotChange
use rule dustFavorsTheHouse
use invariant vaultSolvency
use rule redeemingAllValidity
use rule contributingProducesShares
use rule onlyContributionMethodsReduceAssets
use rule reclaimingProducesAssets

override definition noSupplyIfNoAssetsDef() returns bool = 
    ( userAssets(currentContract) == 0 => totalSupply() == 0 ) &&
    ( totalAssets() == 0 <=> ( totalSupply() == 0 ));