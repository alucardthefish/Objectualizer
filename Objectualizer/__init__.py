

def objectualize(obj) -> str:
    """
    Return str and prints properties of a given object or class in
    a vertical way. More human readable display of an object in
    a similar way as dict/json format.
    """
    import inspect

    def _objectualize(obj, obj_list: list = []):
        output: str = ""
        if obj not in obj_list:
            if hasattr(obj, "__dict__"):
                obj_list.append(obj)
            if inspect.isclass(obj) or hasattr(obj, "__dict__") and type(obj).__name__ != "function":
                output = "{"
                obj_dict = obj.__dict__
                dict_len = len(obj_dict)
                counter = 1
                for k, v in obj_dict.items():
                    delimiter = ", " if counter < dict_len else ""
                    output += f"{k} <{type(v).__name__}> : {_objectualize(v, obj_list)}{delimiter}"
                    counter += 1
                output += "}"
            else:
                if type(obj) == list and len(obj):
                    temp = [_objectualize(element) for element in obj]
                    output += f"{temp}".replace("'", "")
                elif type(obj) == tuple:
                    temp = [_objectualize(element) for element in obj]
                    output += f"{tuple(temp)}".replace("'", "")
                elif type(obj) == dict:
                    output += "{"
                    kounter = 1
                    dict_len = len(obj)
                    for k, v in obj.items():
                        delimiter = ", " if kounter < dict_len else ""
                        output += f"{k} <{type(v).__name__}> : {_objectualize(v)}{delimiter}"
                        kounter += 1
                    output += "}"
                elif type(obj).__name__ == "function":
                    output += "Unsupported Attribute Value"
                else:
                    output += f"{obj}"
        else:
            output += "{...circular reference}"
        return output

    def revolk(obj_str):
        key_counter = 0
        tab = "\t"
        res = ""
        for char in obj_str:
            if char == "{" or char == "[" or char == "(":
                res += char
                res += "\n"
                key_counter += 1
                tabs = key_counter * tab
                res += tabs
                continue
            if char == "}" or char == "]" or char == ")":
                res += "\n"
                key_counter -= 1
                tabs = key_counter * tab
                res += tabs
                res += char
                continue
            if char == ",":
                res += char
                res += "\n"
                tabs = key_counter * tab
                res += tabs
                continue
            if char == " ":
                if res[-1:] == tab:
                    continue

            res += char
        return res
    txt_output = revolk(_objectualize(obj))
    print(txt_output)
    return txt_output
