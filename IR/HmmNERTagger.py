# coding=utf-8
__author__ = 'gu'

from helper import Helper


def print_dptable(V):
    """
    打印路径概率表
    :param V:
    :return:
    """
    print "    ",
    for i in range(len(V)): print "%7d" % i,
    print

    for y in V[0].keys():
        print "%.5s:  " % y,
        for t in range(len(V)):
            print "%.7s " % ("%f" % V[t][y]),
        print


def viterbi(obs, states, start_p, trans_p, emit_p):
    """
    :param obs:观测序列
    :param states:隐状态
    :param start_p:初始概率（隐状态）
    :param trans_p:转移概率（隐状态）
    :param emit_p: 发射概率 （隐状态表现为显状态的概率）
    :return:
    """
    # 路径概率表 V[时间][隐状态] = 概率
    V = [{}]
    # 一个中间变量，代表当前状态是哪个隐状态
    path = {}

    # 初始化初始状态 (t == 0)
    for y in states:
        V[0][y] = start_p[y] * emit_p[y][obs[0]]
        path[y] = [y]

    # 对 t > 0 跑一遍维特比算法
    for t in range(1, len(obs)):
        V.append({})
        newpath = {}

        for y in states:
            # 概率 隐状态 =    前状态是y0的概率 * y0转移到y的概率 * y表现为当前状态的概率
            (prob, state) = max([(V[t - 1][y0] * trans_p[y0][y] * emit_p[y][obs[t]], y0) for y0 in states])
            # 记录最大概率
            V[t][y] = prob
            # 记录路径
            newpath[y] = path[state] + [y]

        # 不需要保留旧路径
        path = newpath

    print_dptable(V)
    (prob, state) = max([(V[len(obs) - 1][y], y) for y in states])
    return (prob, path[state])

def print_tagger(pathlist,sentence):

    tagger = []
    word_index = []
    for i in xrange(len(pathlist)):
        if pathlist[i] != '0':
            word_index.append(i)
        else:
            if len(word_index):
                tagger.append(word_index)
                word_index=[]
    for indexs in tagger:
        print sentence[indexs[0]:indexs[len(indexs)-1]+1],

def hmm_nerf_tagger(sentence):
    helper = Helper()
    sentence = sentence.replace(" ","").replace("\n","").replace("\r","")
    states = helper.get_states()
    observations = helper.get_observationsunicode(sentence.decode("utf-8"))
    start_probability = helper.load_start_pro()
    emission_probability = helper.load_emission_pro()
    transition_probability = helper.load_transition_pro()
    pro,pathlist = viterbi(observations,
                   states,
                   start_probability,
                   transition_probability,
                   emission_probability)

    print (pro,pathlist)
    print_tagger(pathlist,sentence.decode("utf-8"))
    print "\n"

if __name__ == '__main__':
    """
    nr人名456
    ns地名789
    nt机构团体123
    nz其他专名101112
    """

    # sentence = u'在天津，一家科技小巨人企业为近5万家企业提供云计算服务。'

    while True:
        sentence = raw_input("请输入句子：")
        hmm_nerf_tagger(sentence)



