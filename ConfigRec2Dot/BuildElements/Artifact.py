'''
Created on 24. sep. 2019

@author: u246135
'''
from BuildElements.dObejct import DerivedObject 

class Artifact( DerivedObject ):

	isFinal = True
	ManualOverRides = { r'export\p400\TESTMON_CC_MKII\TESTMON_CC_MKII_2_05_NEW_FLASH_RC1_00\TESTMON_CC_MKII_2_05.s1' : r'p400\product\testmonitor\controlcard\cc_mkII\build\testmonitor_cc_mkII.s1' }
	
	def importDo(self, doObject ):
		self.dependencies = doObject.dependencies
		
	def extractName( self, line ):
		fullName = super().extractName( line )
		fullName = self.ManualNameConversion( fullName )
		return fullName

	# Aparently some files in export was renamed manually, so need to compensate here.
	def ManualNameConversion( self, name ):
		for keyName in self.ManualOverRides.keys():
			if name == keyName:
				name = self.ManualOverRides[keyName]
		return name 

class Artifacts( object ):
	
	def isDoVersion( self, line ):
		if line[:23] == 'derived object version ':
			return True
		else:
			return False
