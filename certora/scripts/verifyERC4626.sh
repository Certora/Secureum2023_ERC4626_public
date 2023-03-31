if [[ "$1" ]]
then
    RULE="--rule $1"
fi

if [[ "$2" ]]
then
    MSG="- $2"
fi

certoraRun \
    certora/harnesses/mixins/ERC4626BalanceOfHarness.sol \
    certora/helpers/DummyERC20A.sol certora/helpers/DummyERC20B.sol \
    --verify ERC4626BalanceOfHarness:certora/specs/ERC4626.spec \
    --solc solc8.0 \
    --optimistic_loop \
    --cloud \
    --send_only \
    --rule_sanity \
    $RULE \
    --msg "ERC4626 verification: $RULE $MSG"

    
# certora/harnesses/mixins/ERC4626BalanceOfHarness.sol \
# certora/harnesses/mixins/ERC4626AccountingHarness.sol \
# --multi_example basic \
