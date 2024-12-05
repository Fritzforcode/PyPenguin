# **PyPenguin Documentation**
This is the documentation for [**PyPenguin**](../README.md). 

# File Structure
The file structure of a **PyPenguin Project** should look like this:

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
* `project.json` is documented [below](#format-of-the-project-projectjson).
* `sprite`, `costume` and `sound` names have to [percent encoded](https://en.wikipedia.org/wiki/Percent-encoding) and match their names in `project.json`, where they should not be encoded.
* `#Stage` is used for the stage to avoid overlapping with sprite names.
* **PenguinMod** seems to only support `48kHz` sounds. For a safe usage convert your sounds. 




# **project.json**
The Project data must be an object with the following properties:
* `"sprites"`: [Sprite Format](sprites.md)

* `"globalVariables"`: [Variable Format](variables_lists.md#format-of-variables)

* `"globalLists"`:  [List Format](variables_lists.md#format-of-list)

* `"tempo"`: The tempo of the **Music** extension. Must be an integer between `20` and `500`.

* `"videoTransparency"`: The transpercancy of the stage when using the "Video Sensing" Extension. Must be a number. 

* `"videoState"`: The state of the **Video Sensing** Extension. Must be either `"on"`, `"on flipped"` or `"off"`.

* `"textToSpeechLanguage"`: The language of the **Text to Speech** Extension. Must be either `null` or one of [these](other.md#text-to-speech-languages)

* `"monitors"`: The monitors of the project. [Monitor Format](monitors.md)

* `"extensionData"`: An object containing additional information about extensions.

* `"extensions"`: An array of extension acronyms, which were added to the project. [Currently supported extensions](extensions.md)

### TODO: ADD ILLUSTRATION IMAGE

