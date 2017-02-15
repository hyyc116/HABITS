#coding:utf-8

import sys

def filter_therapy(path):
    filters=['therapy','training','treatment',"treatments",'stimulation','program']
    infilter=['practice']
    therapy_set=[]
    for line in open(path):
        line = line.strip()
        splits = line.split("\t")
        if len(splits)!=3:
            continue

        pmcid= splits[0]
        wordseq=splits[1].split()
        tagseq=splits[2].split()
        if len(wordseq)!=len(tagseq):
            continue

        if len(wordseq)>1:
            
            # filter out length 
            if len(wordseq)==1:
                continue

            #filter 2 size with one article
            if tagseq[0]=="CD" or tagseq[0]=="DT" or tagseq[0]=="POS":
                continue
            
            #endswith words in filters
            for word in filters:
                if splits[1].endswith(word):
                    therapy_set.append(splits[1]+"\t"+splits[2])
            
            #in filters
            for word in infilter:
                if word in splits[1]:
                    therapy_set.append(splits[1]+"\t"+splits[2])

    dic={}
    for therapy in therapy_set:
        dic[therapy] = dic.get(therapy,0)+1

    for k,v in sorted(dic.items(),key=lambda x:x[1], reverse=True):
        if v>0:
            print k+"\t"+str(v)



if __name__=="__main__":
    filter_therapy(sys.argv[1])
