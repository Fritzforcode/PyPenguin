[BACK](main.md)

# Format of Monitors

Must be an object with the following properties:
* `"opcode"`: The opcode of the block reporter, whose value is shown. [Possible Opcodes](other.md#menu-opcodes-not-updated)

* `"options"`: The dropdowns of the block, whose value is shown. Must be an object of block specific keys and values.

* `"position"`: The position of the monitor on the stage.

* `"spriteName"`: The name of the sprite, the block is 

* `"visible"`: Wether the monitor is shown on the stage. Must be a boolean.

## Variable Monitors
Variable Monitors must have these additional properties:
* `"sliderMin"`: The minimum of the slider. (when the monitor is in the slider mode.) Must be an integer when `"onlyIntegers"` is `true` otherwise a number.

* `"sliderMax"`: The maximum of the slider. (when the monitor is in the slider mode.) Must be an integer when `"onlyIntegers"` is `true` otherwise a number.

* `"onlyIntegers"`: If `true` only integers are allowed in the slider.

## List Monitors
* `"size"`: The size of a list monitor, because their size can be changed in the editor. Must be an array coordinate. e.g. `[100, 200]`

