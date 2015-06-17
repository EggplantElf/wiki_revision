import pymongo
from pymongo import MongoClient
from bson.objectid import ObjectId
import gzip
import cPickle
from model import *

def get_collections(url, db, cl):
    client = MongoClient(url)
    return client[db][cl]

def get_annotated_pairs(pairs, label_file, dump_file):
    annotated = []
    for line in open(label_file):
        items = line.strip().split()
        pid, label = ObjectId(items[0]), items[1]
        pair = pairs.find_one(pid)
        annotated.append((label, pair))
        if len(annotated) % 10 == 0:
            print len(annotated)

    stream = gzip.open(dump_file,'wb')
    cPickle.dump(annotated, stream, -1)
    stream.close()

def get_annotated_from_dump(dump_file):
    stream = gzip.open(dump_file,'rb')
    annotated = cPickle.load(stream)
    stream.close()
    return annotated

def get_training_instances(annotated, model_file):
    model = Model()
    instances = []
    for (label, pair) in annotated:
        label = model.map_label(label)
        feats = {}
        for feat_str in ['editDistance', 'editRatio', 'diffRatio', 'newPartLen', 'oldPartLen']:
            extract_numeric_feats(model, feats, pair, feat_str)
        for feat_str in ['editorID', 'isMinor', 'newPartInDict', 'oldPartInDict']:
            extract_literal_feats(model, feats, pair, feat_str)
        instances.append((label, feats))
    model.save(model_file)
    return instances

def extract_numeric_feats(model, feats, pair, feat_str):
    feat = model.map_feat(feat_str)
    if feat:
        feats[feat] = pair[feat_str]

def extract_literal_feats(model, feats, pair, feat_str):
    feat = model.map_feat('%s:%s' % (feat_str, pair[feat_str]))
    if feat:
        feats[feat] = 1

def write_instances_to_libsvm_format(instances, output_file):
    o = open(output_file, 'w')
    for (label, feats) in instances:
        o.write('%s %s\n' % (label, ' '.join('%d:%.2f' % (k, v) for (k, v) in feats.items())))
    o.close()


if __name__ == '__main__':
    pairs = get_collections('mongodb://admin:admin@ds039211.mongolab.com:39211/annotator-3', 'annotator-3', 'pairs')
    # get_annotated_pairs(pairs, '../data/vote.txt', '../data/annotated.dump')
    annotated = get_annotated_from_dump('../data/annotated.dump')
    # l, d = annotated[0]
    # for k in d:
    #     print k, '-->', d[k]
    instances = get_training_instances(annotated, '../data/test.model')
    write_instances_to_libsvm_format(instances, '../data/instances.txt')
    # print instances[0]



