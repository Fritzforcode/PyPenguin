import json, pprint

def kv(obj): return zip(obj.keys(), obj.values())

def make_list_tuple_set(cls, data):
    return {
        "__class__"      : cls,
        #"__module__"     : "builtins",
        "__data__"       : data,  # Convert to list for JSON compatibility,
        #"is_custom_class": False,
    }

def make_dict(cls, keys, values):
    return {
        "__class__"      : cls,
        #"__module__"     : "builtins",
        "__data__keys"   : keys, #split up because keys can be any type
        "__data__values" : values,
        #"is_custom_class": False,
    }

def serialize(obj):
    """Serialize any Python object to JSON."""
    # Handle custom objects with __dict__
    if hasattr(obj, "__dict__"):
        data = {}
        for key, value in kv(obj.__dict__):
            data[key] = serialize(value)
        return {
            "__class__"      : obj.__class__.__name__,
            #"__module__"     : obj.__module__,
            "__data__"       : data,
            #"is_custom_class": True,
        }

    # Handle simple data types
    if isinstance(obj, (str, int, float, bool, type(None))):
        return {
            "__class__"      : obj.__class__.__name__,
            #"__module__"     : "builtins",
            "__data__"       : obj,
            #"is_custom_class": False,
        }

    # Handle tuples, sets, listss
    if isinstance(obj, (tuple, set, list)):
        data = []
        for item in obj:
            data.append(serialize(item))
        return make_list_tuple_set(obj.__class__.__name__, data)
    if isinstance(obj, dict):
        data_keys   = []
        data_values = []
        for key, value in kv(obj):
            data_keys  .append(serialize(key  ))
            data_values.append(serialize(value))
        return make_dict(obj.__class__.__name__, data_keys, data_values)

    # Raise error for unsupported types
    raise TypeError(f"Object of type {type(obj)} is not JSON serializable")
