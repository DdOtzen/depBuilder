import os

from products import products

if __name__ == '__main__':
	crDIr = 'crs'
	if not os.path.isdir( crDIr ) :
		os.mkdir( crDIr )
	os.system( 'cleartool mount \\P422_MCO302' )
	os.system( 'cleartool mount \\p400' )
	os.system( 'cleartool mount \\p400_dsp' )
	os.system( 'cleartool mount \\tools' )
	os.system( 'cleartool mount \\pl_models' )
	os.system( 'cleartool mount \\ecos' )
	os.system( 'cleartool mount \\export' )
	os.system( 'cleartool mount \\pfpd' )
	os.system( 'cleartool mount \\pnio_dk' )
	os.system( 'cleartool mount \\bacnetStack' )
	
	for p in products :
		doPathName = os.path.join('M:\mah__main', products[ p ] )
		crPathName = os.path.join( crDIr, p + '.cr' ) 
		cmd = 'cleartool catcr -recurse -ci -type fl -long ' + doPathName + ' > '  + crPathName
		print( cmd )
		os.system( cmd )
	
		