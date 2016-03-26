from subprocess import call

#python wrapper to clone any git repository , below is just an example to clone cltk repo 
def clone_git_repo(url,dir='repository'): 
	subprocess.call('mkdir '+dir ,shell=True)
	print subprocess.call('cd '+dir +' \n '+ url,shell=True)
	

def get_url_lastpart(url):
	return url.rsplit('/', 1)[-1]

#corpus preparation 
'''
cd
 mkdir corpus
 cd corpus 
 wget http://www.statmt.org/wmt13/training-parallel-nc-v8.tgz
 tar zxvf training-parallel-nc-v8.tgz
'''     
def corpus_preparation(corpus_dir_loc='corpus ',corpus_url='http://www.statmt.org/wmt13/training-parallel-nc-v8.tgz '):
	print get_url_lastpart(corpus_url)
	subprocess.call('cd', shell=True)
	subprocess.call('mkdir '+corpus_dir_loc, shell=True)
  	subprocess.call('cd '+ corpus_dir_loc+'\n'+ 'wget '+corpus_url, shell=True)
  	subprocess.call('cd '+ corpus_dir_loc+'\n'+'tar zxvf '+ get_url_lastpart(corpus_url) , shell=True)
  
#Tokenization 
'''
  ~/mosesdecoder/scripts/tokenizer/tokenizer.perl -l en \
    < ~/corpus/training/news-commentary-v8.fr-en.en    \
    > ~/corpus/news-commentary-v8.fr-en.tok.en
 ~/mosesdecoder/scripts/tokenizer/tokenizer.perl -l fr \
    < ~/corpus/training/news-commentary-v8.fr-en.fr    \
    > ~/corpus/news-commentary-v8.fr-en.tok.fr
'''
def tokenization(script_to_use='~/mosesdecoder/scripts/tokenizer/tokenizer.perl' ,corpus_to_use_lang1='< ~/corpus/training/news-commentary-v8.fr-en.en'
	            ,loc_to_tokenize_lang1='> ~/corpus/news-commentary-v8.fr-en.tok.en' ,corpus_to_use_lang2='< ~/corpus/training/news-commentary-v8.fr-en.fr',
	            loc_to_tokenize_lang2='> ~/corpus/news-commentary-v8.fr-en.tok.fr'):
	subprocess.call(script_to_use+' -l en '+corpus_to_use_lang1 +loc_to_tokenize_lang1, shell=True)
   	subprocess.call(script_to_use+' -l fr '+ corpus_to_use_lang2 +loc_to_tokenize_lang2, shell=True)

#Truecaser
'''
~/mosesdecoder/scripts/recaser/train-truecaser.perl \
     --model ~/corpus/truecase-model.en --corpus     \
     ~/corpus/news-commentary-v8.fr-en.tok.en
 ~/mosesdecoder/scripts/recaser/train-truecaser.perl \
     --model ~/corpus/truecase-model.fr --corpus     \
     ~/corpus/news-commentary-v8.fr-en.tok.fr
'''
def truecaser(script_to_use='~/mosesdecoder/scripts/recaser/train-truecaser.perl',model_file_lang1='~/corpus/truecase-model.en',corpus_to_use_lang1='~/corpus/news-commentary-v8.fr-en.tok.en'
	   ,model_file_lang2='~/corpus/truecase-model.fr',corpus_to_use_lang2='~/corpus/news-commentary-v8.fr-en.tok.fr'):
	subprocess.call(script_to_use+' --model '+model_file_lang1+' --corpus '+corpus_to_use_lang2, shell=True)
	subprocess.call(script_to_use+' --model '+model_file_lang2+' --corpus '+corpus_to_use_lang1, shell=True)

