import urllib
import re
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


	text = soup.find_all('p')[1]
	text= text.encode('utf-8')
	text= text.replace('<br/>', '#')
	text= text[5:len(text)-4]

	#replace every digit with space
	text=re.sub(" \d+", " ", text)
	text=text.split('#')

	
	#removing punctuation from strings , uncomment his if you dont want to remove punctuation
	regex = re.compile('[%s]' % re.escape(string.punctuation))
	target = open("English_setences.txt", 'aw')



	no_sentences=0
	for i in range(len(text)):
		line=regex.sub('', text[i]).strip()
		

		if line!="":
			#print line
			line+='.'
			target.write(line.lower())
			target.write("\n")
			no_sentences+=1


	#print no_sentences
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
	s = s.replace(' ||', '#')
	s = s.replace(' |', '#')

	text=s.split('#')
	#print len(text)
	target = open("Sanskrit_setences.txt", 'aw')
	for i in range(no_sentences):
		line=regex.sub('', text[i]).strip()
		#print line
		if line!="":
			line+='|'
			target.write(line.lower())
			target.write("\n")
			no_sentences+=1

#scrapping all the linking together
for i in range (1190,1191):
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
