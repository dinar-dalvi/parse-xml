#!/usr/bin/python


import sys, string, re, types
import yaml, getopt

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

    args = sys.argv[1:]
    print (len(args))
    print (args[0])

    if len(args) != 1:
       usage()
    inFileName = args[0]
    #outFileName = args[1]
    #if len(args[2] > 0 ):
    #    dockerFile = args[2]

    convertXml2Yaml(inFileName)


def convertXml2Yaml(inFileName):
    # Open XML document using minidom parser
    DOMTree = xml.dom.minidom.parse(inFileName)
    collection = DOMTree.documentElement
    if collection.hasAttribute("shelf"):
       print "Root element : %s" % collection.getAttribute("scm")

    # Get all the scm's in the collection
    scms = collection.getElementsByTagName("scm")

    branches = collection.getElementsByTagName("branches")

    builders = collection.getElementsByTagName("builders")

    # Print detail.
    for scm in scms:
       print "*****Movie*****"
       if scm.hasAttribute("class"):
          url = scm.getElementsByTagName('url')[0]
          print "URL: %s" % url.childNodes[0].data

    for branch in branches:
       print "*****branch*****"
       branch_name = branch.getElementsByTagName('name')[0]
       print "Branch: %s" % branch_name.childNodes[0].data

    for builder in builders:
        print "*****builders*****"
        command = builder.getElementsByTagName('command')[0]
        print "command: %s" % command.childNodes[0].data
        commands= command.childNodes[0].data.split('\n')
        print "command: %s" % commands[1]
        print "*****Comamnds*****"

        for x in commands:
            print "value: %s" % x


    with open(outputfile, 'a') as the_file:
           the_file.write(outStr)
       #print "Format: %s" % format.childNodes[0].data
       #rating = movie.getElementsByTagName('rating')[0]
       #print "Rating: %s" % rating.childNodes[0].data
       #d#escription = movie.getElementsByTagName('description')[0]
       #print "Description: %s" % description.childNodes[0].data

if __name__ == '__main__':
    main()
    #import pdb
    #pdb.run('main()')