[BACK](main.md)

# What a monitor looks like

`"monitors"` must be an array of monitors. A monitor must be an object with the following properties:
| **property**   | **type**          | **description**                                                                                       
|----------------|-------------------|-------------------------------------------------------------------------------------------------------
| `"opcode"`     | string            | The opcode of the block reporter, whose value is shown. [Possible Opcodes](other.md#menu-opcodes)     
| `"options"`    | object of strings | The dropdowns of the block, whose value is shown. Must be an object of block specific keys and values.
| `"position"`   | array coordinate  | The position of the monitor on the stage.                                                             
| `"spriteName"` | null \| string    | The name of the sprite, the block refers to.                                                          
| `"visible"`    | boolean           | Wether the monitor is shown on the stage.                                                             


### Examples
* Example 1
    ```
    {
        "opcode": "[EFFECT] sprite effect",
        "options": {"EFFECT": "color"},
        "position": [20, 20],
        "spriteName": "Sprite1",
        "visible": True,
    }
    ```
    <pre class="blocks">
    ([color v] effect::looks)
    </pre>
* Example 2
    ```
    {
        "opcode": ""value of [VARIABLE]"",
        "options": {"VARIABLE": "my variable"},
        "position": [20, 20],
        "spriteName": "Sprite1",
        "visible": True,
    }
    ```
    <pre class="blocks">
    (my variable)
    </pre>

## Variable Monitors
Variable Monitors must have these additional properties:
| **property**     | **type**           | **description**                                                                                                                            
|------------------|--------------------|--------------------------------------------------------------------------------------------------------------------------------------------
| `"sliderMin"`    | integer (or float) | The minimum of the slider. (when the monitor is in the slider mode.) Must be an integer when `"onlyIntegers"` is `true` otherwise a number.
| `"sliderMax"`    | integer (or float) | The maximum of the slider. (when the monitor is in the slider mode.) Must be an integer when `"onlyIntegers"` is `true` otherwise a number.
| `"onlyIntegers"` | boolean            | If `true` only integers are allowed for `"sliderMin"` and `"sliderMax"`.                                                                   


## List Monitors
List Monitors must have these additional properties:
| **property** | **type**         | **description**                                                                                                           
|--------------|------------------|---------------------------------------------------------------------------------------------------------------------------
| `"size"`     | array coordinate | he size of a list monitor, because their size can be changed in the editor. Must be an array coordinate. e.g. `[100, 200]`


<script src="./scratchblocks.js"></script>
<script>
scratchblocks.renderMatching('pre.blocks', {
    style:     'scratch3',
    languages: ["en"],
    scale: 1,
});
</script>

