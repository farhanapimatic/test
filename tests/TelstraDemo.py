import subprocess
import sys 
import os
from subprocess import Popen, PIPE
import json
def main(argv):
	returnVal={}
	if(len(argv)<2):
		print "Please provide all arguments"
		return 
	file=str(argv[0])
	message=str(argv[1])
	filePath= (os.path.abspath(file))
	response = "";
	workingDirectory=os.path.dirname(filePath)
	print(workingDirectory)
	if not os.path.isfile(filePath):
		return "Wrong Path Given. File Does not exist" 

	p = Popen(["git","stage", "*.*"],cwd=workingDirectory, stdin=PIPE, stdout=PIPE, stderr=PIPE)
	output, err = p.communicate(b"input data that is passed to subprocess' stdin")
	rc = p.returncode
	if(rc!=0):
		if not err:
			err=output
		result={}
		result["success"]="false"
		result["error"]=err
		returnVal["git"]=result
	else:
		p = Popen(["git","commit", "-am",message],cwd=workingDirectory, stdin=PIPE, stdout=PIPE, stderr=PIPE)
		output, err = p.communicate(b"input data that is passed to subprocess' stdin")
		rc = p.returncode
		if(rc!=0):
			if not err:
				err=output
			result={}
			result["success"]="false"
			result["error"]=err
			returnVal["git"]=result
		else:
			p = Popen(["git","push","origin","master"],cwd=workingDirectory, stdin=PIPE, stdout=PIPE, stderr=PIPE)
			output, err = p.communicate(b"input data that is passed to subprocess' stdin")
			rc = p.returncode
			if(rc!=0):
				if not err:
					err=output
				result={}
				print ("Output: "+output)
				result["success"]="false"
				result["error"]=err
				returnVal["git"]=result
			else:
				result={}
				result["success"]="true"
				result["error"]="null"
				returnVal["git"]=result


		


	p = Popen(["curl","-s", "-X", "POST", "https://packagedeployment.westus2.cloudapp.azure.com/api/deploy", "-F", "email=developer@apimatic.io", "-F", "username=apimaticdev", "-F", "password=apimaticPassword!" ,"-F", "apiDescription=@"+filePath,"-F", "language=node"], stdin=PIPE, stdout=PIPE, stderr=PIPE)
	output, err = p.communicate(b"input data that is passed to subprocess' stdin")
	rc = p.returncode
	if(rc==0):
		result={}
		outputJson = json.loads(output)
		result["success"]=outputJson["success"]
		result["error"]=outputJson["error"]
		returnVal["node"]=result
	else:
		result={}
		result["success"]="false"
		result["error"]="Error on API Call"
		returnVal["node"]=result

	p = Popen(["curl","-s", "-X", "POST", "https://packagedeployment.westus2.cloudapp.azure.com/api/deploy", "-F", "email=developer@apimatic.io", "-F", "username=apimaticdev", "-F", "password=apimaticPassword!" ,"-F", "apiDescription=@"+filePath,"-F", "language=ruby"], stdin=PIPE, stdout=PIPE, stderr=PIPE)
	output, err = p.communicate(b"input data that is passed to subprocess' stdin")
	rc = p.returncode
	if(rc==0):
		result={}
		outputJson = json.loads(output)
		result["success"]=outputJson["success"]
		result["error"]=outputJson["error"]
		returnVal["ruby"]=result
	else:
		result={}
		result["success"]="false"
		result["error"]="Error on API Call"
		returnVal["ruby"]=result

	print (json.dumps(returnVal))


if __name__ == "__main__":
	(main(sys.argv[1:]))