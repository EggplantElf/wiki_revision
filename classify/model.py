from __future__ import division
import cPickle
import gzip


class Model:
    def __init__(self, modelfile = None):
        if modelfile:
            self.load(modelfile)
            self.free = False
        else:
            self.feat_dict = {'#': 0}
            self.label_dict = {'#': 0}
            self.word_dict = self.read_words('../extract/dict.txt')
            self.free = True

    def save(self, modelfile):
        stream = gzip.open(modelfile,'wb')
        cPickle.dump(self.feat_dict, stream, -1)
        cPickle.dump(self.label_dict, stream, -1)
        cPickle.dump(self.word_dict, stream, -1)
        stream.close()

    def load(self, modelfile):
        stream = gzip.open(modelfile,'rb')
        self.feat_dict = cPickle.load(stream)
        self.label_dict = cPickle.load(stream)
        self.word_dict = cPickle.load(stream)
        stream.close()

    def map_feat(self, feat_str):
        if self.free and feat_str not in self.feat_dict:
            self.feat_dict[feat_str] = len(self.feat_dict)
        return self.feat_dict.get(feat_str, None)

    def map_label(self, label_str):
        if self.free and label_str not in self.label_dict:
            self.label_dict[label_str] = len(self.label_dict)
        return self.label_dict.get(label_str, None)

    # set or dict?
    def read_words(self, filename):

        self.wlist = frozenset(line.strip() for line in open(filename))


