import fileinput
import shutil

def name():
	return 'w6_gwas'
	
def description():
	return '\tComplex workflow for Genome Wide Association Studies.'
	
def expected_args():
	return '<str:in_genotyping_1> <str:in_genotyping_N> <i:n_individuals_vcf> <str:out_vcf> <str:out_odds> <str:out_plot>'
	
def prepare():
	return
	
def run(argv):
	print ('[INFO] Starting w6')
	if len(argv) is not 6:
		print ('[ERROR] w6 requires 6 arguments')
		print ('<in_genotyping_1> <in_genotyping_N> <n_individuals_vcf> <out_vcf> <out_odds> <out_plot>')
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
	for aLineGen, aLineVcf in zip(aFileGen, aFileVcf):
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
	aOutputFile = open(aOutPlot,'w')
	aOutputFile.write('#'*420*1024) # a file with 420KB
	aOutputFile.close()
	return 0
