import os

from products import products

def NeedUpdate( source, target ):
	if os.path.exists( target ) and os.path.getctime( source ) < os.path.getctime( target ) :
		return False
	else :
		return True

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
	os.system( 'cleartool mount \\fpga' )
	os.system( 'cleartool mount \\bacnetStack' )
	
	for p in products :
		doPathName = os.path.join('M:\mao__cr_extract', products[ p ] )
		crPathName = os.path.join( crDIr, p + '.cr' )
		if os.path.exists( doPathName ) :
			if NeedUpdate( doPathName, crPathName ) : 
				cmd = 'cleartool catcr -recurse -ci -type fl -long ' + doPathName + ' > '  + crPathName
				#print( cmd )
				exitCode = os.system( cmd )
				if exitCode > 0 :
					os.remove( crPathName )
					print( 'ERROR:', crPathName )
				else :
					print( 'created', crPathName )
			else :
				print( '\tskipping {}',format( crPathName ) )

		else :
			print( "WARNING Can't find:", doPathName )
			
		