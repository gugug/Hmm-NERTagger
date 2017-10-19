# Hmm-NERTagger试验的整个流程
[toc]
## HMM五元组
HMM是一个五元组(O，Q，O0 ，A，B) ：
* O:{o1 ….ot } 是状态集合,  也称为观测序列；
* Q:{q1 …qv } 是一组输出结果，也称隐序列；
* aij =P(qj |qi ):  转移概率分布（隐状态）；
* bij =P(oj |qi ):  发射概率（隐状态表现为显状态的概率）；
* O0 是初始状态（隐状态）；
## HMM模型
应用于命名实体识别中：给定一个词的序列，找出最可能的标签序列（内外符号：[内]表示词属于命名实体，[外]表示不属于）

### 应用到语料例子
标注格式：456人名，789地名，123机构团体，101112其他专业名词，0非实体词  
新/0 年/0 前/0 夕/0 ，/0 国/0 家/0 主/0 席/0 习/4 近/5 平/6 通/0 过/0 中/1 国/2 国/2 际/2 广/2 播/2 电/2 台/3 、/0 中/1 央/2 人/2 民/2 广/2 播/2 电/2 台/3 、/0 中/1 央/2 电/2 视/2 台/3 ，/0 发/0 表/0 了/0 2/0 0/0 1/0 4/0 年/0 新/10 年/11 贺/11 词/12  
是不是有点不理解这个怎么来的呢？？？不急，往下看。

## 人民日报的语料长啥样子？？
下面是个例子:  
f为非实体词语， rn为人名， zn为机构团体  
新年前夕/f ，/f 国家主席/f 习近平/rn 通过/f 中国国际广播电台/zn 、/f 中央人民广播电台/zn 、/f 中央电视台/zn  
## 数据预处理
上面的是人民日报的标注好的语料，我们的这个试验是是使用hmm的方式做命名实体识别，采用了基于字的方式来做。传统的是基于词的方式来做。  
所以需要对字进行字级别的划分，很明显，为了表示每个字所属的词性，我们对一个词进行的前和尾进行了标记，如果是中间的字，就一直使用中间数来标记。  
1. 举个例子：  
国家主席/f 习近平/rn  
上面的 国家主席不是实体词，所以就全部标注为0  
习近平是实体名词，所以就用123来标注，前和尾的词用对应的数字标记，中间字都用中间数字标记。  
所以就长这样啦: 国/0 家/0 主/0 席/0 习/4 近/5 平/6  

同理，中国国际广播电台 ---> 中/1 国/2 国/2 际/2 广/2 播/2 电/2 台/3

2. 数据转换
于是就有了下面的东西啦：  
标注格式：456人名，789地名，123机构团体，101112其他专业名词，0非实体词  
数据格式转换后：  
新/0 年/0 前/0 夕/0 ，/0 国/0 家/0 主/0 席/0 习/4 近/5 平/6 通/0 过/0 中/1 国/2 国/2 际/2 广/2 播/2 电/2 台/3 、/0 中/1 央/2 人/2 民/2 广/2 播/2 电/2 台/3 、/0 中/1 央/2 电/2 视/2 台/3 

## 进行五元组的构建
### 隐状态 & 观察状态
观察序列是给定的字序列，隐藏状态是每个字对应的词性标注。
### 初始概率
初始概率就是直接统计语料的词频，统计结果保存在[IR/documents8-2/start_probability.txt](https://github.com/gugug/Hmm-NERTagger/blob/master/IR/documents8-2/start_probability.txt)  
统计词频就是直接计算每个词性出现的概率占总数的比例

### 转移概率
标记间的状态Tj→Ti转移概率可以通过如下公式求出:  
![转移概率计算公式](https://github.com/gugug/Hmm-NERTagger/blob/master/Screenshots/transtition.png)  
例：习/4 近/5 平/6  
P（5|4）=C（4，5）/C（4）计算的结果表示词性4转移到词性5的概率。  
计算结果保存在：[IR/documents8-2/transition_probability.txt](https://github.com/gugug/Hmm-NERTagger/blob/master/IR/documents8-2/transition_probability.txt)  

### 发射概率
每个状态（标记）随对应的符号（单字）的发射概率可由下式求出:  
![发射概率计算公式](https://github.com/gugug/Hmm-NERTagger/blob/master/Screenshots/emission.png)  
例：习/4 近/5 平/6  
P（习|4）=C（习，4）/C（4）计算结果表示4发射到"习"这个字的概率
计算结果保存在：[IR/documents8-2/emission_probability.txt](https://github.com/gugug/Hmm-NERTagger/blob/master/IR/documents8-2/emission_probability.txt)  

**其中符号C代表的是其括号内因子在语料库中的计数**

## 发射概率的时候需要初始化为0
```python
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
```
初始化他们的概率为0，其他发射概率的初始化需要对应着每个字，所以需要分割出一个一个字出来。这个提取是直接把预料中的字提取出来。  
字都保存在[IR/documents8-2/words.txt](https://github.com/gugug/Hmm-NERTagger/blob/master/IR/documents8-2/words.txt)  

## 进行维特比解码找最优路径
维特比算法就是求解HMM上的最短路径，也即是最大概率的算法  
![维特比](https://github.com/gugug/Hmm-NERTagger/blob/master/Screenshots/viterbi.png)  

## 试验中使用了nltk的工具来统计
