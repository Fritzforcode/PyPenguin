[BACK TO START](main.md)  
[BACK TO SPRITES](sprites.md)  

## What a Variable Definition looks like
A variable defintion must be an object with the following properties:
| **property**        | **type**         | **description**                                                                                                                           
|---------------------|------------------|-------------------------------------------------------------------------------------------------------------------------------------------
| `"name"`            | non-empty string | The name of the variable.                                                                                                                 
| `"currentValue"`    | string \| number | The value the variable currently has.                                                                                                     
| `"isCloudVariable"` | boolean          | Wether the variable is a cloud variable. Must be a boolean. Only exists for global variables (variables in the `"globalVariables"` array).


### Example
```
{
    "name": "my variable", 
    "currentValue": "5", 
    "isCloudVariable": False,
}
```

## What a List Definition looks like
A list definition be an object with the following properties:
| **property**        | **type**                    | **description**                      
|---------------------|-----------------------------|----------------------------------
| `"name"`            | non-empty string            | The name of the list.            
| `"currentValue"`    | array of strings \| numbers | The value the list currently has.


### Example
```
{
    "name": "my list", 
    "currentValue": ["hello", 5], 
}
```
