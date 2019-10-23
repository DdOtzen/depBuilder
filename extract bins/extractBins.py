import os, sys

def eprint(*args, **kwargs):
	print(*args, file=sys.stderr, **kwargs)

def GetLatestBin( topDir ):
	files = []
	
# 	print( 'Searching:', topDir )		
	# r=root, d=directories, f = files
	if os.path.isdir( topDir ) :
		for r, _, f in os.walk( topDir ):
			for file in f:
				if '.bin' in file:
					files.append(os.path.join(r, file))
		binCount = len( files ) 
		if binCount <= 0 :
			eprint( 'No Bins found' )
			return ''
# 		print( '\tbins found:', binCount)
		latest_file = max( files, key=os.path.getctime )
		return latest_file
	else :
		eprint( 'Topdir Not found: ' + topDir )
		return ''

if __name__ == '__main__':
	import time
	
	start = time.perf_counter()
	print( GetLatestBin( r'M:\mah__main\export\p400\FC302_CC_MKII' ) )
	end = time.perf_counter()
	print( 'time =', end - start )
