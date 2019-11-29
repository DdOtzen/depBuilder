from ArtifactStorage import ArtifactStorage

def GetArtTypeOptions( label ):
	if label in ['dsp_data.hpp', 'AfcData.hpp', 'Delfino_FlashApplication.hpp', 'mco302_tiC28.hpp' ] :
		artType = 'dsp drive'
		color = '#00ff00'
	elif label in [ 'ParameterDllFile.cpp' ] :
		artType = 'sub paramDll'
		color = '#ffff00'
	elif label in [ 'TESTMON_AOC_1_45.s1', 'TESTMON_AOC_1_53.s1', 'TESTMON_CC_MKII_2_01.s1', 'TESTMON_CC_MKII_2_05.s1' ] :
		artType = 'sub testmon'
		color = '#009900'
	elif label in [ 'SC001_CC_MKII_1_06.bin', 'TR200_55_04.bin', 'TRV200_1_05.bin' ] :
		artType = 'drive'
		color = '#ff0000'
	elif label in [ 'AAF005_2_01.bin', 'AF600_2_40.bin', 'AF650_2_40.bin' ] :
		artType = 'drive AF'
		color = '#ff0000'
	elif label in [ 'CDS303_3_19.bin', 'FC102_CC_MKII_5_52.bin', 'FC103_CC_MKII_2_51.bin', 'FC202_CC_MKII_3_61.bin', 'FC301_CC_MKII_50_07.bin', 'FC302_AFE_47_33.bin', 'FC302_CC_MKII_8_43.bin', 'FC302_IMC_CC_MKII_48_42.bin', 'FC302_LMW_CC_MKII_42_12.bin', 'IPC102_4_48.bin', 'KSB202_CC_MKII_3_30.bin' ] :
		artType = 'drive FC'
		color = '#ff0000'
	elif label in [ 'FC361_CC_MKII_1_04.bin' ] :
		artType = 'drive FC361'
		color = '#ff0000'
	elif label in [  'FAN_POWERCARD_TM_1_22.s', 'option_tm_v1_088.s1', 'profinet_wTM.bin', 'ethernetip_wTM.bin', 'modbustcp_wTM.bin', 'plink_wTM.bin', 'ethercat_wTM.bin', 'bacnetip_wDolf_wTM.bin' ] :
		artType = 'option testmon'
		color = '#3399ff'
	elif label in [ 'aio_rtc_option.bin', 'FAN_POWERCARD_TM_1_22.s', 'FanPowerCard.bin', 'option_tm_v1_088.s1', 'PowerStackHP.bin' ] :
		artType = 'option'
		color = '#3399ff'
	elif label in [ 'akdlon.bin', 'bacnet.bin', 'bacnetip_wDolf_wTM.bin', 'canopen.bin', 'devicenet.bin', 'devicenet_converter.bin', 'emu5k.bin', 'ethercat_wTM.bin', 'ethernetip_wTM.bin', 'mca117.bin', 'modbustcp_wTM.bin', 'plink_wTM.bin', 'profibus.bin', 'profinet_wTM.bin' ] :
		artType = 'option A'
		color = '#3399ff'
	elif label in [ 'gpiooption.bin', 'sensorinputoption.bin', 'cortex_application.bin'  ] :
		artType = 'option B'
		color = '#3399ff'
	elif label in [ 'nios_application.bin' ] :
		artType = 'dsp option'
		color = '#3399ff'
	elif label in [ 'mco305.bin' ] :
		artType = 'option C'
		color = '#3399ff'
	elif label in [ 'libs_mcab301_01_00.danfoss', 'mcab301_01_00.bin', 'mco301_03_06.bin', 'mco302_03_21.bin' ] :
		artType = 'option C solo'
		color = '#3399ff'
	else :
		print( 'unidentified:', label )
		artType = ''
		color = '#000000'
	return 'color="{}" "Art type"="{}"'.format( color, artType )
	
	



def MakeDotFile( arts ):
	with open( 'allDeps.dot', 'w' ) as  depFile :
		depFile.write( 'digraph FC302 {\n' )

		elemList = set()
		for art in arts.values() :
			depFile.write('{} [label="{}" type="art" {}];\n'.format( art.key.replace( '\\', '.').replace('-','_') , art.label, GetArtTypeOptions( art.label ) ) )
			for dep in art.dependencies :
				if dep not in elemList :
					elemList.addField( dep )

		for element in elemList :
			if element not in arts.values() :
				depFile.write('{} [label="{}" type="source"];\n'.format( element.key.replace( '\\', '.').replace('-','_') , element.label) )
		
		
		for art in arts.values():
			for dep in art.dependencies :
				depLine = art.key.replace( '\\', '.').replace('-','_') + ' -> ' + dep.key.replace( '\\', '.').replace('-','_') + ';\n'
				depFile.write(depLine) 
		depFile.write( '}\n' )



if __name__ == '__main__':
	aStore = ArtifactStorage()
	artifacts = aStore.Fetch() 
	for a in artifacts.values() :
		GetArtTypeOptions( a.label )
	MakeDotFile( artifacts )
	