import urllib
import re
import string
import os

try:
    from bs4 import BeautifulSoup
except ImportError:
    from BeautifulSoup import BeautifulSoup


def count_lines(file_no,book_no):

    path_s = "dataset/Rig_Veda_"+str(book_no)+"/Rig_veda_"+str(file_no)+"_eng.txt"
    path_e = "dataset/Rig_Veda_"+str(book_no)+"/Rig_veda_"+str(file_no)+"_eng.txt"

    if os.path.isfile(path_e) and os.path.isfile(path_e):
        target_eng = open(path_e, 'r')
        target_sans = open(path_s, 'r')
        num_lines_eng = sum(1 for line in target_eng)
        num_lines_sans = sum(1 for line in target_sans)
        # to check if no of lines in sanskrit and english file are same or not.
        if (num_lines_sans == num_lines_eng):
            print num_lines_eng
        else:
            print num_lines_eng, num_lines_sans, file_no


def scrap_each_book(book_link,book_no):
    url="http://sacred-texts.com/hin/rigveda/"+book_link+".htm"
    
    
    html = urllib.urlopen(url)
    soup = BeautifulSoup(html)

    h_tag = soup.find('h4')
    for br in h_tag.find_next_siblings():
        link = br.get('href')
        if link != None:
            count_lines(link,book_no)
    

def main():
    #scrapping all books one by book
    for i in range (1,10): 
        scrap_each_book('rvi0'+str(i),i)
    scrap_each_book('rvi10',10)


if __name__ == "__main__":
    main()
