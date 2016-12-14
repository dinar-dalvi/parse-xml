#!/usr/bin/python

from xml.dom.minidom import parse
import xml.dom.minidom

# Open XML document using minidom parser
DOMTree = xml.dom.minidom.parse("config.xml")
collection = DOMTree.documentElement
if collection.hasAttribute("shelf"):
   print "Root element : %s" % collection.getAttribute("scm")

# Get all the movies in the collection
movies = collection.getElementsByTagName("scm")

branches = collection.getElementsByTagName("branches")

builders = collection.getElementsByTagName("builders")

# Print detail of each movie.
for movie in movies:
   print "*****Movie*****"
   if movie.hasAttribute("class"):
      #print "Title: %s" % movie.getAttribute("title")
      url = movie.getElementsByTagName('url')[0]
      print "URL: %s" % url.childNodes[0].data

for branch in branches:
   print "*****branch*****"
   branch_name = branch.getElementsByTagName('name')[0]
   print "Branch: %s" % branch_name.childNodes[0].data
   #getAttribute("name")
   #if movie.hasAttribute("class"):
#      print "Title: %s" % movie.getAttribute("name")

for builder in builders:
    print "*****builders*****"
    command = builder.getElementsByTagName('command')[0]
    print "command: %s" % command.childNodes[0].data
    commands= command.childNodes[0].data.split('\n')
    print "command: %s" % commands[1]
    print "*****Comamnds*****"

    for x in commands:
        print "value: %s" % x

       #print "Format: %s" % format.childNodes[0].data
   #rating = movie.getElementsByTagName('rating')[0]
   #print "Rating: %s" % rating.childNodes[0].data
   #d#escription = movie.getElementsByTagName('description')[0]
   #print "Description: %s" % description.childNodes[0].data