#Truecasing
'''
~/mosesdecoder/scripts/recaser/truecase.perl \
   --model ~/corpus/truecase-model.en         \
   < ~/corpus/news-commentary-v8.fr-en.tok.en \
   > ~/corpus/news-commentary-v8.fr-en.true.en
 ~/mosesdecoder/scripts/recaser/truecase.perl \
   --model ~/corpus/truecase-model.fr         \
   < ~/corpus/news-commentary-v8.fr-en.tok.fr \
   > ~/corpus/news-commentary-v8.fr-en.true.fr
'''
def truecasing(script_to_use='~/mosesdecoder/scripts/recaser/truecase.perl',truecase_model_lang1="~/corpus/truecase-model.en",input_tokenised_file_lang1="< ~/corpus/news-commentary-v8.fr-en.tok.en",
	output_truecased_file_lang1="> ~/corpus/news-commentary-v8.fr-en.true.en",truecase_model_lang2='~/corpus/truecase-model.fr', input_tokenised_file_lang2='< ~/corpus/news-commentary-v8.fr-en.tok.fr',
	output_truecased_file_lang2='> ~/corpus/news-commentary-v8.fr-en.true.fr'):
 	subprocess.call(script_to_use+' --model '+truecase_model_lang1+input_tokenised_file_lang1+output_truecased_file_lang1, shell=True)
   	subprocess.call(script_to_use+' --model '+truecase_model_lang2+input_tokenised_file_lang2+output_truecased_file_lang2, shell=True)
   
#cleaning
'''
~/mosesdecoder/scripts/training/clean-corpus-n.perl \
    ~/corpus/news-commentary-v8.fr-en.true fr en \
    ~/corpus/news-commentary-v8.fr-en.clean 1 80
'''    
def cleaning(script_to_use='~/mosesdecoder/scripts/training/clean-corpus-n.perl',combined_corpus_to_use='~/corpus/news-commentary-v8.fr-en.true',
	output_cleaned_file='~/corpus/news-commentary-v8.fr-en.clean',min_len=1,max_len=80):
	subprocess.call(script_to_use+' '+combined_corpus_to_use+' fr en '+output_cleaned_file + ' ' + str(min_len) + ' ' +str(max_len) ,shell=True)

 
#binarise a file
'''
~/mosesdecoder/bin/build_binary \
   news-commentary-v8.fr-en.arpa.en \
   news-commentary-v8.fr-en.blm.en
'''   
def binarize(script_to_use='~/mosesdecoder/bin/build_binary' ,input_file_to_binarize='news-commentary-v8.fr-en.arpa.en',output_binarized_file='news-commentary-v8.fr-en.blm.en'):
	subprocess.call(script_to_use+' '+input_file_to_binarize+' '+ output_binarized_file ,shell=True)   	 

#Building ngram Language Model 
'''mkdir ~/lm
 cd ~/lm
 ~/mosesdecoder/bin/lmplz -o 3 <~/corpus/news-commentary-v8.fr-en.true.en > news-commentary-v8.fr-en.arpa.en
'''
def build_ngram_model(script_to_use='~/mosesdecoder/bin/lmplz' ,dir_for_model='~/lm',input_corpus='<~/corpus/news-commentary-v8.fr-en.true.en'
	,output_ngram_model='> news-commentary-v8.fr-en.arpa.en',ngram_count=3):
	subprocess.call(script_to_use+' '+'-o '+str(ngram_count)+' '+input_corpus+' '+ output_ngram_model,shell=True) 	

#Training the model
'''
mkdir ~/working
 cd ~/working
 nohup nice ~/mosesdecoder/scripts/training/train-model.perl -root-dir train \
 -corpus ~/corpus/news-commentary-v8.fr-en.clean                             \
 -f fr -e en -alignment grow-diag-final-and -reordering msd-bidirectional-fe \
 -lm 0:3:$HOME/lm/news-commentary-v8.fr-en.blm.en:8                          \
 -external-bin-dir ~/mosesdecoder/tools >& training.out &
'''
def training_model(script_to_use='nohup nice ~/mosesdecoder/scripts/training/train-model.perl',working_dir='~/working',input_corpus_for_training='~/corpus/news-commentary-v8.fr-en.clean'):
	subprocess.call('mkdir '+working_dir,shell=True)
	subprocess.call('cd '+working_dir+' \n '+script_to_use+' -root-dir train '+' -corpus '+input_corpus_for_training+' -f fr -e en -alignment grow-diag-final-and -reordering msd-bidirectional-fe \
 	-lm 0:3:$HOME/lm/news-commentary-v8.fr-en.blm.en:8 -external-bin-dir ~/mosesdecoder/tools  ' ,shell=True)

