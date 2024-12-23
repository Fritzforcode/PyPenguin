def varReporterBlock(variable):
    return {
        "opcode": "value of [VARIABLE]",
        "options": {"VARIABLE": ["variable", variable]},
    }
