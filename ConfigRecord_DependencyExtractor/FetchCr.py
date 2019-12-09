import os

from products import products
from MySytemRunner import run

def NeedUpdate( source, target ):
	if os.path.exists( target ) and os.path.getctime( source ) < os.path.getctime( target ) :
		return False
	else :
		return True

def FetchCrs():
	crDIr = 'crs'
	if not os.path.isdir( crDIr ) :
		os.mkdir( crDIr )
	run( 'cleartool mount \\P422_MCO302' )
	run( 'cleartool mount \\p400' )
	run( 'cleartool mount \\p400_dsp' )
	run( 'cleartool mount \\tools' )
	run( 'cleartool mount \\pl_models' )
	run( 'cleartool mount \\ecos' )
	run( 'cleartool mount \\export' )
	run( 'cleartool mount \\pfpd' )
	run( 'cleartool mount \\pnio_dk' )
	run( 'cleartool mount \\fpga' )
	run( 'cleartool mount \\bacnetStack' )
	
	for p in products :
		doPathName = os.path.join('M:\mao__cr_extract', products[ p ] )
		crPathName = os.path.join( crDIr, p + '.cr' )
		if os.path.exists( doPathName ) :
			if NeedUpdate( doPathName, crPathName ) : 
				cmd = 'cleartool catcr -recurse -ci -type fl -long ' + doPathName + ' > '  + crPathName
				#print( cmd )
				exitCode = run( cmd )
				if exitCode > 0 :
					os.remove( crPathName )
					print( 'ERROR:', crPathName )
				else :
					print( 'created', crPathName )
			else :
				print( '\tskipping {}',format( crPathName ) )

		else :
			print( "WARNING Can't find:", doPathName )
			

if __name__ == '__main__':
	FetchCrs()