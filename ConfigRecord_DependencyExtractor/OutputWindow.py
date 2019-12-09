import PySimpleGUI as sg



class stdOutputWrapper():
		
	def __init__(self, passTrough=None):
		self.passTrough = passTrough
		self.activeGui = False

	def ActivateGui(self):
		self.activeGui = True

	def DeactivateGui(self):
		self.activeGui = False

	def write(self, text ):
		if self.passTrough is not None :
			self.passTrough.write( text)
		if self.activeGui :
			self.GuiPrint( text )

	def flush(self):
		if self.passTrough is not None :
			self.passTrough.flush()
		if self.activeGui :
			outputWindow.window.Read( timeout = 0 )



class stdinWrapper( stdOutputWrapper ):
		
	def GuiPrint( self, text ):
		outputWindow.Print( text )

class stderrWrapper( stdOutputWrapper ):

	def GuiPrint( self, text ):
		outputWindow.PrintErr( text )
	
	
	
class OutputWindow():
	""" """
	debug_window = None

	def __init__( self, size = ( None, None ), location = ( None, None ), font = None, no_titlebar = False, no_button = False,
				 grab_anywhere = False, keep_on_top = True):
		"""

		:param size: Tuple[int, int] (w,h) w=characters-wide, h=rows-high
		:param location:  (Default = (None))
		:param font:  specifies the font family, size, etc
		:param no_titlebar:  (Default = False)
		:param no_button:  (Default = False)
		:param grab_anywhere: If True can grab anywhere to move the window (Default = False)
		:param location: Location on screen to display

		"""
		# Show a form that's a running counter
		self.size = size
		self.location = location
		self.font = font
		self.no_titlebar = no_titlebar
		self.no_button = no_button
		self.grab_anywhere = grab_anywhere
		self.keep_on_top = keep_on_top

		win_size = size if size != ( None, None ) else sg.DEFAULT_DEBUG_WINDOW_SIZE
		self.window = sg.Window( 'Debug Window', no_titlebar = no_titlebar, auto_size_text = True, location = location,
							 font = font or ( 'Courier New', 10 ), grab_anywhere = grab_anywhere, keep_on_top = keep_on_top )
		self.output_element = sg.Multiline( size = win_size, autoscroll = True, key = '_MULTILINE_' )


		if no_button:
			self.layout = [[self.output_element]]
		else:
			self.layout = [
				[self.output_element],
				[sg.DummyButton( 'Quit' ), sg.Stretch()]
			]
		self.window.AddRows( self.layout )
		self.window.Read( timeout = 0 )  # Show a non-blocking form, returns immediately

		self.output_element_W = self.output_element.Widget
		self.output_element_W.tag_config( "stdin", foreground = 'black' )
		self.output_element_W.tag_config( "stderr", foreground = 'red' )
		
		return

	def KeepAlive(self) :
		if self.window is None:  # if window was destroyed alread re-open it
			self.__init__( size = self.size, location = self.location, font = self.font, no_titlebar = self.no_titlebar,
						  no_button = self.no_button, grab_anywhere = self.grab_anywhere, keep_on_top = self.keep_on_top )
		
		event, values = self.window.Read( timeout = 0 )
		
		if event == 'Quit' or event is None:
			self.Close()
			self.__init__( size = self.size, location = self.location, font = self.font, no_titlebar = self.no_titlebar,
						  no_button = self.no_button, grab_anywhere = self.grab_anywhere, keep_on_top = self.keep_on_top )


	def Print( self, text ):
		"""
		:param text: text to be inserted in window
		"""
		self.KeepAlive()
		
		self.output_element_W.insert( 'end', text, "stdin" )
		self.output_element.update('', append=True ) # Needed to make autoscroll work

	def PrintErr( self, text ):
		"""
		:param text: text to be inserted in window
		"""
		self.KeepAlive()
		
		self.output_element_W.insert( 'end', text, "stderr" )
		self.output_element.update('', append=True ) # Needed to make autoscroll work


	def Close( self ):
		""" """
		self.window.Close()
		del self.window
		self.window = None


outputWindow = OutputWindow()
