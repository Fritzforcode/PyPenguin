opcodes = {
    "twFiles_showPickerAs": {
        "type": "stringReporter",
        "category": "Files",
        "newOpcode": "open a file as ([MODE])",
        "inputTypes": {"MODE": "read file mode"},
        "optionTypes": {},
        "menus": [{"new": "MODE", "outer": "as", "inner": "encoding", "menuOpcode": "twFiles_menu_encoding"}],
    },
}