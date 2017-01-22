#coding:utf-8


""" construct the occurrence network """

import sys
from xml.dom.minidom import parse
import xml.dom.minidom
import re
import json

def data_source(index_path, segment="abstract"):

	data = {}
	for line in open(index_path):
		path = line.strip()
		dtree = parse(path)
		collection = dtree.documentElement
		pmid = collection.getElementsByTagName("article-id")[0].toxml()
		if segment=="abstract":
			if len(collection.getElementsByTagName('abstract')) ==0:
				continue
			absnode = collection.getElementsByTagName('abstract')[0]
			contents = []
			for pnode in absnode.getElementsByTagName("p"):
				pcontent = pnode.toxml()
				if 'ext-link' in pcontent:
					continue
				contents.append(pcontent)

			#content = "".join([node.toxml() for node in ])
			#content = re.sub(r'<[^>]*>'," ",content)
			content = " ".join([re.sub(r'\s+'," ",re.sub(r'<[^>]*>'," ",content)) for content in contents])
			data[pmid] = content
		else:
			sys.stderr.write("this is no segment tag named "+segment+".\n")

	print json.dumps(data)



data_source(sys.argv[1])


