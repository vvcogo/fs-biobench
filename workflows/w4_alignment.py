import fileinput

def name():
	return 'w4_alignment'
	
def description():
	return 'Aligns all NGS reads of an individual genome.'
	
def expected_args():
	return '<str:in_fastq> <str:out_sam>'
	
def prepare():
	return
	
def run(argv):
	print ('[INFO] Starting w4')
	if len(argv) is not 2:
		print ('[ERROR] w4 requires 2 arguments')
		print ('<in_fastq> <out_sam>')
		return 1
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
	return 0	
