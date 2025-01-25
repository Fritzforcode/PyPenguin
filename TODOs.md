# TODO

fix comments not work

do more scratch research

research sprite property "broadcasts"

update documentation

insure input magic numbers match (eg. block-only inputs)

add custom colors for custom block stuff

improve error handling

add testing

possibly change null to None ...

both empty script and None as input should make the input value empty

add blocks requirering their extensions

explore and possibly translate extensionData

direction into range 180 to -180

move cloud emoji validation from deoptimize/varables_lists.py into validator.py

explore other text input fields (if they require a min length of 1)

maybe remove "sampleCount"

maybe validate json files before reading them

maybe validate:
- note inputs must be `in range(0, 131)`
- extension names
- layerOrder to be at most 4 - needs research 
- asset names matching
- no duplicate custom block input names

Notes:
    Comments of list blocks who are embedded in another blocks are deleted automatically. There is no way for this to change.
    Warning about using "set [PROPERTY] of ([TARGET]) to (VALUE)" or "[PROPERTY] of ([TARGET])" blocks, because they are instable and might cause problems.
