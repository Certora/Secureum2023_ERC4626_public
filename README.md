# Secureum2023_ERC4626_public

There are 2 ERC4626 implementations (original contract (`src/mixins/`) is abstract). They are in `certora/harnesses/mixins/`. They also include imports to buggy versions. Comment out / uncomment what you need. 
- Can you create your implementations or use some that you know? - Yes, why not?! These two are the most basic implementations. 

There are five buggy versions: `certora/harnesses/bugs/`. We marked bugs with a comment. Search for the word "BUG" to find it faster.
- Can you add your bugs? - Yes.

Example spec is in `certora/specs/`.

The script for the example spec is in `certora/scripts/`. 
- Remember to change the implementation if you want to check another one. 
- If you use `solc-select` instead of `--solc solc8.0`, ensure you've changed it before running the script.