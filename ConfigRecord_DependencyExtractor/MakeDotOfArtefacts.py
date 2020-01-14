from BuildElements import Artifact
from ArtifactStorage import ArtifactStorage



def MakeDotFile( fileName ):
	aStore = ArtifactStorage()
	arts = aStore.Fetch() 

	with open( fileName, 'w' ) as  depFile :
		depFile.write( 'digraph FC302 {\n' )

		for art in arts.values() :
			depFile.write( '"{}" [ label="{}" type="art" ];\n'.format( art.key.replace( '\\', '_' ).replace( '-', '_' ).replace( '.', '_' ) , art.label ) )		
		
		for art in arts.values():
			for dep in art.dependencies :
				if type( dep ) is Artifact :
					depLine = '"{}" -> "{}" [color="gray"];\n'.format( dep.key.replace( '\\', '_').replace('-','_').replace( '.', '_' ), art.key.replace( '\\', '_').replace('-','_').replace( '.', '_' ) )
					depFile.write(depLine) 
		depFile.write( '}\n' )



if __name__ == '__main__':
	MakeDotFile( 'ArtefactDeps.dot' )
	