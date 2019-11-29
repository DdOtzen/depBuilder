
'''
Collection of Queries on lines in a Clear Case Config Record
'''


def isDO( line ):
	if line[:23] == 'derived object         ':
		return True
	else:
		return False


def isNewDO( line ):
	if 'new derived object' in line:
		return True
	else:
		return False


def isVersion( line ):
	if line[:23] == 'version                ':
		return True
	else:
		return False


def isDoVersion( line ):
	if line[:23] == 'derived object version ':
		return True
	else:
		return False

		
def isViewPrivate( line ):
	if line[:23] == 'view private object    ':
		return True
	else:
		return False


def isTarget( line ):
	if line[:7] == 'Target ':
		return True
	else:
		return False

def isMvfsObjects( line ):
	if line[:13] == 'MVFS objects:':
		return True
	else:
		return False

def isBuildScript( line ):
	if line[:13] == 'Build Script:':
		return True
	else:
		return False
