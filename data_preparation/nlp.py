import logging
import os
import tempfile
import nltk
import gensim
from nltk.tokenize import RegexpTokenizer
from nltk.stem.porter import PorterStemmer
from nltk.corpus import stopwords
from gensim import corpora,models
from six import iteritems
from six import iteritems
import time

# 分词前特殊的文本预预处理，过滤中文符号
#in:doc_set;  out:doc_set
def spec_preprocess(doc_set):
    new_doc_set = []
    for doc in doc_set:
        new_doc_set.append(doc.replace('…', ' . '))
    return new_doc_set


'''
function: dealDocset()
input:  doc_set: 类型list，文档集，每个元素是一篇文档
output: 词典dictionary和语料库corpus
'''
def dealDocset(doc_set):
    '''
    clean documents:
    Tokenizing: converting a document to its atomic elements.
    Stopping: removing meaningless words.
    Stemming: merging words that are equivalent in meaning.
    '''
    # Tokenization: token化
    docs_tokenize = []
    for doc in doc_set:
        # 分句
        sens = nltk.sent_tokenize(doc)
        words = []
        for sent in sens:
            # 分词
            # note：nltk.word_tokenize()返回一个list，即[]
            words = words + nltk.word_tokenize(sent)
            # words.append(nltk.word_tokenize(sent))
        docs_tokenize.append(words)
    # print(docs_token)
    print("doc lines: ", len(docs_tokenize))

    # Stopping: removing meaningless words 去停用词，同时去标点符号
    en_stop = stopwords.words("english")
    english_punctuations = ['', '\n', '\t', ',', '.', ':', ';', '?', '(', ')', '[', ']', '&', '!', '*',
                            '@', '#', '$', '%', '"', "'", "-", "--", "•", "...", "..", "''", "``"]
    cn_punctuations = ['，', '。', '：', '；', '？', '（', '）', '【', '】', '&', '！',
                       '*', '@', '#', '￥', '%', '“', '”', "‘", "’", "—", "–", "◦", "…", "……"]
    spec_stop = ['app', "'s", "'t", "'ll", "'m", "'re", "'vt", "a's", '■', '◉',
                 '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    stoplist = en_stop + english_punctuations + cn_punctuations + spec_stop
    docs_stop = []
    for doc in docs_tokenize:
        doc_stop = [token for token in doc if ((not token in stoplist) and (not str(token).isdigit()))]
        docs_stop.append(doc_stop)
    # print(docs_stop)

    # Stemming: merging words that are equivalent in meaning.
    # Create p_stemmer of class PorterStemmer
    # 对于提取词词干，nltk提供了Porter和Lancaster两个stemer
    p_stemmer = PorterStemmer()
    docs_stemmed = []
    for doc in docs_stop:
        doc_stemmed = [p_stemmer.stem(token) for token in doc]
        docs_stemmed.append(doc_stemmed)
    # print(docs_stemmed)

    # Constructing a document-term matrix
    dictionary = corpora.Dictionary(docs_stemmed)
    corpus = [dictionary.doc2bow(doc) for doc in docs_stemmed]
    # print(corpus[0])
    print(len(corpus))
    return (dictionary,corpus)

def ldadeal(corpus,dictionary,numtopics=5,path_r2='',docname='unknown'):
    # Applying the LDA model
    ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics=numtopics, id2word=dictionary, passes=20)
    # print(ldamodel.print_topics(10,10))
    ldamodel.save(path_r2 + docname + ".ldamodel")
    dictionary.save(path_r2 + docname + ".dict")
    corpora.MmCorpus.serialize(path_r2 + docname + ".mm", corpus, id2word=dictionary)

def mainwork(docname,workpath,textdatapath,numtopics=2):
    #path-set
    path_r=workpath
    path_r1=textdatapath
    #path_r1=path_r+"/description/"
    # path_r1=path_r+"/reviews/"
    path_r2=path_r+"/model/"
    path_r3=path_r+"/result1/"
    path_r4=path_r+"/result2/"
    path_r5=path_r+"/jsondata/"
    # import documents: 载入文档
    doc_set = [line.lower() for line in open(path_r1 + docname + '.txt', mode='r', encoding="utf-8")]

    doc_set=spec_preprocess(doc_set)

    (dictionary, corpus)=dealDocset(doc_set)

    ldadeal(corpus,dictionary,numtopics=numtopics,path_r2=path_r2,docname=docname)

