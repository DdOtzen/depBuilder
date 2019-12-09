from ArtifactStorage import ArtifactStorage
from BuildElements import Artifact


def MakeCvsLattix():
	aStore = ArtifactStorage()
	artifacts = aStore.Fetch() 
	with open( fileName, 'w' ) as  csvFile :
		sourceList = set()
		for art in arts.values() :
			for dep in art.dependencies :
				if type( dep ) is not Artifact :
					sourceList.addField( dep )
		print( 'sources found', len(sourceList))
		
		colList = list( arts.values() )
		colList.extend( sourceList )
		rowList = colList.copy()
		
		print( 'elementss found', len( colList ) )
		
		
		headerLine = ' ; '
		for n in range( 1, len( colList ) + 1 ) :
			headerLine += ';{}'.format(n)
		headerLine += '\n'
		csvFile.write( headerLine )
			
		for rowCount, row in enumerate( rowList, start = 1 ) :
			if type( row ) is Artifact :
				line = 'Artefacts\\' + row.fullname
			else :
				line = row.fullname
				
			line += ';{}'.format( rowCount )

			for collum in colList :
				if row in collum.dependencies :
					line += ';1'
				else :
					line += '; '
			line += '\n'
			csvFile.write( line )

if __name__ == '__main__':
	MakeCvsLattix()
