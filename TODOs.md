# TODO

[WORKING ON] update documentation

add testing

add option value translation

possibly change null to None ...

both empty script and None as input should make the input value empty

add blocks requirering their extensions

explore and possibly translate extensionData

direction into range 180 to -180

move cloud emoji validation from deoptimize/varables_lists.py into validator.py

explore other text input fields (if they require a min length of 1)

maybe remove "sampleCount"

maybe translate currentValue for certain types

maybe validate json files before reading them

maybe validate:
- extension names
- layerOrder to be at most 4 - needs research 
- asset names matching
- block types being in the correct place in script or input
- no duplicate custom block input names
- custom opcodes

Notes:
    Comments of list blocks who are embedded in another blocks are deleted automatically. There is no way for this to change.
    Warning about using "set [PROPERTY] of ([TARGET]) to (VALUE)" or "[PROPERTY] of ([TARGET])" blocks, because they are instable and might cause problems.
