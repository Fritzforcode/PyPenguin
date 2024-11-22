# Events (Incomplete)
opcodes = {
    # Events: Keys
    "event_whenkeypressed": {
        "type": "hat",
        "category": "Events",
        "newOpcode": "when [KEY] key pressed",
        "inputTypes": {},
        "optionTypes": {"KEY": "key"},
        "optionTranslation": {"KEY_OPTION": "KEY"},
    },
    "event_whenbroadcastreceived": {
        "type": "hat",
        "category": "Events",
        "newOpcode": "when i receive [BROADCAST]",
        "inputTypes": {},
        "optionTypes": {"BROADCAST": "broadcast"},
        "optionTranslation": {"BROADCAST_OPTION": "BROADCAST"},
    },
    "event_broadcast": {
        "type": "instruction",
        "category": "Events",
        "newOpcode": "broadcast [BROADCAST]",
        "inputTypes": {"BROADCAST": "broadcast"},
        "inputTranslation": {"BROADCAST_INPUT": "BROADCAST"},
        "optionTypes": {},
    },
}