'''
Created on 24. sep. 2019

@author: u246135
'''
from BuildElements.dObejct import DerivedObject 

class Artifact( DerivedObject ):

	isFinal = True
	
	def importDo(self, doObject ):
		self.dependencies.update( doObject.dependencies )
		
	def extractName( self, line ):
		fullName = super().extractName( line )
		return fullName


