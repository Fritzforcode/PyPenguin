# **PyPenguin Documentation**
 This is the documentation for [**PyPenguin**](README.md). 

The file structure of a **PyPenguin Project** could look like this:

```
My PyPenguin Project
├─ project.json
├─ #Stage
│  ├─ costumes
│  │  └─ backdrop1.svg
│  └─ sounds
│     └─ Hello%20there.mp3
└─ Sprite1
   ├─ costumes
   │  └─ costume1.png
   └─ sounds
      └─ Squawk.wav
```
### Notes:
* You can find the example [here](examples/).
* `project.json` is documented [below](#format-of-the-project-projectjson).
* `sprite`, `costume` and `sound` names have to [percent encoded](https://en.wikipedia.org/wiki/Percent-encoding) and match their names in `project.json`, where they should not be encoded.
* `#Stage` is used for the stage to avoid overlapping with sprite names.
* **PenguinMod** seems to only support `48kHz` sounds. For a safe usage convert your sounds. 


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

* `"meta"`: [Metadata Format](#format-of-the-metadata).
### [Example](#projectjson-example)


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

### [Example (Sprite)](#sprite-example)
### [Example (Stage)](#stage-example)

## Format of Scripts
Must be an array of scripts. A script must be an object with the following properties:
* `"position"`: The position of a block reporter or the first block in a script. Must be a two-long array of integers.

* `"blocks"`: The blocks of the script in an array (even for a (single) block reporter). They are in order from top of the script to bottom of the script. [Block Format](#format-of-a-block).

### [Example](#script-example)

## Format of a Block
Must be an object with the following properties:
* `"opcode"`: The operation code of the block. [Block Opcodes](#defined-block-opcodes).

* `"inputs"`: The inputs of the block. [Input Format](#format-of-inputs).

* `"options"`: The options of the block. [Option Format](#format-of-options).

* `"comment"`: The comment attached to the block. Must be either `null` or an object following the [Comment Format](#format-of-comments).

### [Example](#block-example)

## Format of Inputs
Must be an object of block-specific keys and values. Each value must follow one of these modes:
* **Block and Text Mode**: Allows text and optionally a block in the input field. Used in the `"broadcast"`, `"number"` and `"text"` input types. 
* **Block Only Mode**: Allows only text in the input field.

You can see the input types of blocks [HERE](assets/opcode_database.jsonc).

An input value must be an object with the following properties:
* `"mode"`: must be `"block-and-text"` for **Block and Text Mode** and `"block-only"` for **Block Only Mode**.

* `"block"`: Only exists in **Block and Text Mode**. The block that is in the input field. Must be either `null` for no block or a block following the [Block Format](#format-of-a-block).

* `"text"`: The text of the input field. Must be a string.
### [Example](#inputs-example)


## Format of Options 
Must be an object of block-specific keys and values. Currently there is only one option value type, a string.
### [Example](#options-example)


## Format of Comments
Must be either `null` or an object with the following properties:
* `"position"`: The position of the comment in the sprite. Must be a two-long array of numbers.

* `"size"`: The size of the comment when it isn't minimized. Must be a two long array of numbers.

* `"isMinimzed"`: Wether the comment is folded (when `true`) in or expanded (when `false`). Must be a boolean. 

* `"text"`: The text of the comment. Must be a string.
### [Example](#comment-example)


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
### [Example (Costume)](#costume-example)
### [Example (Sound)](#sound-example)



## Format of Variables and Lists
Must be an object with the following properties:
* `"name"`: The name of the variable/list. Must be a non-empty string.

* `"currentValue"`: The value the variable/list currently has. For a variable this must be a string or a number. For a list this must be an array. Each item must be either a string or a number.

* `"monitor"`: Must be either null or an object following the [Monitor Format](#format-of-variable-and-list-monitors)

* `"isCloudVariable"(*)`: Wether the variable is a cloud variable. Must be a boolean.

\* only exists for variables in the `"globalVariables"` array.
### [Example (Variable)](#variable-example)
### [Example (List)](#list-example)



## Format of Variable and List Monitors
Must be either null or an object with the following properties:
* `"visible"`: Wether the monitor is shown on the stage. Must be a boolean.

* `"size"`: The size of the monitor. Must be a two-long array of integers.

* `"position"`: The position of the monitor on the stage.

* `"sliderMin"(*)`: The minimum of the slider. (when the monitor is in the slider mode.) Must be an integer when `"onlyIntegers"` is `true` otherwise a number.

* `"sliderMax"(*)`: The maximum of the slider. (when the monitor is in the slider mode.) Must be an integer when `"onlyIntegers"` is `true` otherwise a number.

* `"onlyIntegers"(*)`: If `true` only integers are allowed in the slider.

\* only exists for variables.
### [Example (Variable)](#variable-monitor-example)
### [Example (List)](#list-monitor-example)







## Format of the Metadata
If you don't need a detailed description and just copy the example. You will probably not ever need to change the metadata.

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

# **Examples**

## `project.json` Example
```
{
    "sprites": [
        {
            "isStage": true,
            "name": "Stage",
            "scripts": [],
            "comments": [],
            "currentCostume": 0,
            "costumes": [
                {
                    "name": "backdrop1",
                    "dataFormat": "svg",
                    "fileStem": "cd21514d0531fdffb22204e0ec5ed84a",
                    "bitmapResolution": 1,
                    "rotationCenter": [240, 180]
                }
            ],
            "sounds": [
                {
                    "name": "Hello there",
                    "dataFormat": "mp3",
                    "fileStem": "ded064067963e912e985745cf0fec86a",
                    "rate": 48000,
                    "sampleCount": 65201
                }
            ],
            "volume": 100
        },
        {
            "isStage": false,
            "name": "Sprite1",
            "scripts": [
                {
                    "position": [0, 0],
                    "blocks": [
                        {
                            "opcode": "set [VARIABLE] to (VALUE)",
                            "inputs": {
                                "VALUE": {
                                    "mode": "block-and-text",
                                    "block": null,
                                    "text": "test123test"
                                }
                            },
                            "options": {
                                "VARIABLE": "global variable"
                            },
                            "comment": {
                                "position": [362.81296730041504, 8],
                                "size": [200, 200],
                                "isMinimized": false,
                                "text": "setting variables"
                            }
                        },
                        {
                            "opcode": "set [VARIABLE] to (VALUE)",
                            "inputs": {
                                "VALUE": {
                                    "mode": "block-and-text",
                                    "block": null,
                                    "text": "456"
                                }
                            },
                            "options": {
                                "VARIABLE": "local variable"
                            },
                            "comment": null
                        },
                        {
                            "opcode": "add (ITEM) to [LIST]",
                            "inputs": {
                                "ITEM": {
                                    "mode": "block-and-text",
                                    "block": null,
                                    "text": "789"
                                }
                            },
                            "options": {
                                "LIST": "global list"
                            },
                            "comment": null
                        },
                        {
                            "opcode": "add (ITEM) to [LIST]",
                            "inputs": {
                                "ITEM": {
                                    "mode": "block-and-text",
                                    "block": null,
                                    "text": "ABC"
                                }
                            },
                            "options": {
                                "LIST": "local list"
                            },
                            "comment": null
                        }
                    ]
                }
            ],
            "comments": [
                {
                    "position": [149.68792330747857, -327.12618351331304],
                    "size": [200, 200],
                    "isMinimized": false,
                    "text": "free floating comment"
                }
            ],
            "currentCostume": 0,
            "costumes": [
                {
                    "name": "costume1",
                    "dataFormat": "png",
                    "fileStem": "b86efb7f23387300cf9037a61f328ab9",
                    "bitmapResolution": 2,
                    "rotationCenter": [158, 146]
                }
            ],
            "sounds": [
                {
                    "name": "Squawk",
                    "dataFormat": "wav",
                    "fileStem": "e140d7ff07de8fa35c3d1595bba835ac",
                    "rate": 48000,
                    "sampleCount": 17867
                }
            ],
            "volume": 100,
            "localVariables": [
                {
                    "name": "local variable",
                    "currentValue": 456,
                    "monitor": {
                        "visible": true,
                        "size": [0, 0],
                        "position": [155, 268],
                        "sliderMin": -100,
                        "sliderMax": 500,
                        "onlyIntegers": true
                    }
                }
            ],
            "localLists": [
                {
                    "name": "local list",
                    "currentValue": [
                        "ABC"
                    ],
                    "monitor": {
                        "visible": true,
                        "size": [0, 0],
                        "position": [361, 92]
                    }
                }
            ],
            "layerOrder": 1,
            "visible": true,
            "position": [0, 0],
            "size": 100,
            "direction": 90,
            "draggable": false,
            "rotationStyle": "all around"
        }
    ],
    "globalVariables": [
        {
            "name": "global variable",
            "currentValue": "test123test",
            "monitor": {
                "visible": true,
                "size": [0, 0],
                "position": [159, 75],
                "sliderMin": 0,
                "sliderMax": 100,
                "onlyIntegers": true
            },
            "isCloudVariable": false
        }
    ],
    "globalLists": [
        {
            "name": "global list",
            "currentValue": [
                789
            ],
            "monitor": {
                "visible": true,
                "size": [0, 0],
                "position": [15, 7]
            }
        }
    ],
    "tempo": 60,
    "videoTransparency": 50,
    "videoState": "on",
    "textToSpeechLanguage": null,
    "extensionData": {},
    "extensions": [],
    "meta": {
        "semver": "3.0.0",
        "vm": "0.2.0",
        "agent": "",
        "platform": {
            "name": "PenguinMod",
            "url": "https://penguinmod.com/",
            "version": "stable"
        }
    }
}
```

## Sprite Example
```
{
    "isStage": false,
    "name": "Sprite1",
    "scripts": [
        {
            "position": [0, 0],
            "blocks": [
                {
                    "opcode": "set [VARIABLE] to (VALUE)",
                    "inputs": {
                        "VALUE": {
                            "mode": "block-and-text",
                            "block": null,
                            "text": "test123test"
                        }
                    },
                    "options": {
                        "VARIABLE": "global variable"
                    },
                    "comment": {
                        "position": [362.81296730041504, 8],
                        "size": [200, 200],
                        "isMinimized": false,
                        "text": "setting variables"
                    }
                },
                {
                    "opcode": "set [VARIABLE] to (VALUE)",
                    "inputs": {
                        "VALUE": {
                            "mode": "block-and-text",
                            "block": null,
                            "text": "456"
                        }
                    },
                    "options": {
                        "VARIABLE": "local variable"
                    },
                    "comment": null
                },
                {
                    "opcode": "add (ITEM) to [LIST]",
                    "inputs": {
                        "ITEM": {
                            "mode": "block-and-text",
                            "block": null,
                            "text": "789"
                        }
                    },
                    "options": {
                        "LIST": "global list"
                    },
                    "comment": null
                },
                {
                    "opcode": "add (ITEM) to [LIST]",
                    "inputs": {
                        "ITEM": {
                            "mode": "block-and-text",
                            "block": null,
                            "text": "ABC"
                        }
                    },
                    "options": {
                        "LIST": "local list"
                    },
                    "comment": null
                }
            ]
        }
    ],
    "comments": [
        {
            "position": [149.68792330747857, -327.12618351331304],
            "size": [200, 200],
            "isMinimized": false,
            "text": "free floating comment"
        }
    ],
    "currentCostume": 0,
    "costumes": [
        {
            "name": "costume1",
            "dataFormat": "png",
            "fileStem": "b86efb7f23387300cf9037a61f328ab9",
            "bitmapResolution": 2,
            "rotationCenter": [158, 146]
        }
    ],
    "sounds": [
        {
            "name": "Squawk",
            "dataFormat": "wav",
            "fileStem": "e140d7ff07de8fa35c3d1595bba835ac",
            "rate": 48000,
            "sampleCount": 17867
        }
    ],
    "volume": 100,
    "localVariables": [
        {
            "name": "local variable",
            "currentValue": 456,
            "monitor": {
                "visible": true,
                "size": [0, 0],
                "position": [155, 268],
                "sliderMin": -100,
                "sliderMax": 500,
                "onlyIntegers": true
            }
        }
    ],
    "localLists": [
        {
            "name": "local list",
            "currentValue": [
                "ABC"
            ],
            "monitor": {
                "visible": true,
                "size": [0, 0],
                "position": [361, 92]
            }
        }
    ],
    "layerOrder": 1,
    "visible": true,
    "position": [0, 0],
    "size": 100,
    "direction": 90,
    "draggable": false,
    "rotationStyle": "all around"
}
```

## Stage Example
```
{
    "isStage": true,
    "name": "Stage",
    "scripts": [],
    "comments": [],
    "currentCostume": 0,
    "costumes": [
        {
            "name": "backdrop1",
            "dataFormat": "svg",
            "fileStem": "cd21514d0531fdffb22204e0ec5ed84a",
            "bitmapResolution": 1,
            "rotationCenter": [240, 180]
        }
    ],
    "sounds": [
        {
            "name": "Hello there",
            "dataFormat": "mp3",
            "fileStem": "ded064067963e912e985745cf0fec86a",
            "rate": 48000,
            "sampleCount": 65201
        }
    ],
    "volume": 100
}
```

## Script Example
```
{
    "position": [0, 0],
    "blocks": [
        {
            "opcode": "set [VARIABLE] to (VALUE)",
            "inputs": {
                "VALUE": {
                    "mode": "block-and-text",
                    "block": null,
                    "text": "test123test"
                }
            },
            "options": {
                "VARIABLE": "global variable"
            },
            "comment": {
                "position": [362.81296730041504, 8],
                "size": [200, 200],
                "isMinimized": false,
                "text": "setting variables"
            }
        },
        {
            "opcode": "set [VARIABLE] to (VALUE)",
            "inputs": {
                "VALUE": {
                    "mode": "block-and-text",
                    "block": null,
                    "text": "456"
                }
            },
            "options": {
                "VARIABLE": "local variable"
            },
            "comment": null
        },
        {
            "opcode": "add (ITEM) to [LIST]",
            "inputs": {
                "ITEM": {
                    "mode": "block-and-text",
                    "block": null,
                    "text": "789"
                }
            },
            "options": {
                "LIST": "global list"
            },
            "comment": null
        },
        {
            "opcode": "add (ITEM) to [LIST]",
            "inputs": {
                "ITEM": {
                    "mode": "block-and-text",
                    "block": null,
                    "text": "ABC"
                }
            },
            "options": {
                "LIST": "local list"
            },
            "comment": null
        }
    ]
}
```

## Block Example
```
{
    "opcode": "set [VARIABLE] to (VALUE)",
    "inputs": {
        "VALUE": {
            "mode": "block-and-text",
            "block": null,
            "text": "test123test"
        }
    },
    "options": {
        "VARIABLE": "global variable"
    },
    "comment": {
        "position": [362.81296730041504, 8],
        "size": [200, 200],
        "isMinimized": false,
        "text": "setting variables"
    }
}
```

## Inputs Example
```
{
    "VALUE": {
        "mode": "block-and-text",
        "block": null,
        "text": "test123test"
    }
}
```
#### Note: `"block"` can be a [block](#block-example).

## Options Example
```
{
    "VARIABLE": "global variable"
}
```

## Comment Example
```
{
    "position": [362.81296730041504, 8],
    "size": [200, 200],
    "isMinimized": false,
    "text": "setting variables"
}
```

## Costume Example
```
{
    "name": "costume1",
    "dataFormat": "png",
    "fileStem": "b86efb7f23387300cf9037a61f328ab9",
    "bitmapResolution": 2,
    "rotationCenter": [158, 146]
}
```

## Sound Example
```
{
    "name": "Hello there",
    "dataFormat": "mp3",
    "fileStem": "ded064067963e912e985745cf0fec86a",
    "rate": 48000,
    "sampleCount": 65201
}
```

## Variable Example
```
{
    "name": "global variable",
    "currentValue": "test123test",
    "monitor": {
        "visible": true,
        "size": [0, 0],
        "position": [159, 75],
        "sliderMin": 0,
        "sliderMax": 100,
        "onlyIntegers": true
    },
    "isCloudVariable": false
}
```

## List Example
```
{
    "name": "global list",
    "currentValue": [
        789
    ],
    "monitor": {
        "visible": true,
        "size": [0, 0],
        "position": [15, 7]
    }
}
```

## Variable Monitor Example
```
{
    "visible": true,
    "size": [0, 0],
    "position": [159, 75],
    "sliderMin": 0,
    "sliderMax": 100,
    "onlyIntegers": true
}
```

## List Monitor Example
```
{
    "visible": true,
    "size": [0, 0],
    "position": [15, 7]
}
```

# **Possible Values for Constants**

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

