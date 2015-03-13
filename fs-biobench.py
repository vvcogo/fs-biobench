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
import abc
import os
import sys
import configparser
import time

### Constants
DEFAULT_CFG='default.cfg'
	
### Main
def main(argv):
	sys.dont_write_bytecode = True # keep clean all folders without .pyc
	if len(argv) is 0 or '-h' in argv[0] or '--help' in argv[0]:
		return usage()
	aConfig = configparser.ConfigParser()
	aConfig.read(DEFAULT_CFG)
	if '-w' in argv[0]:
		return runWorkflow(aConfig, argv)
	elif '-e' in argv[0]:
		return runExperiment(aConfig, argv)
	elif '-l' in argv[0] or '--list' in argv[0]:
		return listWorkflows(aConfig)
	else:
		return usage()

### Run a single workflow (-w)
def runWorkflow(theConfig, theArgv):
	if len(theArgv) > 1:
		aWorkflow=loadWorkflow(theConfig,str(theArgv[1]))
		if aWorkflow is None:
			print ('[ERROR] The requested workflow does not exist.')
			return 1
		return aWorkflow.run(theArgv[2:])
	else:
		print ('[ERROR] Missing the workflow argument.')
		return 1

### Run an entire experiment (-e)
def runExperiment(theConfig, theArgv):
	if len(theArgv) > 1:
		aErrors = 0
		aExperiment = configparser.ConfigParser()
		aExperiment._interpolation = configparser.ExtendedInterpolation()
		aExperiment.read(theArgv[1])
		aExperimentName = aExperiment.get('General','name')
		aResultOutput = open(aExperiment.get('General','results_output'),'w')
		aResultOutput.write('EXPERIMENT_NAME,WORKFLOW_NAME,TIME\n')
		aPreScript = os.system(aExperiment.get('General','script_pre'))
		aWorkflows = aExperiment.items('Workflows')
		aRepetitions = int(aExperiment.get('General','repetitions'))
		for i in range(aRepetitions): # repeat the experiment aRepetitions times
			for aWorkflow in aWorkflows: 
				aInterScript = os.system(aExperiment.get('General','script_inter'))
				aLoadedWorkflow=loadWorkflow(theConfig,aWorkflow[0])
				if aLoadedWorkflow is not None:
					aWorkflowArgs=aWorkflow[1].split(' ')
					aStartTime = time.time()
					aWorkflowErrors = aLoadedWorkflow.run(aWorkflowArgs)
					aElapsedTime = time.time() - aStartTime
					aErrors = aErrors + aWorkflowErrors
					aResultOutput.write(str(aExperimentName)+','+str(aLoadedWorkflow.name())+','+str(aElapsedTime)+'\n')
				else:
					aErrors = aErrors + 1
			aPostScript = os.system(aExperiment.get('General','script_post'))
		aResultOutput.close()
		return aErrors
	else:
		print ('[ERROR] Missing the experiment argument.')
		return 1

### List all available workflows (-l or --list)
def listWorkflows(theConfig):
	aDir = theConfig.get('General', 'dir_workflows')
	aExistentWorkflows = os.listdir(aDir)
	print ('\033[1m'+'Workflow name\t\tDescription'+'\033[0m')
	print ('\033[1m'+'-------------\t\t-----------'+'\033[0m')
	for aWorkflow in sorted(aExistentWorkflows):
		aFilename = str(aDir)+'/'+str(aWorkflow)
		aModule=loadModule(aFilename)
		print (aModule.name()+'\t\t'+aModule.description())
	return 0

### Load a specific workflow
def loadWorkflow(theConfig,theWorkflowName):
	aDir = theConfig.get('General', 'dir_workflows')
	aExistentWorkflows = os.listdir(aDir)
	for aWorkflow in sorted(aExistentWorkflows):
		aFilename = str(aDir)+'/'+str(aWorkflow)
		aModule=loadModule(aFilename)
		if aModule.name() in theWorkflowName:
			return aModule
	return

### Load a Python code
def loadModule(theFilename):
	aDirectory, aModuleName = os.path.split(theFilename)
	aModuleName = os.path.splitext(aModuleName)[0]
	aPath = list(sys.path)
	sys.path.insert(0, aDirectory)
	try:
		aModule = __import__(aModuleName)
	finally:
		sys.path[:] = aPath # restore
		return aModule
	
### Print the usage (-h)	
def usage():
	print ('')
	print ('\033[1m'+'NAME'+'\033[0m')
	print ('\t\033[1m'+'fs-biobench'+'\033[0m - A file system benchmark from bioinformatics workflows.')
	print ('')
	print ('\033[1m'+'SYNOPSIS'+'\033[0m')
	print ('\tpython fs-biobench.py [-h|--help] [-l|--list] [-w <workflow_name> [<arg1> <arg2> ...]] [-e <experiment_file>]')
	print ('')
	print ('\033[1m'+'DESCRIPTION'+'\033[0m')
	print ('\tfs-biobench is a file system benchmark obtained from bioinformatics workflows.')
	print ('')
	print ('\tThe options are as follows:')
	print ('\t-h | --help\t\tPrint this help.')
	print ('\t-l | --list\t\tPresent the available workflows.')
	print ('\t-w\t\t\tRun a single workflow.')
	print ('\t-e\t\t\tRun an experiment with several workflows.')
	print ('')
	print ('\033[1m'+'EXAMPLES'+'\033[0m')
	print ('\tpython fs-biobench.py --help')
	print ('\tpython fs-biobench.py --list')
	print ('\tpython fs-biobench.py -w w1_genotyping 960614 out_w1.genotyping')
	print ('\tpython fs-biobench.py -w w2_sequencing 4715311 100 out_w2.fastq')
	print ('\tpython fs-biobench.py -w w3_miabis w3_prospection_biobanks.xml w3_prospection_collections.xml out_w3.txt')
	print ('\tpython fs-biobench.py -w w4_alignment 1g_reads.fastq out_w4.sam')
	print ('\tpython fs-biobench.py -w w5_assembly 1g_reads.fastq out_w5.fasta')
	print ('\tpython fs-biobench.py -w w6_gwas genotyping_1.txt genotyping_2.txt 100 out_w6.vcf out_w6.odds out_w6.plot')
	print ('\tpython fs-biobench.py -w w7_annotation 1g_reads.fastq out_w7.sam 5600000 out_w7.vcf out_w7_anno.vcf')
	print ('\tpython fs-biobench.py -w w8_methylation 1g_reads.fastq out_w8.sam 960000 out_w8.bed 18000 out_w8.diff')
	print ('')
	print ('\033[1m'+'SEE ALSO'+'\033[0m')
	print ('\thttps://github.com/vvcogo/fs-biobench/')
	print ('')
	return 1
	
### Begin
if __name__ == '__main__':
   sys.exit(main(sys.argv[1:]))
