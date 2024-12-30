import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

project = {"sprites": [{"name": "Stage", "isStage": True, "scripts": [], "comments": [], "currentCostume": 0, "costumes": [], "sounds": [], "volume": 100}], "globalVariables": [], "globalLists": [], "monitors": [], "tempo": 60, "videoTransparency": 0, "videoState": "off", "textToSpeechLanguage": None, "extensionData": {}, "extensions": ["jgJSON"]}

###INSERT_START###
customScripts = [   {   '_type': 'SCRIPT',
        'position': [0, 500],
        'blocks': [   {   '_type': 'BLOCK',
                          'opcode': 'define custom block',
                          'options': {   'noScreenRefresh': ['value', True],
                                         'blockType': ['value', 'textReporter'],
                                         'customOpcode': [   'value',
                                                             'custom::set_register '
                                                             '(register) '
                                                             '(value)']}},
                      {   '_type': 'BLOCK',
                          'opcode': 'set [VARIABLE] to (VALUE)',
                          'inputs': {   'VALUE': {   'block': {   '_type': 'BLOCK',
                                                                  'opcode': 'value '
                                                                            'of '
                                                                            'text '
                                                                            '[ARGUMENT]',
                                                                  'options': {   'ARGUMENT': [   'value',
                                                                                                 'register']}}}},
                          'options': {   'VARIABLE': [   'variable',
                                                         'custom::register']}},
                      {   '_type': 'BLOCK',
                          'opcode': 'set [VARIABLE] to (VALUE)',
                          'inputs': {   'VALUE': {   'block': {   '_type': 'BLOCK',
                                                                  'opcode': 'value '
                                                                            'of '
                                                                            'text '
                                                                            '[ARGUMENT]',
                                                                  'options': {   'ARGUMENT': [   'value',
                                                                                                 'value']}}}},
                          'options': {   'VARIABLE': [   'variable',
                                                         'custom::value']}},
                      {   '_type': 'BLOCK',
                          'opcode': 'call custom block',
                          'inputs': {   'value': {   'text': 'Set the value of '
                                                             'a register.'}},
                          'options': {   'customOpcode': [   'value',
                                                             'VOID (value)']}},
                      {   '_type': 'BLOCK',
                          'opcode': 'set [VARIABLE] to (VALUE)',
                          'inputs': {   'VALUE': {   'block': {   '_type': 'Subscript',
                                                                  'value': {   '_type': 'Name',
                                                                               'id': 'register_map',
                                                                               'ctx': {   '_type': 'Load'}},
                                                                  'slice': {   '_type': 'Name',
                                                                               'id': 'register',
                                                                               'ctx': {   '_type': 'Load'}},
                                                                  'ctx': {   '_type': 'Load'}}}},
                          'options': {   'VARIABLE': [   'variable',
                                                         'custom::index']}},
                      {   '_type': 'If',
                          'test': {   '_type': 'Compare',
                                      'left': {   '_type': 'Name',
                                                  'id': 'index',
                                                  'ctx': {'_type': 'Load'}},
                                      'ops': [{'_type': 'NotEq'}],
                                      'comparators': [   {   '_type': 'Constant',
                                                             'value': 0}]},
                          'body': [   {   '_type': 'Assign',
                                          'targets': [   {   '_type': 'Subscript',
                                                             'value': {   '_type': 'Name',
                                                                          'id': 'registers',
                                                                          'ctx': {   '_type': 'Load'}},
                                                             'slice': {   '_type': 'Name',
                                                                          'id': 'index',
                                                                          'ctx': {   '_type': 'Load'}},
                                                             'ctx': {   '_type': 'Store'}}],
                                          'value': {   '_type': 'Name',
                                                       'id': 'value',
                                                       'ctx': {   '_type': 'Load'}}}],
                          'orelse': []}]}]
customVariables = ['custom::index', 'custom::register', 'custom::value']
###INSERT_END###
from headers import voidValue
scripts = customScripts + [
    voidValue,
]
variables = customVariables + ["__VOID__"]

project["sprites"][0]["scripts"] = scripts
project["globalVariables"] = [{"name":variable, "currentValue":"", "isCloudVariable":False} for variable in variables]

from pypenguin.validate import validateProject
from pypenguin.helper_functions import writeJSONFile
from pypenguin.deoptimize_and_compress import deoptimizeAndCompressProject
validateProject(projectData=project)

writeJSONFile(
    filePath = "project/project.json",
    data     = project
)

deoptimizeAndCompressProject(
    optimizedProjectDir      = "project",
    projectFilePath          = "export.pmp",
    temporaryDir             = "temporary",
    #deoptimizedDebugFilePath = "temp_wrong.json",
)
