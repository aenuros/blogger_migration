# Program to convert an xml
# file to json file

# import json module and xmltodict
# module provided by python
import json
import xmltodict
import os

# open the input xml file and read
# data in form of python dictionary
# using xmltodict module
# with open("blogml.xml") as xml_file:
	
# 	data_dict = xmltodict.parse(xml_file.read())
# 	xml_file.close()
	
# 	# generate the object using json.dumps()
# 	# corresponding to json data
	
# 	json_data = json.dumps(data_dict)
	
# 	# Write the json data to output
# 	# json file
# 	with open("data.json", "w") as json_file:
# 		json_file.write(json_data)
# 		json_file.close()

def makePosts():
	f = open('data.json', 'r')

	loadData = json.load(f)

	f.close()

	entryArray = loadData["feed"]["entry"]

	for member in entryArray:
		if member["content"]["@type"] == "html":
			if isinstance(member["category"], list):
				print(member["title"]["#text"])

				cwd = os.getcwd()
				targetPath = os.path.join(cwd, "jekyllposts")
				while not os.path.exists(targetPath):
					os.mkdir(targetPath)
				
				title = member["title"]["#text"]
				date = member["published"][0:10]

				tagList = []

				for tag in member["category"]:
					if "schema" not in tag["@term"]:
						tagList.append("\"" + tag["@term"] + "\"")

				tagString = ",".join(tagList)

				hasUrl = lambda x : x["@rel"] == "alternate"

				permalink = ""
				for x in filter(hasUrl, member["link"]):
					permalink = x["@href"]
				
				partialPermalink = permalink.split("/")[5]

				filename = date + "-" + partialPermalink

				targetFile = os.path.join(targetPath, filename)
				testFile = open(targetFile, "w")

				testFile.write("---\n")
				testFile.write("layout: post\n")
				testFile.write("tags: [" + tagString + "]\n")
				testFile.write("title: " + title + "\n")
				testFile.write("permalink: " + permalink)
				testFile.write("\n---\n")

				text = member["content"]["#text"]
				testFile.write(text)
				
				testFile.close()


makePosts()