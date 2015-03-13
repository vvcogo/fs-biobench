import fileinput

def name():
	return 'w5_assembly'
	
def description():
	return 'Basic workflow step for DNA assembly.'
	
def expected_args():
	return '<str:in_fastq> <str:out_fasta>'
	
def prepare():
	return
	
def run(argv):
	print ('[INFO] Starting w5')
	if len(argv) is not 2:
		print ('[ERROR] w5 requires 2 arguments')
		print ('<in_fastq> <out_fasta>')
		return 1
	aInFastq 	= str(argv[0])
	aOutput 	= str(argv[1])
	aOutputFile = open(aOutput, 'w')
	aHeader='>XXXXXXX Assembled genome in fasta format'
	aNumChars = 0
	for aLine in fileinput.input(aInFastq):
		aNumChars = aNumChars + len(aLine)
	aOutputFile.write(aHeader+'\n')
	aOutputFile.write('N'*int((aNumChars*0.0166667)))
	aOutputFile.close()
	return 0
