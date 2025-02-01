[BACK](sprites.md)

# What a costume looks like
A costume be an object with these properties:
| **property**         | **type**         | **description**                                                                                                                                                                                                       
|----------------------|------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
| `"name"`             | string           | The name of the costume. Mustn't be encoded. [Its equivalent file in the project directory](main.md#what-a-pypenguin-project-looks-like) has to be [percent encoded](https://en.wikipedia.org/wiki/Percent-encoding). 
| `"extension"`        | file extension   | The file extension of the costume file. eg. `"svg"`                                                                                                                                                                   
| `"bitmapResolution"` | integer          | The resolution of the bitmap in bitmap image types. Usually `1`.                                                                                                                                                      
| `"rotationCenter"`   | array coordinate | A vector from the **center point** of the image to the **rotation center point** of the costume image.       

### Example
```
{
    "name": "costume1",
    "extension": "svg",
    "bitmapResolution": 1,
    "rotationCenter": [0, 0],
}
```

# What a sound looks like
A sound must be an object with these properties:
| **property**    | **type**       | **description**                                                                                                                                                     
|-----------------|----------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------
| `"name"`        | string         | The name of the sound. Mustn't be encoded. Its equivalent file in the project directory has to be [percent encoded](https://en.wikipedia.org/wiki/Percent-encoding).
| `"extension"`   | file extension | The file extension of the sound file. eg. `"wav"`                                                                                                                   
| `"rate"`        | integer        |  The sample rate of the sound. Must be an integer and at least `1`. Seems to always be `48000`. I suggest conveting your sounds to 48kHz before using them.         
| `"sampleCount"` | integer        | The number of samples in the sound. `Sample Count = Sampling Rate(eg. 48kHz) × Duration`                                                                            


### Example
```
{
    "name": "Squawk",
    "extension": "wav",
    "rate": 48000,
    "sampleCount": 17867,
}
```
