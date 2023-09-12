#author:hanshiqiang365

import pandas as pd
from pyecharts.charts import Graph
from pyecharts import options as opts
import jieba
import jieba.posseg as pseg


def process_data():
    with open("水浒传.txt", encoding='gb18030') as f:
        book = f.readlines()

    jieba.load_userdict("characters_list.txt")
    characters_data = pd.read_csv("characters_list.txt")

    mylist = [k[0].split(" ")[0] for k in characters_data.values.tolist()]
    tmpnames = []
    characters_names = {}
    characters_relationships = {}

    for b in book:
        b.replace("晁天王", "晁盖")
        b.replace("晁保正", "晁盖")
        b.replace("宋押司", "宋江")
        b.replace("宋头领", "宋江")
        b.replace("宋公明", "宋江")
        b.replace("黑旋风", "李逵")
        b.replace("武二郎", "武松")
        b.replace("武都头", "武松")
        b.replace("林教头", "林冲")
        b.replace("鲁提辖", "鲁达")
        b.replace("鲁智深", "鲁达")
        b.replace("花和尚", "鲁达")
        b.replace("青面兽", "杨志")
        b.replace("柴大官人", "柴进")
        b.replace("小李广", "花荣")
        b.replace("高太尉", "高俅")
        b.replace("一丈青", "扈三娘")
        b.replace("玉麒麟", "卢俊义")
        b.replace("入云龙", "公孙胜")
        b.replace("一清", "公孙胜")
        poss = pseg.cut(b)
        tmpnames.append([])
        for w in poss:
            if w.flag != 'nr' or len(w.word) != 2 or w.word not in mylist:
                continue
            tmpnames[-1].append(w.word)
            if characters_names.get(w.word) is None:
                characters_names[w.word] = 0
            characters_relationships[w.word] = {}
            characters_names[w.word] += 1

    #print(characters_relationships)
    #print(tmpnames)

    for name, times in characters_names.items():
        print(name, times)

    for name in tmpnames:
        for name1 in name:
            for name2 in name:
                if name1 == name2:
                    continue
                if characters_relationships[name1].get(name2) is None:
                    characters_relationships[name1][name2] = 1
                else:
                    characters_relationships[name1][name2] += 1

    #print(characters_relationships)

    with open("characters_relationship.csv", "w", encoding='utf-8') as f:
        f.write("Source,Target,Weight\n")
        for name, edges in characters_relationships.items():
            for v, w in edges.items():
                f.write(name + "," + v + "," + str(w) + "\n")

    with open("characters_namenode.csv", "w", encoding='utf-8') as f:
        f.write("ID,Label,Weight\n")
        for name, times in characters_names.items():
            f.write(name + "," + name + "," + str(times) + "\n")


def process_graph():
    characters_relationship_data = pd.read_csv('characters_relationship.csv')
    characters_namenode_data = pd.read_csv('characters_namenode.csv')
    characters_relationship_data_list = characters_relationship_data.values.tolist()
    characters_namenode_data_list = characters_namenode_data.values.tolist()

    nodes = []
    for node in characters_namenode_data_list:
        if node[0] == "宋江":
            node[2] = node[2]/2
        nodes.append({"name": node[0], "symbolSize": node[2]/30})

    links = []
    for link in characters_relationship_data_list:
        links.append({"source": link[0], "target": link[1], "value": link[2]})

    g = (
        Graph()
        .add("", nodes, links, repulsion=8000)
        .set_global_opts(title_opts=opts.TitleOpts(title="《水浒传》人物关系"))
    )
    return g


if __name__ == '__main__':
    process_data()
    g = process_graph()
    g.render()

