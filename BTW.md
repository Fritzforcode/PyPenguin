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

maybe rename assets and put into folder structure
 - use url representation for file names (e.g. %20 for SPACE)

maybe remove "sampleCount"

maybe translate currentValue for cetain types

add other monitor types

direction into range 180 to -180

test variable overlapping detection

can var "currentValue" be boolean or null too?

move cloud emoji validation from deoptimize/varables_lists.py into validator.py

update documentation

maybe validate json files before reading them

research bitmapResolution further

explore other text input fields (if they require a min length of 1)

maybe hide input when in block-only mode? needs research

maybe add a standard costume when a sprite has no costumes

maybe validate:
- dataFormat
- extension names
- layerOrder to be at most 4 - needs research 
