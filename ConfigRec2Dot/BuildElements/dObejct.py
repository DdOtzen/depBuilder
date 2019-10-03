
from BuildElements.BaseElement import BaseElement 

# Need to wrap in class to avoid reference directly to bool. As then I cannot change the VALUE of quiet.

class Q:
	do = True
	
quiet = Q()

class DerivedObject( BaseElement ):

	def extractName( self, line ):
		fullName = line[24:].split( ' ', 1 )[0]
		if '@' in fullName:
			fullName = fullName.split('@')[0]
		return fullName

	def __del__(self):
		if not quiet.do:
			print( 'dying', self.key )
