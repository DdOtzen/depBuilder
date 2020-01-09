import sys
import PySimpleGUI as sg
from OutputWindow import EmbeddedOutputWindow, stdOutputWrapper

from FetchCr import FetchCrs
from ParseCRs import ParseCRs
from MakeCvsLattix import MakeCvsLattix
from MakeCvsTable import MakeCvsTable
from MakeDotFile import MakeDotFile
from Report_dsp import makeDspReport
from DDproducts import products

sg.change_look_and_feel( 'Dark2' )

# # Column 1 layout

maxKeyLength = 0
for prodKey in products.keys() :
	maxKeyLength = max( maxKeyLength, len( prodKey ) )

colum1Layout = []
for prodKey, prodVal in products.items() :
	if len( prodVal ) > 58 :
		shortVal = '...' + prodVal[-55:] 
	else :
		shortVal = prodVal
		
	colum1Layout.append( [
						   sg.Text( prodKey, justification = 'right', size = ( maxKeyLength + 1, 1 ) ),
	                       sg.InputText( shortVal, tooltip=prodVal, size = ( 60, 15 ), justification = 'left', disabled = True , font = 'Courier' )
	                     ] )

# # Column 2 layout

outTextField = EmbeddedOutputWindow( key = 'outputField', size = ( 120, 35 ), autoscroll = True )

colum2Layout = [ [ sg.Button( "Fetch CR's", key = 'fetchBtn' ), sg.Button( "Parse CR's", key = 'parseBtn' ) ],
				 [ sg.Checkbox( "Unconditional fetch", key = 'forceFetch' ) ],
				 [ sg.Text( '_' * 30 ) ],
				 [ sg.Button( 'Make CSV for Lattix', key = 'makeLattix', size = ( 23, None ) ), sg.InputText( key = 'pathLattix' , default_text = 'lattix.csv' ), sg.FileSaveAs() ],
				 [ sg.Button( 'Make simple matrix CSV', key = 'makeMatrix', size = ( 23, None ) ), sg.InputText( key = 'pathMatrix' , default_text = 'dd.csv' ), sg.FileSaveAs() ],
				 [ sg.Button( 'Make DSP report', key = 'makeReport', size = ( 23, None ) ), sg.InputText( key = 'pathRepport', default_text = 'Report.csv' ), sg.FileSaveAs() ],
				 [ sg.Button( 'Make dot file', key = 'makeDotfile', size = ( 23, None ) ), sg.InputText( key = 'pathDotfile', default_text = 'allDeps.dot' ), sg.FileSaveAs() ],
				 [ sg.Exit()],
				 [ outTextField ],
			   ]

# Create the Window
colum1 = sg.Column( colum1Layout , scrollable = True, vertical_scroll_only = True )
colum2 = sg.Column( colum2Layout )


layout = [
			[ colum1, colum2 ]
		 ]

window = sg.Window( 'Config record dep extractor', layout, resizable = True )

# Event Loop to process "events" and get the "values" of the inputs

def PassiveUpdate() :
	window.Read( timeout = 0 )

sys.stdout = stdOutputWrapper( sys.stdout, outTextField.Print, PassiveUpdate )
sys.stderr = stdOutputWrapper( sys.stderr, outTextField.PrintErr, PassiveUpdate )


def StartStdoutputCapture():
	sys.stdout.ActivateGui()
	sys.stderr.ActivateGui()


def EndStdoutputCapture():
	sys.stdout.DeactivateGui()
	sys.stderr.DeactivateGui()


while True:
	event, values = window.read()
	if event in ( None, 'Exit' ):  # if user closes window or clicks cancel
		break
	elif event == 'fetchBtn' :
		StartStdoutputCapture()
		FetchCrs( values[ 'forceFetch' ] )
		print( "Done" )
		EndStdoutputCapture()
	elif event == 'parseBtn' :
		StartStdoutputCapture()
		ParseCRs()
		print( "Done" )
		EndStdoutputCapture()
	elif event == 'makeLattix' :
		StartStdoutputCapture()
		MakeCvsLattix( values[ 'pathLattix' ] )
		print( "Done" )
		EndStdoutputCapture()
	elif event == 'makeMatrix' :
		StartStdoutputCapture()
		MakeCvsTable( values['pathMatrix'] )
		print( "Done" )
		EndStdoutputCapture()
	elif event == 'makeReport' :
		StartStdoutputCapture()
		makeDspReport( values[ 'pathRepport' ] )
		print( "Done" )
		EndStdoutputCapture()
	elif event == 'makeDotfile' :
		StartStdoutputCapture()
		MakeDotFile( values[ 'pathDotfile' ] )
		print( "Done" )
		EndStdoutputCapture()
	else :
		print( event, values )

window.close()

if __name__ == '__main__':
	pass
