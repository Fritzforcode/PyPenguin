[BACK](main.md)

# What a sprite looks like
The `"sprites"` attribute of the project data must be an array of sprites. The first sprite is always the stage. Then the other sprites follow in the same order as in the editor. A sprite must be an object with the following properties:
| **property**       | **type**         | **sprite only** | **description**                                                                                                                      
|--------------------|------------------|-----------------|--------------------------------------------------------------------------------------------------------------------------------------
| `"isStage"`        | boolean          | no              | Wether the sprite is the stage. Must be `true` for the stage(the first sprite) and `false` for all other sprites.                    
| `"name"`           | string           | no              | Must be `"Stage"` for the stage(the first sprite). For all other sprites this can be any string.                                     
| `"scripts"`        | array of objects | no              | The scripts of this sprite. [Docs](scripts.md)                                                                                       
| `"comments"`       | array of objects | no              | Comments, that are not attached to a block. [Docs](comments.md)                                                                      
| `"currentCostume"` | integer          | no              | he costume number of the sprite. Must be an integer and at least `0`. Must refer to the index of an existing costume in ˋ"costumes"ˋ.
| `"costumes"`       | array of objects | no              | The costumes/brackdrops of the sprite. [Docs](assets.md#what-a-costume-looks-like)                                                   
| `"sounds"`         | array of objects | no              | The sounds of the sprite. [Docs](assets.md#what-a-sound-looks-like)                                                                  
| `"volume"`         | number           | no              | The sprite volume(applies to its sounds). Must be a number between `0` and `100`.                                                    
| `"localVariables"` | array of objects | yes             | The `"For this sprite only"` variables of this sprite. [Docs](variables_lists.md#what-a-variable-definition-looks-like).             
| `"localLists"`     | array of objects | yes             | The `"For this sprite only"` lists of this sprite. [Docs](variables_lists.md#what-a-list-definition-looks-like).                     
| `"layerOrder"`     | integer          | yes             | The layer the sprite is on. Must be at least `1`. eg. Sprite A is on top of Sprite B because it has a higher `"layerOrder"`.         
| `"visible"`        | boolean          | yes             | Wether the sprite is shown or hidden.                                                                                                
| `"position"`       | array coordinate | yes             | The position of the sprite on the stage.                                                                                             
| `"size"`           | positive number  | yes             | The size of the sprite.                                                                                                              
| `"direction"`      | number           | yes             | The direction of the sprite. Must be between `-180` and `180`.                                                                       
| `"draggable"`      | boolean          | yes             | Wether one can drag the sprite with the mouse in fullscreen mode.                                                                    
| `"rotationStyle"`  | string           | yes             | How the sprite behaves when rotated. Must be either `"all around"`, `"left-right"` or `"don't rotate"`.                              
