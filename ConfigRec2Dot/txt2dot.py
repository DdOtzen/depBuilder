from BuildElements import Artifact
from BuildElements import Source
from BuildElements import DerivedObject
from BuildElements import Product

# import BuildElements

targets = dict()
sources = dict()
dObjects = dict()
artifacts = dict()


def isDO( line ):
	if line[:23] == 'derived object         ':
		return True
	else:
		return False


def isNewDO( line ):
	if isViewPrivate( line ) and 'new derived object' in line:
		return True
	else:
		return False


def isVersion( line ):
	if line[:23] == 'version                ':
		return True
	else:
		return False


def isDoVersion( line ):
	if line[:23] == 'derived object version ':
		return True
	else:
		return False

		
def isViewPrivate( line ):
	if line[:23] == 'view private object    ':
		return True
	else:
		return False


def isTarget( line ):
	if line[:7] == 'Target ':
		return True
	else:
		return False


def extractTargetName( line ):
	fullName = line.split( ' ' )[1]
	return fullName


def UpdateSourceList( sourceId ):
	global sources
	if sourceId not in sources:
		sources[sourceId] = Source( sourceId )


def StartOfFile( line ):
	global state
	if isTarget( line ):
		state = ReadingTarget


def ReadingTarget( line ):
	global state
	if isTarget( line ):
		state = PopulatingTarget
	elif isVersion( line ):
		if '[in makefile]' in line:
			pass
		else:
			inLines.add( line )
	elif isDO( line ):
		if 'new derived object' in line:
			outLines.add( line )
		elif 'referenced derived object' in line:
			inLines.add( line )
		else:
			print( 'Error' )
	elif isNewDO( line ):
		outLines.add( line )
	elif isDoVersion( line ):
		if 'referenced derived object' in line:
			inLines.add( line )
		else:
			print( 'Error a DOV that was not reerenced:', line )


def PopulatingTarget( unused ):
	global state
	global inLines
	global outLines
# 	print( ' in:  ', len( inLines ) )
# 	print( ' out: ', len( outLines ) )
	
	_usedDos = set()
	_usedSources = set()
	for line in inLines:
		
		if isDO( line ):
			_do = DerivedObject( line )
			# add to global list
			if _do.key not in dObjects:
				dObjects[ _do.key ] = _do
			else:
				_do = dObjects[ _do.key ]
			# add to my local list
			_usedDos.add( _do )
		
		elif isVersion( line ):
			_ver = Source( line )
			# add to Global list
			if _ver.key not in sources:
				sources[ _ver.key ] = _ver
			else:
				_ver = sources[ _ver.key ]
			_usedSources.add( _ver )
		
		elif isDoVersion( line ):
			_dov = Artifact( line )
			if _dov.key not in artifacts:
				artifacts[ _dov.key ] = _dov
			else:
				_dov = artifacts[ _dov.key ]
			_usedDos.add( _dov )
		
		else:
			print( 'unhandled Line:', line )
	
	for line in outLines:
		if isDO( line ) or isNewDO( line ):
			_do = DerivedObject( line )
			if _do.key not in dObjects:
				dObjects[ _do.key ] = _do
			else:
				_do = dObjects[ _do.key ]
		else:
			print( 'Error not a DO: "{}"'.format( line ) )
			break
		for _source in _usedSources:
			_do.addDependency( _source )
		for _doIn in _usedDos:
			_do.addDependency( _doIn )

	state = ReadingTarget
	inLines = set()
	outLines = set()


state = StartOfFile
inLines = set()
outLines = set()
	
	
def parse():
	with open( 't2.cr', 'r' ) as  listFile:
		for line in listFile:
			state( line.strip() )
				

if __name__ == '__main__':
	parse()
	print( "found", len( targets ), "targets" )
	print( "found", len( sources ), "sources" )
	print( "found", len( dObjects ), "DO's" )
	print( "found", len( artifacts ), "artifacts" )
# 	for do in dObjects.values():
# 		print( do.key )
	print( [ d.key for d in dObjects['p400\\product\\FC30X\\generated\\DictionaryGerman.o'].dependencies ] )
