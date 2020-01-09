from BuildElements import Artifact
from BuildElements import Source, sQuiet
from BuildElements import DerivedObject
from BuildElements import BeDict
from ArtifactStorage import ArtifactStorage
import logging as log

import ClearCaseCr as cr
import sys, os

sources = BeDict()
dObjects = BeDict()
artifacts = BeDict()


def StartOfFile( line ):
	global state
	if cr.isMvfsObjects( line ):
		state = ReadingFirstTarget


def ReadingFirstTarget( line ):
	if cr.isNewDO( line ):
		art = Artifact( line )
		if art.key not in artifacts:
			if art.key[-4:] == '.bin' or art.key[-4:] == '.i00' or art.key[-8:] == '.danfoss' :
				artifacts[ art.key ] = art
				log.debug( 'ArteFirst: %s', art.key )
		else:
			log.info( '\t\tPrimary Artifact repeated %s', art.label )
	ReadingTarget( line )

				
def ReadingTarget( line ):
	global state
	if cr.isBuildScript( line ):
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
			log.debug( 'Added ArteFact: %s', dov.key )

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
	
	
def Parse( crFileName, isManualWodoo=False ):
	global state
	with open( crFileName, 'r' ) as  listFile:
		if isManualWodoo :
			state = ReadingTarget
		else :
			state = StartOfFile
		
		for line in listFile:
			state( line.strip() )



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






def CountLabelRepeats() :
	"""
	Count repeated labels
	Telling how many files in different paths, share the file name
	"""
	
	labels = set()
	labelCount = 0
	for bElens in [ artifacts, sources ]:
		for bElen in bElens.values():
			if bElen.label in labels:
				print( 'Match found:', bElen.label )
				labelCount += 1
			else:
				labels.add( bElen.label )
	print( 'searched over {} labels. Found {} repeats'.format( len( labels ), labelCount ) )

def ParseCRs() :
	global dObjects
	global sources
	
	log.basicConfig( level = log.INFO )

	for f in os.listdir( 'crs' ) :
	#for f in [ 'MCB102.cr' ] :
		if f == '@manualWoodoo.cr' : continue
		
		log.info( 'parsing: %s', f)
		Parse( os.path.join( 'crs', f ) )
		Parse( os.path.join( 'crs', '@manualWoodoo.cr' ), isManualWodoo=True )
		
		log.info( '\tlooking for broken artifact objects')
		for key in artifacts.keys():
			# only empty artifacts must be tested
			if len( artifacts[key].dependencies ) == 0 :
				if key not in dObjects.keys():
					log.warning( '\t Artifact %s Not Found in derived obejcts', key )
		
		log.info( '\tlinking and colapsing dep tree %s', f )
		for artifact in artifacts.values():
			# Only empty artifacts must be populatewd.
			if  artifact.key in dObjects :
				artifact.importDo( dObjects.pop( artifact.key ) )
				artifact.getDeepDeps()

# 		if 'p400\service\moc\dsp_data.hpp' in artifacts :
# 			dsp_data =  artifacts[ 'p400\service\moc\dsp_data.hpp' ]
# 			for dep in dsp_data.dependencies :
# 				if 'debug\dsp28_flash' in dep.key :
# 					print( dep.key )  	
		
		log.info( '\tcleaning up %s', f )
		del( dObjects )
		dObjects = BeDict()

	sQuiet.do = False
	del( sources )
	sources = BeDict()

	log.info( 'Store tree to file' )
	artStore = ArtifactStorage()
	artStore.Save( artifacts )

	
# 	for artifact in artifacts.values():
# 		print( artifact.key )

	sQuiet.do = True
	print( 'exit' )

if __name__ == '__main__':
	ParseCRs()