def mainwork2(docname,workpath):
    #work for description

    #path-set
    path_r=workpath
    path_r1=path_r+"/description/"
    path_r2=path_r+"/model/"
    path_r3=path_r+"/result1/"
    path_r4=path_r+"/result2/"
    path_r5=path_r+"/jsondata/"
    #other deal of nlp after mainwork
    dictionary = corpora.Dictionary.load(path_r2 + docname + '.dict')
    corpus = corpora.MmCorpus(path_r2 + docname + '.mm')
    ldamodel = gensim.models.ldamodel.LdaModel.load(path_r2 + docname + ".ldamodel")
    #print(ldamodel.print_topics(5, 10))

    topics_matrix = ldamodel.show_topics(formatted=False, num_words=10)
    # topics_matrix=np.array(topics_matrix)
    # topic_words=topics_matrix[:,:,1]
    # for i in topic_words:
    # print([str(word) for word in i])
    outfile1 = open(path_r3 + docname + '.txt', mode='a', encoding='utf-8')
    outfile2 = open(path_r4 + docname + '.txt', mode='a', encoding='utf-8')
    for topic in topics_matrix:
        (topicid, words) = topic
        for word in words:
            outfile1.write(str(word[0]) + '\n')
            outfile2.write(str(word[0])+' '+str(word[1])+ '\n')
            # word--(wordstr,概率)
            # print(word[0],str(word[1]))
    outfile1.close()
    outfile2.close()
    return

def mainwork3(docname,workpath):
    #work for reviews
    #second part of mainwork of reviews nlp

    #path-set
    #here workpath is /reviews/...
    path_r=workpath
    path_r1=path_r+"/reviews/"
    path_r2=path_r+"/model/"
    path_r3=path_r+"/result1/"
    path_r4=path_r+"/result2/"
    #path_r5=path_r+"/jsondata/"
    #other deal of nlp after mainwork
    dictionary = corpora.Dictionary.load(path_r2+ docname + '.dict')
    corpus = corpora.MmCorpus(path_r2+ docname + '.mm')
    ldamodel = gensim.models.ldamodel.LdaModel.load(path_r2+ docname + ".ldamodel")
    #print(ldamodel.print_topics(10, 10))

    topics_matrix = ldamodel.show_topics(formatted=False, num_words=10)
    # topics_matrix=np.array(topics_matrix)
    # topic_words=topics_matrix[:,:,1]
    # for i in topic_words:
    # print([str(word) for word in i])
    outfile1 = open(path_r3 + docname + '.txt', mode='a', encoding='utf-8')
    outfile2 = open(path_r4 + docname + '.txt', mode='a', encoding='utf-8')
    for topic in topics_matrix:
        (topicid, words) = topic
        for word in words:
            outfile1.write(str(word[0]) + '\n')
            outfile2.write(str(word[0]) + ' ' + str(word[1]) + '\n')
            # word--(wordstr,概率)
            # print(word[0],str(word[1]))
    outfile1.close()
    outfile2.close()
    return


