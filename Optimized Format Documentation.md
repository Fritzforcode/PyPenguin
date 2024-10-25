Properties of objects are always required except when labeled "optional"


## Structure of the Project
The Project data must be an object with the following properties:
    - "sprites": Defined in "Structure of Sprites".
    - "variables": Defined in "Structure of Variables and Lists".
    - "lists": Defined in "Structure of Variables and Lists".
    - "tempo": The tempo from the "Music" extension. Must be an integer between 20 and 500.
    - "videoTransparency": The transpercancy of the stage when using the "Video Sensing" Extension. Must be a number. 
    - "videoState": The state of the "Video Sensing" Extension. Must be either "on", "on flipped" or "off".
    - "textToSpeechLanguage": The language of the TTS-Extension. Possible Values are listed in "Supported text to speech langauges".
    - "extensionData": An object containing additional information about extensions. (Let me know if you wish more research.)
    - "extensions": An array of extension acronyms, which were added to the project.
    - "meta": Defined in "Structure of the Metadata"

## Structure of Sprites
Must be an array of sprites. The first sprite is always the stage. Then the other sprites follow in the same order as in the editor.
### Structure of a Sprite 
The data of a sprite. Must be an object with the following properties:
    - "isStage": Wether the sprite is the stage. Must be true for the stage(the first sprite) and false for all other sprites.
    - "name": Must be "Stage" for the stage(the first sprite). For all other sprites it can be any string.
    - "scripts": Defined in "Structure of Scripts".
    - "comments": Defined in "Structure of Comments".
    - "currentCostume": The costume number of the sprite. Must be an integer and at least 0.
    - "costumes": Defined in "Structure of Costumes and Sounds".
    - "sounds": Defined in "Structure of Costumes and Sounds".
    - "volume": Must be a number between 0 and 100.
    - "layerOrder": The layer the sprite is on. Must always be 0 for the stage. For all other sprites it must be an integer and at least 1.  
    - "visible"(*): Wether the sprite is shown or hidden. Must be a boolean.
    - "position"(*): The position of the sprite on the stage. Must be a two-long array of numbers.
!!!!!(needs research)    - "size"(*): The size of the sprite. Must be a positive number.
!!!!!(needs research)    - "direction"(*). The direction of the sprite. Must be a number.
    - "draggable"(*): Wether one can drag the sprite with the mouse in fullscreen mode. Must be a boolean.
    - "rotationStyle"(*): How the sprite behaves when it rotates. Must be either "all around", "left-right" or "don't rotate".
* Attributes which are only necessary for sprites. The stage shouldn't have these attributes.

## Structure of Scripts
Must be an array of scripts. A script is defined in "Structure of a Script"
## Structure of a Script
Must be an object with the following properties:
    - "position": The position of a block reporter or the first block in a script. Must be a two-long array of integers.
    - "blocks": The blocks of the script(still an array even for a single block reporter). They are in order from top of the script to bottom of the script. Must be an array of blocks. A block is definded in "Structure of a block"
## Structure of a block
Must be an object with the following properties:
    - "opcode": The operation code of the block. Possible Values are defined in "Defined Block Opcodes"
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
## Defined Block Opcodes

## Structure of Comments

## Structure of Costumes and Sounds 

## Structure of Variables and Lists

## Supported text to speech languages
Must be either null or one of these:
    - "ar" (Arabic)
    - "zh-cn" (Chinese (Mandarin))
    - "da" (Danish)
    - "nl" (Dutch)
    - "en" (English)
    - "fr" (French)
    - "de" (German)
    - "hi" (Hindi)
    - "is" (Icelandic)
    - "it" (Italian)
    - "ja" (Japanese)
    - "ko" (Korean)
    - "nb" (Norgwegian)
    - "pl" (Polish)
    - "pt-br" (Porturguese (Brazilian))
    - "pt" (Protuguese)
    - "ro" (Romanian)
    - "ru" (Russian)
    - "es" (Spanish)
    - "es-419" (Spanish (Latin American))
    - "sv" (Swedish)
    - "tr" (Turkish)
    - "cy" (Welsh)

## Structure of the Metadata
If you don't need a detailed description and just copy the example(works for PengiunMod). You will probably not ever need to change the metadata.
Must be an object with the following properties:
!!!!!!(needs research)
    - "semver"
    - "vm"
    - "agent"
    - "platform": Some information about the platform used to edit your project.
### Pengunimod Metadata Example
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