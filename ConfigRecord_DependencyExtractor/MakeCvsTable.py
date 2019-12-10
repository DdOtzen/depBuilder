from ArtifactStorage import ArtifactStorage


def MakeCvsTable( fileName ):
	aStore = ArtifactStorage()
	arts = aStore.Fetch() 
	with open( fileName, 'w' ) as  csvFile :
		elemList = set()
		for art in arts.values() :
			for dep in art.dependencies :
				if dep not in elemList :
					elemList.add( dep )
		print( 'elems found', len(elemList))
		
		headerLine = 'Artifacts'
		for element in elemList :
			headerLine += ';' + element.fullname
		headerLine += ';Count\n'
		csvFile.write( headerLine )
		
		for art in arts.values() :
			line = art.fullname
			count = 0
			for element in elemList :
				if element in art.dependencies :
					count += 1
					line += ';X'
				else :
					line += '; '
			line += ';' + str( count ) + '\n'
			csvFile.write( line )


if __name__ == '__main__':
	MakeCvsTable('dd.csv')