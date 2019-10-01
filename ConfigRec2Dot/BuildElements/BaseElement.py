

class BaseElement( object ):

	isFinal = False
	
	def __init__(self, line ):
		self.fullname = self.extractName( line )
		self.key = self.fullname
		self.label = self.fullname.rsplit('\\',1)[1]
		
		self.dependencies = set()
		
	def extractName(self, line ):
		print( 'error extractName not implemented in: ', self.__class__ )
		return ''
	
	def addDependency(self, dep):
			self.dependencies.add( dep )