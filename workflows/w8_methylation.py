import fileinput

def name():
	return 'w8_methylation'
	
def description():
	return 'Complex workflow for DNA methylation.'
	
def expected_args():
	return '<str:in_fastq> <str:out_sam> <l:max_num_lines_bed> <str:out_bed> <l:max_num_lines_diff> <str:out_diff>'
	
def prepare():
	return
	
def run(argv):
	print ('[INFO] Starting w8')
	if len(argv) is not 6:
		print ('[ERROR] w8 requires 6 arguments')
		print ('<in_fastq> <out_sam> <max_num_lines_bed> <out_bed> <max_num_lines_diff> <out_diff>')
		return 1
	aOutSam 	= str(argv[1])
	aMaxNumLinesBed = int(argv[2]) # e.g., 9600000 (300MB)
	aOutBed 	= str(argv[3])
	aMaxNumLinesDiff = int(argv[4]) # e.g., 18000 (1MB)
	aOutDiff 	= str(argv[5])
	# Align the fastq to a SAM file
	aInFastq 	= str(argv[0])
	aOutput 	= str(argv[1])
	aOutputFile = open(aOutput, 'w')
	aHeader='@HD XX:X.X XX:XXXXXXXXXX\n@SQ XX:X XX:XXXXXXXXX XX:XXXXXX XX:/XXXX/XXXXX/XXX/XXXX/XXXXXXXXXXXXX.XXXXX XX:XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX\n@RG XX:XXXXXX:X XX:XXXXXXXX XX:XXXX-XXXXXXX-XXXXXXXXX-XXXX XX:XX XX:XXXX-XX-XXXXX:XX:XX-XXXX XX:XXXXXXX XX:XXXXXX'
	aPrefix='XX:XXXXXX:X:XXX+XXXXXX XXX X XXXXXXXXX XX XXX XX XXXXXXXXX XX'
	aSuffix='XX:X:X XX:X:X XX:X:XX XX:X:XX XX:X:X XX:X:X XX:X:X XX:X:X XX:X:X XX:X:XX'
	aOutputFile.write(aHeader+'\n')
	aLineNum = 0
	for aLine in fileinput.input(aInFastq):
		if '#' not in aLine:	
			if aLineNum is 3:
				aLineNum = 0
				aLineLen = len(aLine)
				aOutputFile.write(aPrefix+' '+(aLineLen*'N')+(aLineLen*'Q')+' '+aSuffix+'\n')
			else:
				aLineNum = aLineNum + 1
		else:
			aLineNum = 0
	aOutputFile.close()
	# Create a BED from SAM
	aOutputFile = open(aOutBed, 'w')
	aMetStatusLine='chrXX XXXXXXXXX XXXXXXXXX X.XXXXXXX'
	aLineNum = 0
	for aLine in fileinput.input(aOutSam):
		aLineNum = aLineNum + 1
		if aLineNum < aMaxNumLinesBed:
			aOutputFile.write(aMetStatusLine+'\n')
	while aLineNum < aMaxNumLinesBed:
		aLineNum = aLineNum + 1
		aOutputFile.write(aMetStatusLine+'\n')
	aOutputFile.close()
	# Creating the diff methylated file	
	aDiffMetHeader='#Chromosome #CpGs #significant CpGs #DMR Start #DMR End #Direction in Y1O3 #DMR Size'
	aDiffMetLine='chrXX XX XX XXXXXXXXX XXXXXXXXX Hypermethylation XXXX'
	aOutputFile = open(aOutDiff, 'w')
	aLineNum = 0
	aOutputFile.write(aDiffMetHeader)
	for aLine in fileinput.input(aOutDiff):
		aLineNum=aLineNum+1
		if aLineNum<aMaxNumLinesDiff:
			aOutputFile.write(aDiffMetLine+'\n')
	aOutputFile.close()
	return 0
