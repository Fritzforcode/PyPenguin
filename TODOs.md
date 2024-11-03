# Magic Values(Input Types):
- broadcasts: 11
- text: 10 eg. say
- number: 4 eg. operator
- boolean: 2 (hidden when empty) eg. not
- look into scratch wiki "file format"

# Missing Features:
- procedures
- more block opcodes

# TODO
explore and possibly translate extensionData

add other monitor types

direction into range 180 to -180

move cloud emoji validation from deoptimize/varables_lists.py into validator.py

explore other text input fields (if they require a min length of 1)

maybe remove "sampleCount"

maybe translate currentValue for cetain types

maybe validate json files before reading them

maybe hide input when in block-only mode? needs research

maybe add a standard costume when a sprite has no costumes

maybe reseatch monitor size

maybe remove fileStem

research rotationCenter for different costume types

research monitor values being wrong

add testing

research bug: comment becomming parent of block

maybe validate:
- dataFormat
- extension names
- fileStem (no folders allowed and the file existing)
- layerOrder to be at most 4 - needs research 
- meta
