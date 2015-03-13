def name():
	return 'w1_genotyping'
	
def description():
	return 'Write a genotyping file containing the genomic variations of an individual.'
	
def expected_args():
	return '<l:num_variations> <str:out_genotyping>'
	
def prepare():
	return
	
def run(argv):
	print ('[INFO] Starting w1')
	if len(argv) is not 2:
		print ('[ERROR] w1 requires 2 arguments')
		print ('<num_variations> <out_genotyping>')
		return 1
	aNumVars	= int(argv[0]) #e.g., 23andMe genotypes 960614 human variations
	aOutput 	= str(argv[1])
	aOutputFile = open(aOutput, 'w')
	aHeader='#rsid chr pos genotype'
	aGenotypingLine='rsXXXXXXXXX XX XXXXXXXXX XX' #27 bytes per line
	aOutputFile.write(aHeader+'\n')
	for i in range(aNumVars):
		aOutputFile.write(aGenotypingLine+'\n')
	aOutputFile.close()
	return 0
