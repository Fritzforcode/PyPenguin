[BACK TO START](main.md)  
[BACK TO SPRITES](sprites.md)  

## What a Variable Definition looks like
Must be an object with the following properties:
* `"name"`: The name of the variable. Must be a non-empty string.

* `"currentValue"`: The value the variable currently has as a string or number. 

* `"isCloudVariable"`: Wether the variable is a cloud variable. Must be a boolean. Only exists for global variables (variables in the `"globalVariables"` array).

## What a List Definition looks like
Must be an object with the following properties:
* `"name"`: The name of the list. Must be a non-empty string.

* `"currentValue"`: The value the list currently has. For a list this must be an array. Each item must be either a string or a number.
