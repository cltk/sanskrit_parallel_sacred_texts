import urllib
import re
import os 
import string
try:
	from bs4 import BeautifulSoup
except ImportError:
	from BeautifulSoup import BeautifulSoup

def scrap_doc(file_no):	
	urls="http://sacred-texts.com/hin/rvsan/"+str(file_no)
	urle="http://sacred-texts.com/hin/rigveda/"+str(file_no)

	html = urllib.urlopen(urle)
	soup = BeautifulSoup(html)

	#to remove <a></a>
	for a in soup.findAll('a'):
		del a['href']

	text= soup.find_all('p')[1]
	text= text.encode('utf-8')

	text= text.replace('<br/>', '#')
	
	text = re.sub("(<[^>]+>)", '', text)
	#print text.count('#')
	text= text[1:]

	#replace every digit with space
	text=re.sub(" \d+", " ", text)
	text=text.split('#')

	#removing punctuation from strings , uncommenth this if you dont want to remove punctuation
	regex = re.compile('[%s]' % re.escape(string.punctuation))
	target_e = open("dataset/Rig_Veda/Rig_veda_"+str(file_no)+"_eng.txt", 'w')



	no_sentences_eng=0
	for i in range(len(text)):
		line=regex.sub('', text[i]).strip()
		

		if line!="":
			#print line
			line+='.'
			target_e.write(line.lower())
			target_e.write("\n")
			no_sentences_eng+=1


	#print no_sentences_eng
	#now scrapping the sanskrit doc.
	html = urllib.urlopen(urls)
	soup = BeautifulSoup(html)
	#print soup

	s=""
	h_tag=soup.find('h3')
	s+=(h_tag.nextSibling).encode('utf-8')
	
	for br in soup.find('h3').find_next_siblings():
		s+= ((br.nextSibling).encode('utf-8')) 


	#print s
	s = s.replace('||', '#')
	s = s.replace('|', '#')

	#counting no of lines in sanskrit text
	no_sentences_sanskrit= s.count('#')/2
	text=s.split('#')
	#print no_sentences_sanskrit
	target_s = open("dataset/Rig_Veda/Rig_veda_"+str(file_no)+"_sans.txt", 'w')

	flag=0  # flag to check if file should be deleted or not
	for i in range(no_sentences_sanskrit):
		line=regex.sub('', text[i]).strip()
		#print line
		if line!="":
			line+='|'
			
			#checking if the sanskrit file contains any english line by mistake , if so delete such file 
			check= re.search('[a-zA-Z]+',line)
			if check!=None:
				print check,"sentences are not completely written"
				flag=1
				break

			target_s.write(line.lower())
			target_s.write("\n")
			

	if no_sentences_sanskrit!=no_sentences_eng or flag :
		print "files not equal", file_no		

		try:
			os.remove("dataset/Rig_Veda/Rig_veda_"+str(file_no)+"_eng.txt")
			os.remove("dataset/Rig_Veda/Rig_veda_"+str(file_no)+"_sans.txt")
		except OSError:
			pass		

#scrapping all the linking together
def sacred_texts():
	url="http://sacred-texts.com/hin/rigveda/rvi01.htm"


	html = urllib.urlopen(url)
	soup = BeautifulSoup(html)

	
	h_tag=soup.find('h4')
	c=0
	for br in h_tag.find_next_siblings():
		link=br.get('href')
		if link!=None:
			c=c+1
			print c
			scrap_doc(link)

if __name__ == "__main__":
	sacred_texts()