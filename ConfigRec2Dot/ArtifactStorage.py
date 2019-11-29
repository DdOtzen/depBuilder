import pickle

class ArtifactStorage ( object ):

	def Fetch( self ):
		with open( r'C:\temp\d.pkl', 'rb' ) as afile :
			arts = pickle.load( afile )
			return arts

	def Save( self, arts ):
		with open( r'C:\temp\d.pkl', 'wb' ) as afile :
			pickle.dump( arts, afile )
			
if __name__ == '__main__':
	a = { 'aa': [1,'aa', {1,2,3}]}
	print( a)
	artStore = ArtifactStorage()
	
	artStore.Save( a )
	
	b = artStore.Fetch()
	
	print( b )