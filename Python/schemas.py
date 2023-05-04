import copy
components = {

    'path': {
        'path': {
            'type': str
        }
    },
    'path&id': {
        'path': {
            'type': str
        },
        'id': {
            'type': int
        }
    },
    'tag_params':{
        'path': {
            'type': str
        },
        'id': {
            'type': int
        },
        'tags':{
            'type':list
		}       
	}
}
schemas = {
    'put_app_power': {
        'parameters': {
            'state': {
                'type': (bool, int)
            }
        },
        'required': ['state']
    },
    'put_app_play': {
        'parameters': {
            'play': {
                'type': (bool, int)
            }
        },
        'required': ['play']
    },
    'put_project_cookRate': {
        'parameters': {
            'rate': {
                'type': (int, float)
            }
        },
        'required': ['rate']
    },
    'put_project_realTime': {
        'parameters': {
            'realTime': {
                'type': (int, bool)
            }
        },
        'required': ['realTime']
    },
    'put_project_performOnStart': {
        'parameters': {
            'performOnStart': {
                'type': (int, bool)
            }
        },
        'required': ['performOnStart']
    },
    'post_project_load': {
        'parameters': components['path'],
        'required': []
    },
    'post_project_save': {
        'parameters': components['path'],
        'required': []
    },
    'put_ui_masterVolume': {
        'parameters': {
            'volume': {
                'type': (int, float)
            }
        },
        'required': ['volume']
    },
    'get_op': {
        'parameters': components['path&id'],
        'required': [['path', 'id']]
    },
    'post_op': {
        'parameters': {
            'name': {
                'type': str
            },
            'type': {
                'type': str
            },
            'parent': {
                'type': str
            }
        },
        'required': [
            'name',
            'type',
            'parent'
        ]
    },
    'delete_op': {
        'parameters': components['path&id'],
        'required': [['path', 'id']]
    },
    'get_op_id': {
        'parameters': components['path'],
        'required': ['path']
    },
    'get_op_name': {
        'parameters': components['path&id'],
        'required': [['path', 'id']]
    },
    'put_op_name': {
        'parameters': {
            'path': {
                'type': str
            },
            'id': {
                'type': int
            },
            'name': {
                'type': str
            }
        },
        'required': [
            'name',
            ['path', 'id']
        ]
    },
    'get_op_storage': {
        'parameters': components['path&id'],
        'required': [['path', 'id']]
    },
    'get_op_tags': {
        'parameters': components['path&id'],
        'required':[['path', 'id']]
    },
    'post_op_tags':{
        'parameters':components['tag_params'],
        'required':[
            ['path', 'id'],
            'tags'
		]
	},
    'delete_op_tags':{
        'parameters':components['tag_params'],
        'required':[
            ['path', 'id'],
            'tags'
		]
	},
    'get_op_par':{
        'parameters':{
            'path':{
                'type':str
            },
            'id':{
                'type':str
            },
            'name':{
                'type':str
            }
        },
        'required':[
            ['path','id'],
            'name'
        ]
    },
    'put_op_par':{
        'parameters':{
            'path':{
                'type':str
            },
            'id':{
                'type':str
            },
            'par':{
                'type':str
            },
            'val':{
                'type':str
            }
        },
        'required':[
            ['path', 'id'],
            'par',
            'val'
        ]
    },
    'get_named_op':{
        'parameters':{
            'name':{
                'type':str
            }
        },
        'required':['name']
    },
    'get_named_op_attribute':{
        'parameters':{
            'name':{
                'type':str
            },
            'attribute':{
                'type':str
            }
        },
        'required':['name', 'attribute']
    },
    'get_named_op_par':{
        'parameters':{
            'name':{
                'type':str
            },
            'par':{
                'type':str
            }
        },
        'required':['name', 'par']
    },
    'put_named_op_attribute':{
        'parameters':{
            'name':{
                'type':str
            },
            'attribute':{
                'type':str
            },
            'value':{
                'type':str
            }
        },
        'required':['name', 'attribute', 'value']
    }
}
