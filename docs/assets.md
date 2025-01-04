[BACK](sprites.md)

# What a costume looks like
### Must be an object wit the following properties:
* `"name"`: Them name of the costume. Mustn't be encoded. Its equivalent file in the project directory has to be [percent encoded](https://en.wikipedia.org/wiki/Percent-encoding).
* `"extension"`: The file extension of the costume file. eg. `".svg"`
* `"bitmapResolution"`: The resolution of the bitmap in bitmap image types. Usually `1`.
* `"rotationCenter"`: A vector from the **center point** of the image to the **rotation center point** of the costume image.

# What a sound looks like
### Must be an object wit the following properties:
* `"name"`: Them name of the sound. Mustn't be encoded. Its equivalent file in the project directory has to be [percent encoded](https://en.wikipedia.org/wiki/Percent-encoding).
* `"extension"`: The file extension of the sound file. eg. `".wav"`
* `"rate"`: The sample rate of the sound. Must be an integer and at least `1`. Seems to always be `48000`. I suggest conveting your sounds to 48kHz before using them.
* `"sampleCount"`: The number of samples in the sound. `Sample Count = Sampling Rate(eg. 48kHz) × Duration`

### You can get the Pengiunmod sounds and costumes here:
* [Costumes](https://github.com/PenguinMod/PenguinMod-ObjectLibraries/tree/main/files/images)
* [Sounds](https://github.com/PenguinMod/PenguinMod-ObjectLibraries/tree/main/files/sounds)  