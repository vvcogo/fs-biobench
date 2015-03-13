# FS-Biobench: A file system benchmark from bioinformatics workflows
# Copyright (C) 2015 Vinicius Vielmo Cogo (LaSIGE, University of Lisbon)

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

### Import
import sys
import fileinput
import xml.etree.ElementTree as ET
from PIL import Image
from itertools import izip
import shutil
	
### Main
def main(argv):
	if len(argv) is 0:
		usage()
		return 1
	aWorkflow = str(argv[0]).upper()
	if 'W1' in aWorkflow:
		return w1_genotyping(argv[1:])
	elif 'W2' in aWorkflow:
		return w2_sequencing(argv[1:])
	elif 'W3' in aWorkflow:
		return w3_miabis(argv[1:])
	elif 'W4' in aWorkflow:
		return w4_alignment(argv[1:])
	elif 'W5' in aWorkflow:
		return w5_assembly(argv[1:])
	elif 'W6' in aWorkflow:
		return w6_gwas(argv[1:])
	elif 'W7' in aWorkflow:
		return w7_annotation(argv[1:])
	elif 'W8' in aWorkflow:
		return w8_methylation(argv[1:])
	else:
		print('[ERROR] The mentioned workflow '+aWorkflow+' does not exist');
		usage()
		return 1

### Usage
def usage():
	print '	usage:'
	print '		python workflows.py <the_workflow> [<arg1> <arg2> ...]'
	print '	arguments:'
	print '		the_workflow: 	workflow code to run (e.g., w1)'
	print '		arg1..N:	workflow arguments (e.g., input.fastq)'
	print '	workflows:'
	print '		w1: Data storage with a genotyping file ()'
	print '		w2: Data storage with a sequencing file ()'
	print '		w3: Data prospection with a MIABIS XML query ()'
	print '		w4: Basic workflow step for DNA alignment ()'
	print '		w5: Basic workflow step for DNA assembly ()'
	print '		w6: Complex workflow for Genome Wide Association Studies ()'
	print '		w7: Complex workflow for exome annotation ()'
	print '		w8: Complex workflow for DNA methylation ()'

### W1 - Genotyping
def w1_genotyping(argv):
	print '[INFO] Starting w1'
	if len(argv) is not 2:
		print '[ERROR] w1 requires 2 arguments';
		print '<num_variations> <out_genotyping>'
		return 1
	aNumVars	= long(argv[0]) #e.g., 23andMe genotypes 960614 human variations
	aOutput 	= str(argv[1])
	aOutputFile = open(aOutput, 'w')
	aHeader='#rsid chr pos genotype'
	aGenotypingLine='rsXXXXXXXXX XX XXXXXXXXX XX' #27 bytes per line
	aOutputFile.write(aHeader+'\n')
	for i in range(aNumVars):
		aOutputFile.write(aGenotypingLine+'\n')
	aOutputFile.close()
	return 0
	
### W1 - Sequencing
def w2_sequencing(argv):
	print '[INFO] Starting w2'
	if len(argv) is not 3:
		print '[ERROR] w2 requires 3 arguments';
		print '<num_reads> <read_size> <out_fastq>'
		return 1
	aNumReads	= long(argv[0])
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

	
### W3 - MIABIS
def w3_miabis(argv):
	print '[INFO] Starting w3'
	if len(argv) is not 3:
		print '[ERROR] w3 requires 3 arguments';
		print '<in_biobanks> <in_collections> <out_result>'
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
	
### W4 - Alignment
def w4_alignment(argv):
	print '[INFO] Starting w4'
	if len(argv) is not 2:
		print '[ERROR] w4 requires 2 arguments';
		print '<in_fastq> <out_sam>'
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

### W5 - Assembly
def w5_assembly(argv):
	print '[INFO] Starting w5'
	if len(argv) is not 2:
		print '[ERROR] w5 requires 2 arguments';
		print '<in_fastq> <out_fasta>'
		return 1
	aInFastq 	= str(argv[0])
	aOutput 	= str(argv[1])
	aOutputFile = open(aOutput, 'w')
	aHeader='>XXXXXXX Assembled genome in fasta format'
	aNumChars = 0
	for aLine in fileinput.input(aInFastq):
		aNumChars = aNumChars + len(aLine)
	aOutputFile.write(aHeader+'\n')
	aOutputFile.write('N'*long((aNumChars*0.0166667)))
	aOutputFile.close()
	return 0
	
