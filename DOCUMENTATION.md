# PyPenguin Documentation
This is the documentation for **PyPenguin**. 

The file structure of **PyPenguin Project** should look like this:

```
My PyPenguin Project (can be anything)
├─ project.json
├─ #Stage
│  ├─ costumes
│  │  └─ backdrop1.svg
│  └─ sounds
│     └─ Hello%20World.mp3
└─ Sprite1
   ├─ costumes
   │  └─ costume1.png
   └─ sounds
      └─ Squawk.wav
```
#### Notes:
* `project.json` is documented [below](#format-of-the-project-projectjson).
* `sprite`, `costume` and `sound` names have to [percent encoded](https://en.wikipedia.org/wiki/Percent-encoding).
* `#Stage` is used for the stage to avoid overlapping with sprite names.
* PenguinMod seems to only support `48kHz` sounds. For a safe usage convert your sounds. 


## Format of the Project (`project.json`)
The Project data must be an object with the following properties:
* `"sprites"`: [Stage and Sprites Format](#format-of-sprites).

* `"globalVariables"`: [Variable Format](#format-of-variables-and-lists).

* `"globalLists"`:  [List Format](#format-of-variables-and-lists).

* `"tempo"`: The tempo from the **Music** extension. Must be an integer between 20 and 500.

* `"videoTransparency"`: The transpercancy of the stage when using the "Video Sensing" Extension. Must be a number. 

* `"videoState"`: The state of the "Video Sensing" Extension. Must be either `"on"`, `"on flipped"` or `"off"`.

* `"textToSpeechLanguage"`: The language of the **Text to Speech** Extension. Must be either `null` or one of [Possible Values](#supported-text-to-speech-languages).

* `"extensionData"`: An object containing additional information about extensions. (Let me know if you wish more research.)

* `"extensions"`: An array of extension acronyms, which were added to the project.

* `"meta"`: [Meta Format](#format-of-the-metadata).



## Format of Sprites
Must be an array of sprites. The first sprite is always the stage. Then the other sprites follow in the same order as in the editor. A sprite must be an object with the following properties:
* `"isStage"`: Wether the sprite is the stage. Must be `true` for the stage(the first sprite) and `false` for all other sprites.

* `"name"`: Must be "Stage" for the stage(the first sprite). For all other sprites this can be any string.

* `"scripts"`: The scripts of the sprite. [Script Format](#format-of-scripts).

* `"comments"`: The comments that are not attached to a block. A comment must be either `null` or an object following the [Comment Format](#format-of-comments).

* `"currentCostume"`: The costume number of the sprite. Must be an integer and at least `0`.

* `"costumes"`: [Costume Format](#format-of-costumes-and-sounds).

* `"sounds"`: [Sound Format](#format-of-costumes-and-sounds).

* `"volume"`: The volume(applies to sounds). Must be a number between `0` and `100`.

* `"localVariables"`: The `"For this sprite only"` variables of this sprite. [Variable Format](#format-of-variables-and-lists).

* `"localLists"`: The `"For this sprite only"` lists of this sprite. [List Format](#format-of-variables-and-lists).

* `"layerOrder"(*)`: The layer the sprite is on. Must be an integer and at least `1`.

* `"visible"(*)`: Wether the sprite is shown or hidden. Must be a boolean.

* `"position"(*)`: The position of the sprite on the stage. Must be a two-long array of numbers.

* `"size"(*)`: The size of the sprite. Must be a positive number.

* `"direction"(*)`. The direction of the sprite. Must be a number between `-180` and `180`.

* `"draggable"(*)`: Wether one can drag the sprite with the mouse in fullscreen mode. Must be a boolean.

* `"rotationStyle"(*)`: How the sprite behaves when it rotates. Must be either `"all around"`, `"left-right"` or `"don't rotate"`.

\* Attributes which are only necessary for sprites. The stage shouldn't have these attributes.



## Format of Scripts
Must be an array of scripts. A script must be an object with the following properties:
* `"position"`: The position of a block reporter or the first block in a script. Must be a two-long array of integers.

* `"blocks"`: The blocks of the script in an array (even for a (single) block reporter). They are in order from top of the script to bottom of the script. [Block Format](#format-of-a-block).



## Format of a Block
Must be an object with the following properties:
* `"opcode"`: The operation code of the block. [Block Opcodes](#defined-block-opcodes).

* `"inputs"`: The inputs of the block. [Input Format](#format-of-inputs).

* `"options"`: The options of the block. [Option Format](#format-of-options).

* `"comment"`: The comment attached to the block. Must be either `null` or an object following the [Comment Format](#format-of-comments).
#### Example



## Format of Inputs
Must be an object of block-specific keys and values. Each value must follow one of these modes:
* **Block and Text Mode**: Allows text and optionally a block in the input field. Used in the `"broadcast"`, `"number"` and `"text"` input types. 
* **Block Only Mode**: Allows only text in the input field.

You can see the input types of blocks [HERE](assets/opcode_database.jsonc).

An input value must be an object with the following properties:
* `"mode"`: must be `"block-and-text"` for **Block and Text Mode** and `"block-only"` for **Block Only Mode**.

* `"block"`: Only exists in **Block and Text Mode**. The block that is in the input field. Must be either `null` for no block or a block following the [Block Format](#format-of-a-block).

* `"text"`: The text of the input field. Must be a string.
#### Example



## Format of Options 
Must be an object of block-specific keys and values. Currently there is only one option value type, a string.
#### Example



## Defined Block Opcodes
Here is a list of opcodes currently defined:
* `"when [KEY_OPTION] key pressed"`
* `"when i receive [BROADCAST_OPTION]"`
* `"broadcast [BROADCAST_INPUT]"`
* `"(NUM1) + (NUM2)"`
* `"(NUM1) * (NUM2)"`
* `"join (STRING1) (STRING2)"`
* `"set [VARIABLE] to (VALUE)"`
* `"change [VARIABLE] by (VALUE)"`
* `"add (ITEM) to [LIST]"`



## Format of Comments
Must be either `null` or an object with the following properties:
* `"position"`: The position of the comment in the sprite. Must be a two-long array of numbers.

* `"size"`: The size of the comment when it isn't minimized. Must be a two long array of numbers.

* `"isMinimzed"`: Wether the comment is folded (when `true`) in or expanded (when `false`). Must be a boolean. 

* `"text"`: The text of the comment. Must be a string.
#### Example



## Format of Costumes and Sounds 
Must be an object with the following properties:
* `"name"`: The name of the costume or sound. Must be a string.

* `"dataFormat"`: The file extension of the asset. (Let me know if you wish a detailed list of supported file types.)

* `"fileStem"`: The file name (without extension) of the asset. (Does not allow folders.) Must be a string.

For a costume the following properties are required additionally:
* `"bitmapResolution"`: The resolution of the bitmap. Must be an integer and at least `1`.

* `"rotationCenter"`: The point the costume can be rotated around. 

For a sound the following properties are required additionally:

* `"rate"`: The sample rate of the sound. Must be an integer and at least `1`. Seems to always be `48000`.

* `"sampleCount"`: The number of samples in the sound.
#### Example (Costume)
#### Example (Sound)



## Format of Variables and Lists
Must be an object with the following properties:
* `"name"`: The name of the variable/list. Must be a non-empty string.

* `"currentValue"`: The value the variable/list currently has. For a variable this must be a string or a number. For a list this must be an array. Each item must be either a string or a number.

* `"monitor"`: Must be either null or an object following the [Monitor Format](#format-of-variable-and-list-monitors)

* `"isCloudVariable"(*)`: Wether the variable is a cloud variable. Must be a boolean.

\* only exists for variables in the `"globalVariables"` array.



## Format of Variable and List Monitors
Must be either null or an object with the following properties:
* `"visible"`: Wether the monitor is shown on the stage. Must be a boolean.

* `"size"`: The size of the monitor. Must be a two-long array of integers.

* `"position"`: The position of the monitor on the stage.

* `"sliderMin"(*)`: The minimum of the slider. (when the monitor is in the slider mode.) Must be an integer when `"onlyIntegers"` is `true` otherwise a number.

* `"sliderMax"(*)`: The maximum of the slider. (when the monitor is in the slider mode.) Must be an integer when `"onlyIntegers"` is `true` otherwise a number.

* `"onlyIntegers"(*)`: If `true` only integers are allowed in the slider.

\* only exists for variables.



## Supported Text to Speech Languages
* `"ar"` (Arabic)
* `"zh-cn"` (Chinese (Mandarin))
* `"da"` (Danish)
* `"nl"` (Dutch)
* `"en"` (English)
* `"fr"` (French)
* `"de"` (German)
* `"hi"` (Hindi)
* `"is"` (Icelandic)
* `"it"` (Italian)
* `"ja"` (Japanese)
* `"ko"` (Korean)
* `"nb"` (Norgwegian)
* `"pl"` (Polish)
* `"pt-br"` (Porturguese (Brazilian))
* `"pt"` (Protuguese)
* `"ro"` (Romanian)
* `"ru"` (Russian)
* `"es"` (Spanish)
* `"es-419"` (Spanish (Latin American))
* `"sv"` (Swedish)
* `"tr"` (Turkish)
* `"cy"` (Welsh)



## Format of the Metadata
If you don't need a detailed description and just copy the example(works for **PengiunMod**). You will probably not ever need to change the metadata.

Must be an object with the following properties:

* `"semver"`: Must be `"3.0.0"`.

* `"vm"`: The version of the PenguinMod Virtual Machine which was used to edit the project. The most recent version is `"0.2.0"`.

* `"agent"`: The User Agent. Must be `""` for PenguinMod.

* `"platform"`: Some information about the platform used to edit your project.
#### Example
```
{
    "semver": "3.0.0",
    "vm": "0.2.0",
    "agent": "",
    "platform": {
        "name": "PenguinMod",
        "url": "https://penguinmod.com/",
        "version": "stable"
    }
}
```
