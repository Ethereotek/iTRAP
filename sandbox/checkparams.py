

putOpPar = {
    'op-path': '/project1',
    'par-name':True,
    'par-val':'test'
}
schema = {
        'parameters':{
            'op-path':{
                'type':str
            },
            'op-id':{
                'type':str
            },
            'par-name':{
                'type':str
            },
            'par-val':{
                'type':'any'
            }
        },
        'required':[
            ('op-path', 'op-id'),
            'par-name',
            'par-val'
        ]
    }


def checkParameters(pars: dict, schema):
    included_pars = pars.keys()
    expected_pars = schema['parameters']
    required_pars = schema['required']

    hasRequired = True
    validType = False

    for p in required_pars:

        if type(p) == str:
            # `p in included_pars` will return boolean True or False
            # if not included, hasRequired permanently False
            hasRequired = hasRequired and (p in included_pars)
        if type(p) == tuple:
            hasTupleOption = False
            for _p in p:
                hasTupleOption = hasTupleOption or (_p in included_pars)
            hasRequired = hasRequired and hasTupleOption
            # check if one of these is present
            pass
    if hasRequired:
        validType = True
        for par, val in pars.items():
            expected_type = expected_pars[par]['type']
            if type(expected_type) == tuple:
                validType = False
                for _type in expected_type:
                    validType = validType or (_type == type(val))
            elif expected_type == 'any':
                pass
            else:
                validType = validType and (expected_type == type(val))

    return hasRequired, validType


params_present = checkParameters(putOpPar, schema)
print(params_present)
