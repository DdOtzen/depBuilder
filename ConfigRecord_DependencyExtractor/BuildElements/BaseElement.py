

class BaseElement( object ):

	isFinal = False
	
	def __init__(self, line ):
		self.fullname = self.extractName( line )
		self.key = self.fullname.lower()
		self.label = self.fullname.rsplit('\\',1)[1]
		
		self.dependencies = set()
		
	def extractName(self, line ):
		print( 'error extractName not implemented in: ', self.__class__ )
		return ''
	
	def addDependency(self, dep):
			self.dependencies.addField( dep )
			
	def getDeepDeps( self ):
		diveList = []
		for dep in self.dependencies:
			if not dep.isFinal:
				diveList.append( dep )
		for dep in diveList:
			self.dependencies.remove( dep )
			self.dependencies.update( dep.getDeepDeps() )
		return self.dependencies