#Testing
'''~/mosesdecoder/bin/moses -f ~/working/mert-work/moses.ini'''
def testing(script_to_use='~/mosesdecoder/bin/moses',input_moses_file='~/working/mert-work/moses.ini'):
	subprocess.call(script_to_use+' -f '+input_moses_file,shell=True)

#binarise the phrase-table and lexicalised reordering models
'''
mkdir ~/working/binarised-model
 cd ~/working
 ~/mosesdecoder/bin/processPhraseTableMin \
   -in train/model/phrase-table.gz -nscores 4 \
   -out binarised-model/phrase-table
 ~/mosesdecoder/bin/processLexicalTableMin \
   -in train/model/reordering-table.wbe-msd-bidirectional-fe.gz \
   -out binarised-model/reordering-table'''

def binarizePrasetable_lexicalreordering(script_to_use_phrase='~/mosesdecoder/bin/processPhraseTableMin',script_to_use_lexical='~/mosesdecoder/bin/processLexicalTableMin',
	working_dir_binarise='~/working/binarised-model',working_dir='~/working',input_phrase_table='train/model/phrase-table.gz',output_phrase_table='binarised-model/phrase-table',
	input_lexical_table='train/model/reordering-table.wbe-msd-bidirectional',output_lexical_table='binarised-model/reordering-table'
	,nscores_count=4):
	subprocess.call('mkdir '+working_dir_binarise,shell=True)
	subprocess.call('cd '+working_dir+' \n '+script_to_use_phrase+' -in '+input_phrase_table +' -nscores '+str(nscores_count)+' -out '+output_phrase_table,shell=True)
	subprocess.call('cd '+working_dir+' \n '+script_to_use_lexical+' -in '+input_lexical_table +' -out '+output_lexical_table,shell=True)

#BLEU score
'''nohup nice ~/mosesdecoder/bin/moses            \
   -f ~/working/filtered-newstest2011/moses.ini   \
   < ~/corpus/newstest2011.true.fr                \
   > ~/working/newstest2011.translated.en         \
   2> ~/working/newstest2011.out 
 ~/mosesdecoder/scripts/generic/multi-bleu.perl \
   -lc ~/corpus/newstest2011.true.en              \
   < ~/working/newstest2011.translated.en'''

def bleu_score(script_to_use='nohup nice ~/mosesdecoder/bin/moses',filtered_moses_file='~/working/filtered-newstest2011/moses.ini',
	input_test_file_lang1='~/corpus/newstest2011.true.fr',output_translated_file='~/working/newstest2011.translated.en',
	script_to_use_bleu='~/mosesdecoder/scripts/generic/multi-bleu.perl' ,input_test_file_lang2='~/corpus/newstest2011.true.en'):
	subprocess.call(script_to_use+' -f '+filtered_moses_file+' '+input_test_file_lang1+' '+output_translated_file+' '+'2> ~/working/newstest2011.out ',shell=True)
	subprocess.call(script_to_use_bleu+' -lc '+input_test_file_lang2+' '+output_translated_file,shell=True)

#list of all the methods required to make a baseline moses model.
corpus_preparation()
tokenization()  
#clone_git_repo("git clone https://github.com/coderbhupendra/cltk.git",'repository')	  
truecaser()
truecasing()
cleaning()
build_ngram_model()
binarize()
training_model()
#similarly for tuning and training we can use above methods just by changing the default paramter values
testing()
bleu_score()

