
def jsonifyOp(operator):
	jOp = {
		'id':operator.id,
		'name':operator.name,
		'path':operator.path,
		'time':operator.time,
		'parent':operator.parent,
		'type':{
			'label':operator.label,
			'family':operator.family,
			'type':operator.type,
			'subType':operator.subType,
			'OPType':operator.OPType
		}
	}

def jsonifyTableRow(table, row=0, numCols=1):
	for col in range(numCols):
		pass