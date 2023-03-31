# ERC4626 - bug explanation

A specification file of ERC4626.

This spec can be checked against implementations of ERC4626. This repo contains two examples.

Version certora/harnesses/mixins/ERC4626BalanceOfHarness.sol uses external balance to reference the balance of the system. This version is buggy, as seen in this run:
https://vaas-stg.certora.com/output/23658/53dd81e08d874f0480009d029d6e1a89/?anonymousKey=e5b5e427144def37ed8aaa62f1c97a8816d280da

The invariant `noSupplyIfNoAssetsSTRONGER` does not hold 
```
totalAssets() == 0 <=> totalSupply() == 0
```
A weaker version of this invariant holds `noAssetsIfNoSupply` 
```
totalAssets() == 0 => ( totalSupply() == 0 )
```

since it does not hold an important property that one can not gain does not hold (`dustFavorsTheHouse`). It shows a case whereby an external transfer, one can gain assets from the system. 

On the version certora/harnesses/mixins/ERC4626AccountingHarness.sol the stronger noSupplyIfNoAssets holds and so does 
`dustFavorsTheHouse `. This is because the system manages the balances internally and does not refernces the external balance at the underlying token. 