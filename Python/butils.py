
def jsonifyOp(operator):
	jOp = {
		'id':operator.id,
		'name':operator.name,
		'path':operator.path,
		'time':{
			'path':operator.time.path,
			'id':operator.time.id
			},
		'parent':{
			'path':operator.parent().path,
			'id':operator.parent().id
			},
		'type':{
			'label':operator.label,
			'family':operator.family,
			'type':operator.type,
			'subType':operator.subType,
			'OPType':operator.OPType
		}
	}
	return jOp

def jsonifyTableRow(table, row=0, numCols=1):
	for col in range(numCols):
		pass

def mapOperators():

	operator_id_map = {}
	for row in op("map_operator_ids/operator_id_map").rows():
		path = row[0].val
		operator = op(path)

		_id = operator.id
		name = operator.name
		row[1].val = _id

		_map = {
			'path': path,
			'id': _id
		}
		operator_id_map[name] = _map

	return operator_id_map
