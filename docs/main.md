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
* `sprite`, `costume` and `sound` names have to [percent encoded](https://en.wikipedia.org/wiki/Percent-encoding) and match their names in `project.json`, where they should not be encoded.
* `#Stage` is used for the stage to avoid overlapping with sprite names.
* **PenguinMod** seems to only support `48kHz` sounds. For a safe usage convert your sounds. 

# What a project data file looks like
### The project data file([JSON]([text](https://en.wikipedia.org/wiki/JSON)) file) is called `project.json`. It should contain a json object with these properties:
* `"sprites"`: Contains stage and sprites of the project. [Docs](sprites.md)

* `"globalVariables"`: An array of the defined "For all sprites" variables. [Docs](variables_lists.md#what-variable-definitions-look-like)

* `"globalLists"`: An array of the defined "For all sprites" lists. [Docs](variables_lists.md#what-list-definitions-look-like)

* `"extensions"`: An array of the string ids of the included extensions. [Docs](other.md#extensions)

* `"monitors"`: An array of shown and hidden reporters. eg. a reporter for the "my variable" variable. [Docs](monitors.md)

### Optional Properties:
* `"tempo"`: The tempo of the music extension. An integer between `20` and `500`.

* `"videoTransparency"`: The transapency of the screen when using the **Video Sensing** extension. A number.

* `"videoState"`: The state of the camera when using the **Video Sensing** extension. Either `"on"`, `"on flipped"` or `"off"`.

* `"textToSpeechLanguage"`: The language when using the "Text to Speech" extension. Must be either `null` or one of [these](other.md#text-to-speech-languages)

* `"extensionData"`: Data about extensions. Is not completely demystified.

* `"extensionURLs"`: Contains the urls of external extensions. eg. `{"Bitwise": "https://extensions.turbowarp.org/bitwise.js"}`
