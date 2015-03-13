import fileinput

def name():
	return 'w7_annotation'
	
def description():
	return 'Complex workflow for exome annotation.'
	
def expected_args():
	return '<str:in_fastq> <str:out_sam> <l:max_num_lines_vcf> <str:out_vcf> <str:out_annotated>'
	
def prepare():
	return
	
def run(argv):
	print ('[INFO] Starting w7')
	if len(argv) is not 5:
		print ('[ERROR] w7 requires 5 arguments')
		print ('<in_fastq> <out_sam> <max_num_lines_vcf> <out_vcf> <out_annotated>')
		return 1
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
	# Create a VCF from SAM
	aOutSam 		= str(argv[1])
	aMaxNumLinesVcf = int(argv[2]) # e.g., 5600000
	aOutVcf 		= str(argv[3])
	aOutAnnoVcf 	= str(argv[4])
	aHeaderVcf='#CHROM POS ID REF ALT QUAL INFO GEN1'
	aLineVcf='XX XXXXXXXXX . X X . X/X'
	aOutputFile = open(aOutVcf, 'w')
	aLineNum = 0
	aOutputFile.write(aHeaderVcf)
	for aLine in fileinput.input(aOutSam):
		aLineNum = aLineNum + 1
		if aLineNum < aMaxNumLinesVcf:
			aOutputFile.write(aLineVcf+'\n')
	while aLineNum < aMaxNumLinesVcf:
		aLineNum = aLineNum + 1
		aOutputFile.write(aLineVcf+'\n')
	aOutputFile.close()
	# Annotating the VCF
	aAnnoLineVcf='XX XXXXXXXXX rsXXXXXXXXX X X XX.XX XXXXXXXXXX X/X'
	aOutputFile = open(aOutAnnoVcf, 'w')
	aLineNum = 0
	aOutputFile.write(aHeaderVcf)
	for aLine in fileinput.input(aOutVcf):
		aLineNum = aLineNum + 1
		if aLineNum < aMaxNumLinesVcf:
			aOutputFile.write(aAnnoLineVcf+'\n')
	while aLineNum < aMaxNumLinesVcf:
		aLineNum = aLineNum + 1
		aOutputFile.write(aAnnoLineVcf+'\n')
	aOutputFile.close()
	return 0
