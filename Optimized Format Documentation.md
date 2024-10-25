Properties of objects are always required except when labeled differently


## Format of the Project
The Project data must be an object with the following properties:
* "sprites": [Stage and Sprites Format](#format-of-sprites)

* "variables": [Variable Format](#format-of-variables-and-lists)
* "lists":  [List Format](#format-of-variables-and-lists)
* "tempo": The tempo from the "Music" extension. Must be an integer between 20 and 500.
* "videoTransparency": The transpercancy of the stage when using the "Video Sensing" Extension. Must be a number. 
* "videoState": The state of the "Video Sensing" Extension. Must be either "on", "on flipped" or "off".
* "textToSpeechLanguage": The language of the TTS-Extension. Possible Values are listed in "Supported text to speech langauges".
* "extensionData": An object containing additional information about extensions. (Let me know if you wish more research.)
* "extensions": An array of extension acronyms, which were added to the project.
* "meta": [Meta Format](#format-of-the-metadata)
## Format of Sprites
Must be an array of sprites. The first sprite is always the stage. Then the other sprites follow in the same order as in the editor.
### Format of a Sprite 
The data of a sprite. Must be an object with the following properties:
* "isStage": Wether the sprite is the stage. Must be true for the stage(the first sprite) and false for all other sprites.

* "name": Must be "Stage" for the stage(the first sprite). For all other sprites it can be any string.
* "scripts": [Script Format](#format-of-scripts)
* "comments": [Comment Format](#format-of-comments)
* "currentCostume": The costume number of the sprite. Must be an integer and at least 0.
* "costumes": [Costume Format](#format-of-costumes-and-sounds)
* "sounds": [Sound Format](#format-of-costumes-and-sounds)
* "volume": Must be a number between 0 and 100.
* "layerOrder": The layer the sprite is on. Must always be 0 for the stage. For all other sprites it must be an integer and at least 1.  
* "visible"(*): Wether the sprite is shown or hidden. Must be a boolean.
* "position"(*): The position of the sprite on the stage. Must be a two-long array of numbers.

!!!!!(needs research)* "size"(*): The size of the sprite. Must be a positive number.

!!!!!(needs research)* "direction"(*). The direction of the sprite. Must be a number.
* "draggable"(*): Wether one can drag the sprite with the mouse in fullscreen mode. Must be a boolean.
* "rotationStyle"(*): How the sprite behaves when it rotates. Must be either "all around", "left-right" or "don't rotate".
\* Attributes which are only necessary for sprites. The stage shouldn't have these attributes.

## Format of Scripts
Must be an array of scripts. A script is defined in "Format of a Script"
### Format of a Script
Must be an object with the following properties:
    - "position": The position of a block reporter or the first block in a script. Must be a two-long array of integers.
    - "blocks": The blocks of the script(still an array even for a single block reporter). They are in order from top of the script to bottom of the script. Must be an array of blocks. A block is definded in "Format of a block"
## Format of a Block
Must be an object with the following properties:
* "opcode": The operation code of the block. [Block Opcodes](#defined-block-opcodes)
* "inputs": Must be an object of block-specific keys and object values.
```
{
    "opcode": "set [VARIABLE] to (VALUE)",
    "inputs": {
        "VALUE": {
            "mode": "block-and-text",
            "block": 3,
            "text": "0"
        }
    },
    "options": {
        "VARIABLE": "var"
    },
    "comment": null
}
```
## Defined Block Opcodes

## Format of Comments

## Format of Costumes and Sounds 

## Format of Variables and Lists

## Supported text to speech languages
Must be either null or one of these:
* "ar" (Arabic)
* "zh-cn" (Chinese (Mandarin))
* "da" (Danish)
* "nl" (Dutch)
* "en" (English)
* "fr" (French)
* "de" (German)
* "hi" (Hindi)
* "is" (Icelandic)
* "it" (Italian)
* "ja" (Japanese)
* "ko" (Korean)
* "nb" (Norgwegian)
* "pl" (Polish)
* "pt-br" (Porturguese (Brazilian))
* "pt" (Protuguese)
* "ro" (Romanian)
* "ru" (Russian)
* "es" (Spanish)
* "es-419" (Spanish (Latin American))
* "sv" (Swedish)
* "tr" (Turkish)
* "cy" (Welsh)
## Format of the Metadata
If you don't need a detailed description and just copy the example(works for PengiunMod). You will probably not ever need to change the metadata.

Must be an object with the following properties:

!!!!!!(needs research)
* "semver"
* "vm"
* "agent"
* "platform": Some information about the platform used to edit your project.
### Pengunimod Metadata Example
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