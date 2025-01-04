# What a sprite looks like
The ˋ"sprites"ˋ attribute of the project data must be an array of sprites. The first sprite is always the stage. Then the other sprites follow in the same order as in the editor. A sprite must be an object with the following properties:

* `"isStage"`: Wether the sprite is the stage. Must be `true` for the stage(the first sprite) and `false` for all other sprites.

* `"name"`: Must be `"Stage"` for the stage(the first sprite). For all other sprites this can be any string.

* `"scripts"`: An array of the scripts of this sprite. [Docs]()

* `"comments"`: An array of comments, that are not attached to a block. [Docs]()

* `"currentCostume"`: The costume number of the sprite. Must be an integer and at least `0`.

* `"costumes"`: An array of the costumes/brackdrops of the sprite. [Docs]()

* `"sounds"`: An array of the sounds of the sprite. [Docs]()

* `"volume"`: The global volume(applies to sounds). Must be a number between `0` and `100`.

* `"localVariables"`: The `"For this sprite only"` variables of this sprite. [Docs]().

* `"localLists"`: The `"For this sprite only"` lists of this sprite. [Docs]().

Sprites, who are not the stage, must have these properties too:
* `"layerOrder"`: The layer the sprite is on. Must be an integer and at least `1`.

* `"visible"`: Wether the sprite is shown or hidden. Must be a boolean.

* `"position"`: The position of the sprite on the stage. Must be a two-long array of numbers.

* `"size"`: The size of the sprite. Must be a positive number.

* `"direction"`. The direction of the sprite. Must be a number between `-180` and `180`.

* `"draggable"`: Wether one can drag the sprite with the mouse in fullscreen mode. Must be a boolean.

* `"rotationStyle"`: How the sprite behaves when it rotates. Must be either `"all around"`, `"left-right"` or `"don't rotate"`.
