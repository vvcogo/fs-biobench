import xml.etree.ElementTree as ET

def name():
	return 'w3_miabis'
	
def description():
	return 'Data prospection with a MIABIS XML query.'
	
def expected_args():
	return '<l:num_variations> <str:out_genotyping>'
	
def prepare():
	return
	
def run(argv):
	print ('[INFO] Starting w3')
	if len(argv) is not 3:
		print ('[ERROR] w3 requires 3 arguments')
		print ('<in_biobanks> <in_collections> <out_result>')
		return 1
	aBiobanks 		= str(argv[0]) 
	aCollections 	= str(argv[1]) 
	aOutput			= str(argv[2])
	aOutputFile 	= open(aOutput, 'w')
	# Searching collections by disease
	aNumNodes = 0
	aXml = ET.parse(aCollections)
	aRoot = aXml.getroot()
	for aChild in aRoot:
		aNumNodes = aNumNodes + 1
		aDisease = aChild.find('disease').text
		if aNumNodes%100 is 0:
			aUrl = aChild.find('url').text
			aOutputFile.write(aUrl+'\n')
	# Searching biobanks by country
	aNumNodes = 0
	aXml = ET.parse(aBiobanks)
	aRoot = aXml.getroot()
	for aChild in aRoot:
		aNumNodes = aNumNodes + 1
		aCountry = aChild.find('country').text
	aOutputFile.close()
	return 0