def descriptionnlp(appinfospath):
    #work for desc
    #appinfospath="..../appinfos"

    path_r=appinfospath
    path_r1=path_r+"/description/"
    path_r2=path_r+"/model/"
    path_r3=path_r+"/result1/"
    path_r4=path_r+"/result2/"
    path_r5=path_r+"/jsondata/"
    filelist=os.listdir(path_r1)
    #print(reviewslist)
    docnamelist=[reviews.split('.txt')[0] for reviews in filelist]
    #print(docnamelist)
    #print(len(docnamelist))

    #creat two recordfile: success--reviews not empty;fail----reviews empty
    recordfile1=open(path_r+"/success.txt",mode='w',encoding='utf-8')
    recordfile2=open(path_r+"/fail.txt",mode='w',encoding='utf-8')
    recordfile3 = open(path_r + "/errors.txt", mode='w', encoding='utf-8')

    for docname in docnamelist:
        if os.path.getsize(path_r1+docname+".txt")==0:
            recordfile2.write(str(docname)+'\n')
            continue
        else:
            recordfile1.write(str(docname)+'\n')

            try:
                mainwork(docname, path_r, path_r1, numtopics=2)
                mainwork2(docname, path_r)
            except Exception as e:
                print('Dealing with file '+str(docname)+" Failed!")
                recordfile3.write(str(docname)+'\n')

    recordfile1.close()
    recordfile2.close()
    recordfile3.close()
    return

def reviewsnlp(reviewspath):
    #work for reviews
    #path_r="./reviews"
    #path_r1="./reviews/reviews/"
    #path_r2="./reviews/model/"
    #path_r3="./reviews/result1/"
    #path_r4="./reviews/result2/"

    path_r=reviewspath
    path_r1=path_r+"/reviews/"
    path_r2=path_r+"/model/"
    path_r3=path_r+"/result1/"
    path_r4=path_r+"/result2/"
    #path_r5=path_r+"/jsondata/"
    filelist=os.listdir(path_r1)
    #print(reviewslist)
    docnamelist=[reviews.split('.txt')[0] for reviews in filelist]
    #print(docnamelist)
    #print(len(docnamelist))

    #creat three recordfile: success--reviews not empty;fail----reviews empty;errors for spec
    recordfile1=open(path_r+"/success.txt",mode='w',encoding='utf-8')
    recordfile2=open(path_r+"/fail.txt",mode='w',encoding='utf-8')
    recordfile3 = open(path_r + "/errors.txt", mode='w', encoding='utf-8')

    for docname in docnamelist:
        if docname.startswith('nores'):
            continue

        if os.path.getsize(path_r1+docname+".txt")==0:
            recordfile2.write(str(docname)+'\n')
            continue
        else:
            recordfile1.write(str(docname)+'\n')
            try:
                mainwork(docname, path_r, path_r1, numtopics=10)
                mainwork3(docname, path_r)
            except Exception as e:
                print('Dealing with file '+str(docname)+" Failed!")
                recordfile3.write(str(docname)+'\n')


    recordfile1.close()
    recordfile2.close()
    recordfile3.close()
    return


if __name__ == '__main__':
    #db = pymysql.connect(host="localhost", user="root", password="mwq199502", db="appnet2", port=3306, charset='utf8')
    #cur = db.cursor()
    print("Good start!")

    homepath='D:/pycode/appnet/step1/data'
    #0-200
    packagestart=0
    packageend=200
    #prepare dir and applist
    #prepareApplist(cur,db,homepath,packagestart,packageend)

    #crawl
    #crawldata(homepath,packagestart,packageend)

    #nlp
    #test for single package--package 1
    #packagepath=homepath+"/package1"
    #descriptionnlp(packagepath+"/appinfos")
    #reviewsnlp(packagepath+"/reviews")
    #work
    for i in range(packagestart,packageend):
        runlogfile = open(homepath + "/packagelog.txt", mode='a', encoding='utf-8')
        starttime=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        runlogfile.write(starttime+"  package"+str(i+1)+" start to deal...\n")
        print(starttime+"  package"+str(i+1)+" start to deal...")

        try:
            packagepath = homepath + "/package" + str(i + 1)
            descriptionnlp(packagepath + "/appinfos")
            reviewsnlp(packagepath + "/reviews")
        except Exception as e:
            print("Meeting error when dealing with package "+str(i+1)+"!")
            runlogfile.write("Meeting error when dealing with package "+str(i+1)+"!\n")

        endtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        runlogfile.write(endtime + "  package" + str(i + 1) + " end to deal...")
        print(endtime + "  package" + str(i + 1) + " end to deal...\n")
        runlogfile.close()

    print("Good end!")

    #cur.close()
    #db.close()
