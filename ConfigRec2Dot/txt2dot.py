from BuildElements import Artifact
from BuildElements import Source, sQuiet
from BuildElements import DerivedObject, quiet
from BuildElements import BeDict

import ClearCaseCr as cr
import sys



sources = BeDict()
dObjects = BeDict()
artifacts = BeDict()




def StartOfFile( line ):
	global state
	if cr.isTarget( line ):
		state = ReadingFirstTarget


def ReadingFirstTarget( line ):
	if cr.isNewDO( line ):
		art = Artifact( line )
		if art.key not in artifacts:
			artifacts[ art.key ] = art
		else:
			print( 'Primary Artifact repeated' )
	ReadingTarget( line )

				
def ReadingTarget( line ):
	global state
	if cr.isTarget( line ):
		state = PopulatingTarget
	elif cr.isVersion( line ):
		if '[in makefile]' in line:
			pass
		else:
			inLines.add( line )
	elif cr.isDO( line ):
		if 'new derived object' in line:
			outLines.add( line )
		elif 'referenced derived object' in line:
			inLines.add( line )
		else:
			print( 'Error' )
	elif cr.isNewDO( line ):
		outLines.add( line )
	elif cr.isDoVersion( line ):
		if 'referenced derived object' in line:
			inLines.add( line )
		else:
			print( 'Error a DOV that was not reerenced:', line )


def PopulatingTarget( unused ):
	global state
	global inLines
	global outLines
	
	usedDos = set()
	usedSources = set()
	for line in inLines:
		
		if cr.isDO( line ):
			do = dObjects.Listify( DerivedObject( line ) )
			usedDos.add( do )
		
		elif cr.isVersion( line ):
			ver = sources.Listify( Source( line ) )
			usedSources.add( ver )
		
		elif cr.isDoVersion( line ):
			dov = artifacts.Listify( Artifact( line ) )
			usedDos.add( dov )
		
		else:
			print( 'unhandled Line:', line )
	
	for line in outLines:
		if cr.isNewDO( line ):
			newDo = dObjects.Listify( DerivedObject( line ) )
		else:
			print( 'Error not a DO: "{}"'.format( line ) )
			break
		for source in usedSources:
			newDo.addDependency( source )
		for usedDo in usedDos:
			newDo.addDependency( usedDo )

	state = ReadingTarget
	inLines = set()
	outLines = set()


state = StartOfFile
inLines = set()
outLines = set()
	
	
def Parse():
	with open( 't2.cr', 'r' ) as  listFile:
		for line in listFile:
			state( line.strip() )


def LinkArtifacts():
	for art in artifacts.values():
		art.importDo( dObjects.pop( art.key ) )
				

def CountReferences( aDict ):
	c = dict()
	for o in aDict.values():
		r = sys.getrefcount( o )
		if r in c:
			c[r] += 1
		else:
			c[r] = 1
	for k in sorted( c.keys() ):
		print( "{}: {}".format( k, c[k] ) )


if __name__ == '__main__':
	Parse()
# 	print( "found", len( sources ), "sources" )
# 	print( "found", len( dObjects ), "DO's" )
# 	print( "found", len( artifacts ), "artifacts" )
	for key in artifacts.keys():
		print( key )
		if key in dObjects.keys():
			print( '\tFound' )
	LinkArtifacts()
# 	print( "found", len( sources ), "sources" )
# 	print( "found", len( dObjects ), "DO's" )
# 	print( "found", len( artifacts ), "artifacts" )

#	CountReferences( dObjects )
	del( dObjects )
# 	quiet.do = False
	labels = set()
	labelCount = 0
	for bElens in [ artifacts, sources ]:
		for bElen in bElens.values():
			if bElen.label in labels:
# 				print( 'Match found:', bElen.label )
				labelCount += 1
			else:
				labels.add( bElen.label )
	print( 'searched over {} labels. Found {} repeats'.format( len( labels ), labelCount ) )

	sQuiet.do = False
	del( sources )

	for artifact in artifacts.values():
		print( artifact.key )
		print( 'before:', len( artifact.dependencies ) )
		deps = artifact.getDeepDeps()
		with open( artifact.label + '.dep', 'w' ) as  depFile :
			print( artifact.fullname, file = depFile )
			for dep in artifact.dependencies :
				print( dep.fullname, file = depFile )
		print( 'returned:', len( deps ) )
		print( 'after:', len( artifact.dependencies ) )
	
	quiet.do = True
	sQuiet.do = True
	print( 'exit' )

