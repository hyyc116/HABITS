#coding:utf-8


import sys
from collections import defaultdict

def filter_already_known(known_therapy_path, scale_therapy):
    already_known=set([line.split("\t")[0] for line in open(known_path)])
    for line in open(scale_therapy):
        line= line.strip()
        if line.split("\t")[0] not in already_known:
            yield line

def scale_therapy_linking(known_therapy_path, known_scale_path, scale_therapy, scale_NPs_path):
    #from a list of therapy find the related test
    new_therapies = filter_already_known(known_therapy_path,scale_therapy)
    #known_scales
    known_scales=set([line.strip().split("\t")[0] for line in open(known_scale_path)])
    

    # scale_NPs.txt
    #from this file, get pmcid contain this therapy
    pt_dic=defaultdict(set)
    for line in open(scale_NPs_path):
        line=line.strip()
        splits = line.split("\t")
        if len(splits)!=3:
            continue
        if splits[1] in therapy_set:
            pt_dic[splits[0]].add(splits[1])

    pmcidset = set(pt_dic.keys())

    #tests_scales.txt
    for line in open(scale_NPs_path):
        splits = line.strip().split("\t")
        if len(splits)!=3:
            continue
        if splits[0] in pmcidset and splits[1] in known_scales:
            for therapy in pt_dic[splits[0]]:
                print splits[0]+"=="+splits[1]+"=="+therapy


if __name__ == '__main__':
    scale_therapy_linking(sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4])