### W6 - GWAS
def w6_gwas(argv):
	print '[INFO] Starting w6'
	if len(argv) is not 6:
		print '[ERROR] w6 requires 6 arguments';
		print '<in_genotyping_1> <in_genotyping_N> <n_individuals_vcf> <out_vcf> <out_odds> <out_plot>'
		return 1
	aInGen1 	= str(argv[0])
	aInGen2 	= str(argv[1])
	aIndVcf		= int(argv[2])
	aOutVcf 	= str(argv[3])
	aOutOdds	= str(argv[4])
	aOutPlot	= str(argv[5])
	aHeaderVcf='#CHROM POS ID REF ALT GEN1 GEN2'
	aPrefixVcf='XX XXXXXXXXX rsXXXXXXXXX X X'
	aEntryVcf='X/X'
	aHeaderOdds='#CHROM POS ID ODDS P-VALUE'
	aLineOdds='XX XXXXXXXXX rsXXXXXXXXX XXX.XXX X.XX'
	# Creating a VCF with N-1 individuals
	aOutputFile = open(aOutVcf, 'w')
	aOutputFile.write(aHeaderVcf+'\n')
	for aLine in fileinput.input(aInGen1):
		if '#' not in aLine:
			aOutputFile.write(aPrefixVcf+((' '+aEntryVcf)*aIndVcf)+'\n')
	aOutputFile.close()
	# Adding the individual number N
	aOutputFile = open(aOutVcf+'.tmp', 'w')
	aFileGen = open(aInGen2,'r')
	aFileVcf = open(aOutVcf, 'r')
	for aLineGen, aLineVcf in izip(aFileGen, aFileVcf):
		if '#' not in aLineVcf:
			aOutputFile.write(aLineVcf.replace('\n', '')+' '+aEntryVcf+'\n')
		else:
			aOutputFile.write(aLineVcf)
	aOutputFile.close()
	shutil.move(aOutVcf+'.tmp',aOutVcf)
	# Calculating odds and p-values
	aInVcf = open(aOutVcf, 'r')
	aOutputFile = open(aOutOdds, 'w')
	aOutputFile.write(aHeaderOdds+'\n')
	for aLineVcf in aInVcf:
		if '#' not in aLineVcf:
			aOutputFile.write(aLineOdds+'\n')
	# Creating the Manhattan plot
	aImage = Image.new('RGB', (300,220), 'white') #420KB
	aImage.save(aOutPlot, 'BMP', compress=False)
	return 0
	
### W7 - Annotation
def w7_annotation(argv):
	print '[INFO] Starting w7'
	if len(argv) is not 5:
		print '[ERROR] w7 requires 5 arguments';
		print '<in_fastq> <out_sam> <max_num_lines_vcf> <out_vcf> <out_annotated>'
		return 1
	# Align the fastq to a SAM file
	w4_alignment(argv[0:2])
	# Create a VCF from SAM
	aOutSam 		= str(argv[1])
	aMaxNumLinesVcf = long(argv[2]) # e.g., 5600000
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
	
### W8 - Methylation
def w8_methylation(argv):
	print '[INFO] Starting w8'
	if len(argv) is not 6:
		print '[ERROR] w8 requires 6 arguments';
		print '<in_fastq> <out_sam> <max_num_lines_bed> <out_bed> <max_num_lines_diff> <out_diff>'
		return 1
	aOutSam 	= str(argv[1])
	aMaxNumLinesBed = long(argv[2]) # e.g., 9600000 (300MB)
	aOutBed 	= str(argv[3])
	aMaxNumLinesDiff = long(argv[4]) # e.g., 18000 (1MB)
	aOutDiff 	= str(argv[5])
	# Align the fastq to a SAM file
	w4_alignment(argv[0:2])
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
	
### Begin
if __name__ == '__main__':
   sys.exit(main(sys.argv[1:]))
