def parse_adjustment(data):
    return parse_adjustment_data(data['$objects'], data['$top']['root'].data)

def parse_adjustment_data(data, root_index):
    out = {}
    for idx, key in enumerate(data[root_index]['NS.keys']):
        objkey = data[key.data]
        keyval = data[root_index]['NS.objects'][idx].data
        objval = data[keyval]
        if type(objval) == dict:
            keycls = objval['$class']
            if data[keycls]['$classname'] == "NSMutableDictionary":
                objval = parse_adjustment_data(data, keyval)
        out[objkey] = objval
    return out