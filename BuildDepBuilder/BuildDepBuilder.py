import os
from extractBins import GetLatestBin
from datetime import datetime, timezone
LOCAL_TIMEZONE = datetime.now(timezone.utc).astimezone().tzinfo

options = [ 'MCA101',
			 'MCA104',
			 'MCA105',
			 'MCA107',
			 'MCA109',
			 'MCA114',
			 'MCA117',
			 'MCA120',
			 'MCA121',
			 'MCA122',
			 'MCA123',
			 'MCA124',
			 'MCA125',
			 'MCA194',
			 'MCB101',
			 'MCB102',
			 'MCB103',
			 'MCB105',
			 'MCB109',
			 'MCB113',
			 'MCB114',
			 'MCB115',
			 'MCB116',
			 'MCB15X_CORTEX',
			 'MCB15X_NIOS',
			 'MCAB301',
			 'MCAB301_OEMLIBS',
			 'MCO005',
			 'MCO101',
			 'MCO102',
			 'MCO104',
			 'MCAB301',
			 'MCO301',
			 'MCO302',
			 'MCO305',
			 'MCO350',
			 'MCO351',
			 'ACTIVEINRUSHHP_TM',
			 'FAN_POWERCARD',
			 'FAN_POWERCARD_TM',
			 'POWERCARDHP',
			 'POWERCARDHP_TM',
			 'POWERSTACKHP',
			 'POWERSTACKHP_BL  ',
			 'AAF005' ]

drives = [ 	'AAF005',
			'AF600',
			'AF650',
			'CDS303',
			'CUE202',
			'CUE203',
			'FC102_CC_MKII',
			'FC103_CC_MKII',
			'FC202_SAS',
			'FC202_CC_MKII',
			'FC301_CC_MKII',
			'FC301_VES',
			'FC302_AFE',
			'FC302_CC_MKII',
			'FC302_CRP',
			'FC302_IMC_CC_MKII',
			'FC302_KAB',
			'FC302_LMW_CC_MKII',
			'FC361_CC_MKII',
			'IPC102',
			'KSB202_CC_MKII',
			'LB302',
			'LD302',
			'SC001_CC_MKII',
			'TR200',
			'TRV200',
			'FC101_VLTSIM',
			'FC102_VLTSIM',
			'FC202_VLTSIM',
			'FC302_VLTSIM',
			'FC_LCPSIM',
 ]

products = drives + options

#from txt2dot import *

if __name__ == '__main__':
	
	baseDir = r'M:\mah__main\export\p400'
	bins = list()
	timeNow  = datetime.now( LOCAL_TIMEZONE )

	for prod in drives :
		binFile = GetLatestBin( baseDir +'\\' + prod )
		if binFile != '' :
			fileTime = datetime.fromtimestamp( os.path.getctime( binFile ), LOCAL_TIMEZONE )
			age = timeNow - fileTime

			print( '{};{};{:.2f} years old'.format( prod, binFile, age.days / 365 ) )
		else :
			print( '{};N/A;-1'.format( prod ) )
		bins.append( binFile )
	