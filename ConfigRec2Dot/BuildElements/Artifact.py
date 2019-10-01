'''
Created on 24. sep. 2019

@author: u246135
'''
from BuildElements.dObejct import DerivedObject 

class Artifact( DerivedObject ):

	isFinal = True
	
	

class Artifacts( object ):
	
	def isDoVersion( self, line ):
		if line[:23] == 'derived object version ':
			return True
		else:
			return False
