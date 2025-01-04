# **PyPenguin Documentation**
This is the documentation for [**PyPenguin**](../README.md). 

# What a PyPenguin Project looks like
## File Structure
The file structure of a **PyPenguin Project** should look like this:

```
My PyPenguin Project
├─ project.json
├─ stage
│  ├─ costumes
│  │  └─ backdrop1.svg
│  └─ sounds
│     └─ Hello%20there.mp3
└─ sprite_Sprite1
   ├─ costumes
   │  └─ costume1.png
   └─ sounds
      └─ Squawk.wav
```
### Notes:
* `project.json` contains the data of the project.
* `sprite`, `costume` and `sound` names have to [percent encoded](https://en.wikipedia.org/wiki/Percent-encoding) and match their names in `project.json`, where they should not be encoded.
* `#Stage` is used for the stage to avoid overlapping with sprite names.
* **PenguinMod** seems to only support `48kHz` sounds. For a safe usage convert your sounds. 

# What a project data file looks like
The project data file must be ˋJSONˋ file called ˋproject.jsonˋ. It should contain a json object with these properties:
* `"sprites"`: Contains stage and sprites of the project. [Docs](sprites_new.md)

* ˋ"globalVariables"ˋ: An array of the defined "For all sprites" variables. [Docs]()

* ˋ"globalLists"ˋ: An array of the defined "For all sprites" lists. [Docs]()

* ˋ"extensions"ˋ: An array of the ids of the included extensions.

* ˋ"monitors"ˋ: An array of shown and hidden reporters. eg. a reporter for the "my variable" variable. [Docs]()

Optional Properties:
* ˋ"tempo"ˋ: The tempo of the music extension. An integer between ˋ20ˋ and ˋ500ˋ.

* ˋ"videoTransparency"ˋ: The transapency of the screen when using the "Video Sensing" extension. A number.

* ˋ"videoState"ˋ: The state of the camera when using the "Video Sensing" extension. Either ˋ"on"ˋ, ˋ"on flipped"ˋ or ˋ"off"ˋ.

* ˋ"textToSpeechLanguage"ˋ: The language when using the "Text to Speech" extension. Must be either `null` or one of [these](other.md#text-to-speech-languages)

* ˋ"extensionData"ˋ: Data about extensions. Is not completely demystified.

* ˋ"extensionURLs"ˋ: Contains the urls of external extensions. eg. ˋ{"Bitwise": "https://extensions.turbowarp.org/bitwise.js"}ˋ
