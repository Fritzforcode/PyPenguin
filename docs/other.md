[BACK TO START](main.md)  
[BACK TO MONITORS](monitors.md)  

# Text to Speech Languages
* `"Arabic (ar)"`
* `"Chinese (Mandarin) (zh-cn)"`
* `"Danish (da)"`
* `"Dutch (nl)"`
* `"English (en)"`
* `"French (fr)"`
* `"German (de)"`
* `"Hindi (hi)"`
* `"Icelandic (is)"`
* `"Italian (it)"`
* `"Japanese (ja)"`
* `"Korean (ko)"`
* `"Norwegian (nb)"`
* `"Polish (pl)"`
* `"Portuguese (Brazilian) (pt-br)"`
* `"Portuguese (pt)"`
* `"Romanian (ro)"`
* `"Russian (ru)"`
* `"Spanish (es)"`
* `"Spanish (Latin American) (es-419)"`
* `"Swedish (sv)"`
* `"Turkish (tr)"`
* `"Welsh (cy)"`

# Extensions
To add an extension to your project add the extension's id to `"extensions"`. External extensions(eg. **Bitwise**) require a link being added to `"extensionURLs"`
* **Music** id: `"music"`
* **Pen** id: `"pen"`
* **Animated Text** id: `"text"`
* **Video Sensing** id: `"videoSensing"`
* **Text to Speech** id: `"text2speech"`
* **Translate** id: `"translate"`
* **Makey Makey** id: `"makeymakey"`
* **Files** id: `"twFiles"`
* **Bitwise** id: `"Bitwise"` + add to extension urls: `{"Bitwise": "https://extensions.turbowarp.org/bitwise.js"}`
* **JSON** id: `"jgJSON"`

### Example
```
{
    ...
    "extensions": ["pen", "jgJSON", "Bitwise"],
    "extensionURLs": {
        "Bitwise": "https://extensions.turbowarp.org/bitwise.js"
    },
}
```

# Menu Opcodes
* `"x position"`
* `"y position"`
* `"direction"`
* `"bubble width"`
* `"bubble height"`
* `"x stretch"`
* `"y stretch"`
* `"[EFFECT] sprite effect"`
* `"tint color"`
* `"visible?"`
* `"layer"`
* `"costume [PROPERTY]"`
* `"backdrop [PROPERTY]"`
* `"size"`
* `"[EFFECT] sound effect"`
* `"volume"`
* `"answer"`
* `"mouse down?"`
* `"mouse clicked?"`
* `"mouse x"`
* `"mouse y"`
* `"clipboard item"`
* `"draggable?"`
* `"loudness"`
* `"loud?"`
* `"timer"`
* `"current [PROPERTY]"`
* `"days since 2000"`
* `"username"`
* `"logged in?"`
* `"value of [VARIABLE]"`
* `"value of [LIST]"`
* `"tempo"`
* `"is text visible?"`
* `"get width of the text"`
* `"get height of the text"`
* `"displayed text"`
* `"get data uri of last rendered text"`
* `"language"`
