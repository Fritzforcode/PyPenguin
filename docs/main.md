# **PyPenguin Documentation**
This is the documentation for [**PyPenguin**](../README.md). 

# What a PyPenguin Project looks like
The file structure of a **PyPenguin Project** should look like this:

```
My PyPenguin Project
├─ project.json
├─ stage
│  ├─ costumes
│  │  └─ backdrop1.svg
│  └─ sounds
│     └─ Hello%20there.mp3
│     └─ I%20dont%20like%20sand.mp3
└─ sprite_Sprite1
   ├─ costumes
   │  └─ costume1.png
   └─ sounds
      └─ Squawk.wav
```
### Notes:
* `project.json` contains the data of the project.
* **costume** and **sound names** have to [percent encoded](https://en.wikipedia.org/wiki/Percent-encoding) and match their names in `project.json`, where they should not be encoded.
* **sprite names** must consist of the prefix `sprite_` and the [percent encoded](https://en.wikipedia.org/wiki/Percent-encoding) remainder.
* `stage` is used for the stage.
* **PenguinMod** seems to only support `48kHz` sounds. For a safe usage convert your sounds. 

# What a project data file looks like
The project data file([JSON file](https://en.wikipedia.org/wiki/JSON)) is called `project.json`. It should contain a json object with these properties:
| **property**             | **type**          | **optional?** | **description**                                                                                                                   
|--------------------------|-------------------|---------------|-----------------------------------------------------------------------------------------------------------------------------------
| `"sprites"`              | array of objects  | no            | Contains stage and sprites of the project. [Docs](sprites.md)                                                                     
| `"globalVariables"`      | array of objects  | no            | The defined "For all sprites" variables. [Docs](variables_lists.md#what-variable-definitions-look-like)                           
| `"globalLists"`          | array of objects  | no            | The defined "For all sprites" lists. [Docs](variables_lists.md#what-list-definitions-look-like)                                   
| `"extensions"`           | array of strings  | no            | The string ids of the included extensions. [Docs](other.md#extensions)                                                            
| `"monitors"`             | array of objects  | no            | The shown and hidden reporters. eg. a reporter for the "my variable" variable. [Docs](monitors.md)                                
| `"tempo"`                | integer           | yes           | The tempo of the music extension. Must be between `20` and `500`.                                                                 
| `"videoTransparency"`    | integer / float   | yes           | The transapency of the screen when using the **Video Sensing** extension.                                                         
| `"videoState"`           | string            | yes           | The state of the camera when using the **Video Sensing** extension. Either `"on"`, `"on flipped"` or `"off"`.                     
| `"textToSpeechLanguage"` | string            | yes           | The language when using the "Text to Speech" extension. Must be either `null` or one of [these](other.md#text-to-speech-languages)
| `"extensionData"`        | object            | yes           | Data about extensions. Is not completely demystified.                                                                             
| `"extensionURLs"`        | object of strings | yes           | Contains the urls of external extensions. eg. `{"Bitwise": "https://extensions.turbowarp.org/bitwise.js"}`                        

