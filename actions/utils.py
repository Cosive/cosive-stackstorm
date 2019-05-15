from datetime import datetime
# Taken from https://github.com/yaleman/st2-whois/actions/whois_lib.py - it's good for more than whois though
def clean_list(data):
    """ filters a list for bad stackstorm items
    input: list
    returns: list
    """
    result = []
    for element in data:
        if isinstance(element, unicode) or isinstance(element, datetime):
            result.append(str(element))
        else:
            result.append(element)
    return result

def clean_dict(data):
    """ takes any dict, but typically the return value of an Action, and cleans up any data that'll make
        stackstorm have a hissy fit
        input: dict
        returns: dict
        """
    result = {}
    # go through the results and put it in a form that stackstorm can take
    for key in data.keys():
        if isinstance(data[key], datetime): # datetime is bad, m'kay
            result[key] = data[key].isoformat()
        # because sometimes, people make lists of problematic elements!
        elif isinstance(data[key], list):
            result[key] = clean_list(data[key])
        # handle nested dicts
        elif isinstance(data[key], dict):
            result[key] = clean_dict(data[key])
        # handle unicode, because python2
        elif isinstance(data[key], unicode):
            result[key] = str(data[key])
        # everything else I got was OK...
        else:
            result[key] = data[key]
    return result