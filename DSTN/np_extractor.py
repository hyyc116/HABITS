#coding:utf-8
import sys
from chunk_parser import *
import datetime
from multiprocessing.dummy import Pool as ThreadPool
import os


class logger:
    def __init__(self,size):
        self._size=size
        self._step=0

    def step(self):
        self._step+=1
        if self._step%self._size==1:
            sys.stderr.write("step:{:}\n".format(self._step))

    def info(self,info):
        sys.stderr.write("INFO:{:}\n".format(info))


LOGGING= logger(10)


def get_paper_list(path):
    papers=[]
    for line in open(path):
        splits = line.strip().split("====")
        if len(splits)!=4:
            continue

        papers.append(splits[-1])
    return papers

def extract_NPs(data):
    LOGGING.step()
    pmcid,abstext = data
    abstext = unicode(abstext,errors="ignore")
    start = datetime.datetime.now()
    tag_list=[]
    np_set=[]
    tag_set=[]
    for iobtags in chunk_content(abstext):
        if iobtags is None:
            continue
        trees = load_iobtags(iobtags)
        if trees is None:
            continue
        np_list,np_tags= get_NPs(trees)
        for i,np in enumerate(np_list):
            if len(np.split())<2:
                continue
            #for word in filters:
            #    if np.endswith(word):
            np_set.append(np.lower())
            tag_set.append(np_tags[i])
    
    now = datetime.datetime.now()
    LOGGING.info("parse:{:}".format((now-start).seconds))
    return pmcid,np_set,tag_set




if __name__=="__main__":
    #papers = get_paper_list(sys.argv[1])
    #loging("{:} articles need to be processed.".format(len(papers)))
    if not os.path.exists(sys.argv[1]):
        open(sys.argv[1],"w").write("\n")
    already_parsed = set([line.strip().split("\t")[0] for line in open(sys.argv[1]) if line.strip()!=""])
    datas=[]
    for line in open(sys.argv[2]):
        splits = line.strip().split("\t")
        if len(splits)!=2:
            continue
        pmcid=splits[0]
        abstext=splits[1]
        if pmcid in already_parsed:
            continue
        datas.append((pmcid,abstext))
    n=1000
    folders = len(datas)/n+1
    for i in range(folders):
        LOGGING.info('===parsing folder {:}.'.format(i))
        m = (i+1)*n if (i+1)*n<len(datas) else len(datas)
        folder_datas = datas[i*n:m]
        pool = ThreadPool(8)
        results = pool.map(extract_NPs, folder_datas)
        for pmcid,np_set,tagset in results:
            for i,np in enumerate(np_set):
                print pmcid+"\t"+np+"\t"+tagset[i]
