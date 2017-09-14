import os
for subdir,dirs,files in os.walk('.'):# traversing through documents 
	for file in files:
		if file.endswith(".xml"): # Access only xml files
			f=open(os.path.join(subdir,file),'r')
			document = f.read()
			f_name = file[14:-4].replace(" ", "")
			os.makedirs(f_name)
			dir_path = os.path.dirname(os.path.realpath(__file__))
			pwd = os.path.join(dir_path,f_name)
			#print (pwd)
			#print(document)
			import xml.etree.ElementTree as ET
			tree = ET.parse(file)
			root = tree.getroot()
			missing = []
			for i,record in enumerate(root.iter('record')):
				is_missing= False
				a_name = []
				for author in record.iter('author'):
					a_name.append(author.text)
				
				if(len(a_name)==0):
					print('Missing')
				else:
					name = a_name[0].split(',')[0]

				title = record.find('titles').find('title').text

				if record.find('dates') is None:
					missing.append(title)
					is_missing = True
				else:
					if record.find('dates').find('year').text is None:
						is_missing = True
						missing.append(title)
					else:
						year = record.find('dates').find('year').text

				if record.find('abstract') is None:
					is_missing = True
					missing.append(title)
				else:
					abstract = record.find('abstract').text
				if is_missing is False:
					file_name = str(i+1)+"."+title[0:240].replace("/", " or ")+","+ year+".txt"
					output = open(os.path.join(pwd,file_name),"w+")
					output.write("%s%s,%s,\"%s\""%(name,year,title,abstract))
					print("%s%s,%s,\"%s\""%(name,year,title,abstract))
					output.close()
				print ('\n----------------------------------------------------------------\n')
			output = open(os.path.join(pwd,'missing.txt'),'w+')
			missing = list(set(missing))
			output.write("%s"%"\n\n".join(missing))
			print("%s"%"\n".join(missing))


			print(root)
			print('--------------------------------------------------------')
			f.close()
