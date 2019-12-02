from ArtifactStorage import ArtifactStorage

class Line( object ):
	def __init__( self, text = None ):
		self.text = text
		
	def AddField( self, fieldText ):
		if self.text is not None :
			self.text += ';'
		else :
			self.text = ''
		self.text += fieldText
		
	def AsString(self):
		return self.text

class UsedBy():

	def __init__(self, file, artefacts ):
		
		intCount = 0
		self.perArt = Line()
		self.accumulated = ''
		self.count = '0'
		for art in artefacts.values() :
			if file in art.dependencies :
				self.accumulated += '{},'.format( art.label)
				self.perArt.AddField( 'X' )
				intCount += 1
			else :
				self.perArt.AddField( ' ' )
		if self.accumulated is not '' :
			self.accumulated = self.accumulated[:-1] 
		self.count = str( intCount )

def FindSharedWith( artifacts, file ):
	usedBy = set()
	for art in artifacts.values() :
		if file in art.dependencies :
			usedBy.add(art)
	return usedBy
	
def MakeHeader( artefacts ):
	header0 = '        ;        ;      ;Used by   ;Used by'
	header1 = 'FullName;FileName;in Vob;Acumulated;count'
	for art in artefacts.values() :
		header0 += ';Used by'
		header1 += ';{}'.format( art.label )
	header = header0 + '\n' + header1
	return header
		
def MakeLine( file, artefacts ):
	line = Line( file.fullname )
	line.AddField( file.label )
	line.AddField( GetVob( file.fullname ) )
	
	usage = UsedBy( file, artefacts )
	line.AddField( usage.accumulated )
	line.AddField( usage.count )
	line.AddField( usage.perArt.AsString() )
	
	return line.AsString()
	
def GetVob( fullName ):
	return fullName.split('\\',1)[0]

def main():
	aStore = ArtifactStorage()
	
	artefacts = aStore.Fetch() 
	
	artefactInFocus = artefacts.pop(r'p400\vlt_data\moc\cc_mkii\delfino_flashapplication.hpp')
	
	print( 'Examining:', artefactInFocus.label,'\n' )
	
	with open('Report.csv', 'w') as csvFile :
		csvFile.write( MakeHeader( artefacts ) )	
		csvFile.write( '\n' )

		for depFile in artefactInFocus.dependencies :
			csvFile.write( MakeLine( depFile, artefacts ) )
			csvFile.write( '\n' )

if __name__ == '__main__':
	main()