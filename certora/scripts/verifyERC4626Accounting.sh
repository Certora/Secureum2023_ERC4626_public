if [[ "$1" ]]
then
    RULE="--rules $1"
fi

if [[ "$2" ]]
then
    MSG="- $2"
fi

certoraRun \
    certora/harnesses/mixins/ERC4626AccountingHarness.sol \
    certora/helpers/DummyERC20A.sol certora/helpers/DummyERC20B.sol \
    --verify ERC4626AccountingHarness:certora/specs/ERC4626Accounting.spec \
    --solc solc8.0 \
    --optimistic_loop \
    --cloud \
    --send_only \
    --rule_sanity \
    $RULE \
    --msg "ERC4626 verification: $RULE $MSG"