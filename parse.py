#!/usr/bin/python


import sys, string, re, types, yaml, getopt, os, stat, errno

from xml.dom.minidom import parse
import xml.dom.minidom


USAGE_TEXT = """
Convert Jenkins config.xml to Applatix template file

Usage: python parse.py <in_file>  E.g parse.py config.xml

axscm_build.yaml /Users/dinar_dalvi/applatix_code/example-node/Dockerfile

"""

def usage():
    print USAGE_TEXT
    sys.exit(-1)

def main():
    inputfile = ''
    outputfile = 'axscm_build.yaml'
    dockerFile=''
    inDirectoryName=''

    args = sys.argv[1:]
    print (len(args))
    print (args[0])

    if len(args) != 2:
       usage()
    inFileName = args[0]
    inDirectoryName = args[1]

    if CheckIsDir(inDirectoryName):
        convertXml2Yaml(inFileName,inDirectoryName)
    else:
        print "Provided Directory does not exist"
        usage()

def CheckIsDir(directory):
  try:
    return stat.S_ISDIR(os.stat(directory).st_mode)
  except OSError, e:
    if e.errno == errno.ENOENT:
      return False
    raise

def convertXml2Yaml(inFileName,inDirectoryName):

    #Declare variables
    gitUrl = u''
    branchname = u''

    gitUrl_value = u''
    branchname_value = u''
    applatix_command = u''
    imagename = u''

    # Open XML document using minidom parser
    DOMTree = xml.dom.minidom.parse(inFileName)
    collection = DOMTree.documentElement
    if collection.hasAttribute("shelf"):
       print "Root element : %s" % collection.getAttribute("scm")

    # Get all the scm's in the collection
    scms = collection.getElementsByTagName("scm")
    branches = collection.getElementsByTagName("branches")
    builders = collection.getElementsByTagName("builders")

    # Start getting details
    for scm in scms:
       if scm.hasAttribute("class"):
          gitUrl = scm.getElementsByTagName('url')[0]
          gitUrl_value = gitUrl.childNodes[0].data

    for branch in branches:
       branchname = branch.getElementsByTagName('name')[0]
       branchname_value =branchname.childNodes[0].data


    for builder in builders:
        command = builder.getElementsByTagName('command')[0]
        commands= command.childNodes[0].data.split('\n')

    #iterate through commands array and build a complete command structure.
    for x in commands:
        print "value: %s" % x
        if (len(applatix_command) == 0):
            if (len(x) > 0):
                applatix_command =  applatix_command.strip('\t\n\r') + x + ' && '
        else:
            applatix_command = applatix_command.strip('\t\n\r') + x + ' && '

    #remove the traling &&
    applatix_command= applatix_command[:-3]

    if not os.path.exists(inDirectoryName + "/Dockerfile"):
       print "Dockerfile not present! "
    else:
         # open the Dockerfile file and read FROM as we need it for the <IMAGE>
         with open(inDirectoryName + "/Dockerfile") as f:
             for line in f:
                 if "FROM" in line:
                     print line
                     imagename =line[4:]
             f.close()

    #Make sure .applatix folder is there, if not then create one.
    if not os.path.isdir(inDirectoryName + "/.applatix"):
       os.makedirs(inDirectoryName + ".applatix")
       print ".applatix folder created"
       # Perhaps copy sample templates later.

    print "ALL NEEDED VARIABLES"
    print "gitURL command: %s" % gitUrl_value
    print "branch name : %s" % branchname_value
    print "imagename  : %s" % imagename
    print "applatix command: %s" % applatix_command

    data= u''
    with open(os.getcwd() + "/applatix_templates/axscm_docker_build_sample.yaml", 'r') as myfile:
        data=myfile.read()
        myfile.close()

    #replace needed parts.
    data = data.replace("command:", "command: " + '"' + "sh -c 'cd /src && " + applatix_command + "'" + '"')
    data = data.replace("image:", "image: " + '"' + imagename.strip() + '"')

    print "data: %s" % data

    #write the file
    with open(os.getcwd() + "/applatix_templates/axscm_docker_build.yaml", 'wb+') as newfile:
        newfile.write(data)
        newfile.close()

    print "All Done %s"

if __name__ == '__main__':
    main()
    #import pdb
    #pdb.run('main()')