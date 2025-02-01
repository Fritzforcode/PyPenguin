[BACK TO SPRITES](sprites.md)  
[BACK TO SCRIPTS](scripts.md)  

# What a comment looks like
A comment must be an object with the following properties:
| **property**    | **type**         | **description**                                                                                                                 
|-----------------|------------------|---------------------------------------------------------------------------------------------------------------------------------
| `"position"`    | array coordinate | The position of the comment within the coding space.                                                             
| `"size"`        | array coordinate | The size of the comment when its expanded. The width must be at least `52` and the height at least `32`.
| `"isMinimized"` | boolean          | Wether the comment is minimized or expanded.                                                           
| `"text"`        | string           | The text content of the comment.                                                        

### Example
```
{
    "position": [0, 0],
    "size": [200, 80],
    "isMinimized": False,
    "text": "This block does something"
}
```
