# coding=utf-8
import os
import nltk

__author__ = 'gu'

class Helper:
    """
    Helper统计初始概率，转移概率，发射概率的一些方法
    """
    def __init__(self):
        """
        初始转移概率 发射概率为0
        :return:
        """
        self.transition_probability = {'0': {},
                                       '1': {},
                                       '2': {},
                                       '3': {},
                                       '4': {},
                                       '5': {},
                                       '6': {},
                                       '7': {},
                                       '8': {},
                                       '9': {},
                                       '10': {},
                                       '11': {},
                                       '12': {}
                                       }

        self.emission_probability = {'0': {},
                                     '1': {},
                                     '2': {},
                                     '3': {},
                                     '4': {},
                                     '5': {},
                                     '6': {},
                                     '7': {},
                                     '8': {},
                                     '9': {},
                                     '10': {},
                                     '11': {},
                                     '12': {}
                                     }
        self.init_probility()

    def get_states(self):
        """
        隐状态
        :return:
        """
        states = ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12')
        return states

    def get_observationsunicode(self, sentence):
        """
        unicode格式的观察状态格式
        :param sentence:
        :return:
        """
        word_list = []
        for i in sentence:
            word_list.append(i)
        return tuple(word_list)

    def get_txtpathlist(self, dirpath='/PycharmProjects/2014_8_2/train/'):
        """
         获取txt全部的路径
        :param dirpath:
        :return:
        """
        targetpathlist = []
        pathlist = os.listdir(dirpath)
        for path in pathlist:
            subdirpath = dirpath + path
            # for txtpath in os.listdir(subdirpath):
            #     targetpathlist.append(subdirpath + '/' + txtpath)
            # print subdirpath
            targetpathlist.append(subdirpath)
        print len(targetpathlist)
        return targetpathlist

    def combine_alltext(self, pathlist):
        """
        # 整合全部文本内容到一个文件中
        :param pathlist:
        :return:
        """
        wf = open('documents8-2/all_text.txt', 'w+')
        for path in pathlist:
            txt = open(path, 'r')
            text = txt.read()
            wf.write(text)
            wf.write('\n')
            txt.close()
        wf.close()
        print "write all_text done!"

    def get_word_tag(self):
        """
        # 获取词和标注
        :return: word_tag_list
        """
        rf = open('documents8-2/all_text.txt', 'r')
        word_tag_list = []
        lines = rf.readlines()
        for line in lines:
            line = line.replace("\n", "").replace("\r", "")
            wtags = line.split(" ")
            for wt in wtags:
                w_t = wt.split("/")
                if len(w_t) == 2:
                    word_tag_list.append((w_t[0], w_t[1]))
        return word_tag_list

    def get_tag_tag(self):
        """
        # 获取前一个标注 后一个标注的组合
        :return: tag_tag_list
        """
        rf = open('documents8-2/all_text.txt', 'r')
        tag_tag_list = []
        lines = rf.readlines()
        for line in lines:
            line = line.replace("\n", "").replace("\r", "")
            if line != "":
                wtags = line.split(" ")
                for i in range(len(wtags) - 1):

                    forward_w_t = wtags[i].split("/")
                    backward_w_t = wtags[i + 1].split("/")
                    if len(backward_w_t) == 2:
                        tag_tag_list.append((forward_w_t[1], backward_w_t[1]))
        rf.close()
        # fdist = nltk.FreqDist(tag_tag_list)
        # for key,value in fdist.items():
        #      print key, value, fdist.freq(key)
        return tag_tag_list

    def get_words(self, word_tag_list):
        """
        获取全部字
        :param word_tag_list:
        :return:
        """
        wf = open('documents8-2/words.txt', 'w+')
        words = []
        for w, t in word_tag_list:
            words.append(w)
        onlywords = set(words)
        for w in onlywords:
            wf.write(w + " ")
        wf.close()
        print len(onlywords)
        return onlywords

    def get_start_probability(self, word_tag_list):
        """
        开始概率：标注的初始概率
        :param word_tag_list:
        :return:
        """
        fdist = nltk.FreqDist(t for w, t in word_tag_list)
        print fdist.items()
        for key, value in fdist.items():
            print key, value, fdist.freq(key)

    def get_emission_probability(self, word_tag_list):
        """
        获取发射概率，字对应的标注的概率
        :param words:
        :param word_tag_list:
        :return:
        """
        start_pro = self.load_start_profortransemi()

        wf = open('documents8-2/emission_probability.txt', 'w+')
        fdist = nltk.FreqDist(word_tag_list)
        for key, value in fdist.items():
            print key[1], key[0], value, fdist.freq(key) / start_pro[key[1]][0]
            wf.write(key[1] + ' ' + key[0] + ' ' + str(value) + ' ' + str(fdist.freq(key) / start_pro[key[1]][0]))
            wf.write('\n')
        wf.close()

    def get_transition_probability(self, tag_tag_list):
        """
        获取转移概率 前标注转移下一个标注的概率
        :param tag_tag_list:
        :return:
        """
        wf = open('documents8-2/transition_probability.txt','w+')
        start_pro = self.load_start_profortransemi()
        fdist = nltk.FreqDist(tag_tag_list)
        print fdist.items()
        for key, value in fdist.items():
            condition_pro2 = value*1.00 / start_pro[key[0]][0]
            print '频率/频率的条件概率', key[0], key[1], value, condition_pro2
            wf.write(key[0]+' '+key[1]+' '+str(value)+' '+str(condition_pro2))
            wf.write('\n')
        wf.close()

    def load_start_profortransemi(self, path='documents8-2/start_probability.txt'):
        """
        用于计算转移概率 发射概率的格式封装，便于计算
        :param path:
        :return:
        """
        start_pro = {}
        rf = open(path, 'r')
        lines = rf.readlines()
        for line in lines:
            line = line.replace("\n", '')
            line = line.decode("utf-8")
            tag_pro = line.split(" ")
            start_pro[tag_pro[0]] = [eval(tag_pro[1]), eval(tag_pro[2])]
        return start_pro

    def load_words(self, path='documents8-2/words.txt'):
        """
        把语料的字全部加载进来，用于初始化方法
        :param path:
        :return:
        """
        rf = open(path, 'r')
        lines = rf.readlines()
        words = []
        for line in lines:
            line = line.replace("\n", "")
            line = line.decode("utf-8")
            words = line.split(" ")
            words.remove(words[0])
        return words

    def init_probility(self):
        """
        初始化转移概率 发射概率的值为0
        :return:
        """
        words = self.load_words()
        for state0 in self.get_states():
            for state1 in self.get_states():
                self.transition_probability[state0][state1] = 0
            for word in words:
                self.emission_probability[state0][word] = 0

    def load_start_pro(self, path='documents8-2/start_probability.txt'):
        """
        hmm 维特比计算的时候，初始概率的格式封装
        :param path:
        :return:
        """
        start_pro = {}
        rf = open(path, 'r')
        lines = rf.readlines()
        for line in lines:
            line = line.replace("\n", '')
            line = line.decode("utf-8")
            tag_pro = line.split(" ")
            start_pro[tag_pro[0]] = eval(tag_pro[2])
        return start_pro

    def load_transition_pro(self, path='documents8-2/transition_probability.txt'):
        """
        hmm 维特比计算的时候，转移概率的封装
        :param path:
        :return:
        """
        rf = open(path, 'r')
        lines = rf.readlines()
        for line in lines:
            line = line.replace("\n", '')
            line = line.decode("utf-8")
            tag_totag_pro = line.split(" ")
            self.transition_probability[tag_totag_pro[0]][tag_totag_pro[1]] = eval(tag_totag_pro[3])
        return self.transition_probability

    def load_emission_pro(self, path='documents8-2/emission_probability.txt'):
        """
        hmm 维特比计算的时候，发射概率的格式封装
        :param path:
        :return:
        """
        rf = open(path, 'r')
        lines = rf.readlines()
        for line in lines:
            line = line.replace("\n", '')
            line = line.decode("utf-8")
            tag_toword_pro = line.split(" ")
            # print tag_toword_pro
            self.emission_probability[tag_toword_pro[0]][tag_toword_pro[1]] = eval(tag_toword_pro[3])
        return self.emission_probability

# helper = Helper()
# pathlist = helper.get_txtpathlist()

# helper.combine_alltext(pathlist)

# wordtaglist = helper.get_word_tag()
# helper.get_words(wordtaglist)

# helper.get_start_probability(wordtaglist)
# helper.get_emission_probability(wordtaglist)

# tagtaglist = helper.get_tag_tag()
# helper.get_transition_probability(tagtaglist)