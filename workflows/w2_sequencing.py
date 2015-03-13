def name():
	return 'w2_sequencing'
	
def description():
	return 'Write an NGS sequencing file containing the DNA reads of an individual.'
	
def expected_args():
	return '<l:num_reads> <i:read_size> <str:out_fastq>'
	
def prepare():
	return
	
def run(argv):
	print ('[INFO] Starting w2')
	if len(argv) is not 3:
		print ('[ERROR] w2 requires 3 arguments')
		print ('<num_reads> <read_size> <out_fastq>')
		return 1
	aNumReads	= int(argv[0])
	aReadSize	= int(argv[1]) 
	aOutput 	= str(argv[2])
	aOutputFile = open(aOutput, 'w')
	for i in range(aNumReads):
		#each read contains (aReadSize * 2 + 20) bytes (e.g., 220 for aReadSize=100)
		aOutputFile.write('@XXXXXXXXXXX.XXXX/X\n')
		aOutputFile.write((aReadSize*'N')+'\n')
		aOutputFile.write('+\n')
		aOutputFile.write((aReadSize*'Q')+'\n')
	aOutputFile.close()	
	return 0
