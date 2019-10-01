import os, sys


def GetLatestBin( topDir ):
    
    #path = 'M:\mao__main_latest\export\p400\MCA104'
        
    files = []        
    # r=root, d=directories, f = files        
    for r, _, f in os.walk( topDir ):        for file in f:            if '.bin' in file:                files.append(os.path.join(r, file))        
    latest_file = max( files, key=os.path.getctime )
    print( "Latest: ", latest_file )
if __name__ == '__main__':
    GetLatestBin( sys.argv[1] )
