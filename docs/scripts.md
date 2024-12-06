[GO BACK](sprites.md)

# Format of Scripts
Must be an object with the following properties:
* ˋ"position"ˋ: The position of the first block of the script in the coding space.
* ˋ"blocks"ˋ: The blocks of the script in order from top to bottom. [Block Format](#format-of-blocks)

## Format of Blocks
A Block must be an object with the following properties. ˋ"inputs"ˋ will be auto completed for blocks, that don't have inputs. ˋ"options"ˋ will be auto completed for blocks, that don't have dropdowns.
* ˋ"opcode"ˋ: The name of the block. [Opcodes](opcodes.md) e.g. "set [VARIABLE] to (VALUE)"
* ˋ"inputs"ˋ: The inputs of the block. 
* ˋ"options"ˋ: The dropdowns of the block.
* ˋ"comment"ˋ: The comment of the block. [Comment Format](comments.md)

