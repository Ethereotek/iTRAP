itrap = op("iTRAP")
# reinit permissions dict
itrap.store('Permissions', {'keys':{},'users':{}})

# unsync files
itrap.op('iTRAP').par.file = ''
itrap.op('butils').par.file = ''
itrap.op('request_validation').par.file = ''
itrap.op('Permissions').par.file = ''
itrap.op('ttree_builder').par.file = ''
itrap.op('schemas').par.file = ''

op("iTRAP").save("Build/iTRAP.tox")