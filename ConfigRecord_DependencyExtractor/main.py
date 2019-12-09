import sys
import PySimpleGUI as sg
from products import products
from OutputWindow import stdinWrapper, stderrWrapper
from FetchCr import FetchCrs
from ParseCRs import ParseCRs 
from MakeCvsLattix import MakeCvsLattix
from MakeCvsTable import MakeCvsTable
from MakeDotFile import MakeDotFile
from Report_dsp import makeDspReport

sg.change_look_and_feel('Dark2')

## Column 1 layout

maxKeyLength = 0
for prodKey in products.keys() :
	maxKeyLength = max( maxKeyLength, len(prodKey))

colum1Layout = []
for prodKey, prodVal in products.items() :
	colum1Layout.append( [ 
						   sg.Text( prodKey, justification='right', size=( maxKeyLength +1, 1 ) ),
	                       sg.InputText(prodVal, size= (40,15),justification='right', disabled=False, background_color='white' )
	                     ] )


## Column 2 layout

colum2Layout = [ [ sg.Button( "Fetch CR's", key = 'fetchBtn' ), sg.Button( "Parse CR's", key = 'parseBtn' ) ],
				 [ sg.Checkbox( "Unconditional fetch", key = 'forceOption' ) ],
				 [ sg.Text( '_' * 30 ) ],
				 [ sg.Button( 'Make CSV for Lattix', key='makeLattix', size = ( 23, None ) ), sg.InputText( key = 'pathLattix' ), sg.FileBrowse() ],
				 [ sg.Button( 'Make simple matrix CSV', key='makeMatrix', size = ( 23, None ) ), sg.InputText( key = 'pathMatrix' ), sg.FileBrowse() ],
				 [ sg.Button( 'Make UsedBy report', key='makeReport', size = ( 23, None ) ), sg.InputText( key = 'pathRepport' ), sg.FileBrowse() ],
				 [ sg.Button( 'Make dot file', key='makeDotfile', size = ( 23, None ) ), sg.InputText( key = 'pathDotfile' ), sg.FileBrowse() ],
				 [ sg.Exit()],
				 [ sg.Multiline( key='outputField', size = ( 80, 35 ) ) ],
			   ]

# Create the Window
colum1 = sg.Column( colum1Layout , scrollable=True, vertical_scroll_only=True )
colum2 = sg.Column( colum2Layout )

layout = [
			[ colum1, colum2 ]
		 ]

window = sg.Window( 'Config record dep extractor', layout, resizable = True )


# Event Loop to process "events" and get the "values" of the inputs


sys.stdout = stdinWrapper( sys.stdout )
sys.stderr = stderrWrapper( sys.stderr )

def ActivateOutputWindow():
	sys.stdout.ActivateGui()
	sys.stderr.ActivateGui()

def DeacivateOutputWindow():
	sys.stdout.DeactivateGui()
	sys.stderr.DeactivateGui()

while True:
	event, values = window.read()
	if event in ( None, 'Exit' ):  # if user closes window or clicks cancel
		break
	elif event == 'fetchBtn' :
		ActivateOutputWindow()
		FetchCrs()
		DeacivateOutputWindow()
	elif event == 'parseBtn' :
		ActivateOutputWindow()
		ParseCRs()
		DeacivateOutputWindow()
	elif event == 'makeLattix' :
		ActivateOutputWindow()
		MakeCvsLattix()
		DeacivateOutputWindow()
	elif event == 'makeMatrix' :
		ActivateOutputWindow()
		MakeCvsTable(arts, fileName)
		DeacivateOutputWindow()
	elif event == 'makeReport' :
		ActivateOutputWindow()
		ParseCRs()
		DeacivateOutputWindow()
	elif event == 'makeDotfile' :
		ActivateOutputWindow()
		ParseCRs()
		DeacivateOutputWindow()
	else :
		print( event, values )

window.close()

if __name__ == '__main__':
	pass
