# encoding: utf-8

from flask import Flask
app = Flask(__name__)
from flask import render_template
import json
from py2neo import Graph, Node, Relationship
neo_graph = Graph(
    "http://10.200.6.5:7474/db/data/", 
    username="neo4jTest", 
    password="ictsoftware"
)


def neoob2dict(ob):
    '''
        将ob对象转换成dict对象
    '''
    newDictOb = dict(ob)
    newDictOb["label"]= get_neo_label(ob)
    return newDictOb

def get_neo_label(ob):
    labelsets = ob.labels()._SetView__items
    for nodelabel in labelsets:
        labelstr= nodelabel.encode("utf-8")
        break
    return labelstr

def dict2json(newDictOb):
    '''
        neo节点转化成字典格式
    '''
    if newDictOb["label"] == "Douban":
        jsonNode = json.dumps({"id":newDictOb["neo_id"], 
                "name":newDictOb["name"], 
                "size":40, "category":1})
    elif newDictOb["label"] == "Weibo":
        jsonNode = json.dumps({"id":newDictOb["neo_id"], 
                "name":newDictOb["nick_name"], 
                "size":40, "category":2})
    elif newDictOb["label"] == "User":
        jsonNode = json.dumps({"id":newDictOb["neo_id"], 
                "name":newDictOb["neo_id"], 
                "size":80, "category":0})
    return jsonNode

@app.route('/search')
@app.route('/search/<nick_name>')
def search(nick_name=None):
    rellist=[]
    newDictList=[]
    jsonNodeList=[]
    ob=neo_graph.find_one("Douban", "name", nick_name)
    rootOb=None
    for rel1 in neo_graph.match(end_node=ob):
        if get_neo_label(rel1.start_node())=='User':
            rootOb=rel1.start_node()
    
    sourceDictOb=neoob2dict(rootOb)
    newDictList.append(sourceDictOb)
    jsonNodeList.append(dict2json(sourceDictOb))
    ##根据豆瓣作为source节点进行查找
    leafNodeList = neo_graph.match(start_node=rootOb)
    for rel1 in leafNodeList:
        targetDictOb=neoob2dict(rel1.end_node())
        newDictList.append(targetDictOb)
        jsonNodeList.append(dict2json(targetDictOb))
        relLabel=rel1._Relationship__type.__str__()
        myrel=json.dumps({"source":sourceDictOb["neo_id"],  "target":targetDictOb["neo_id"],
                          "label":{"normal":{"show":True,"formatter":relLabel}} })
        rellist.append(myrel)
    ##再将每个子节点
#     for rel2 in leafNodeList:
#         targetDictOb=neoob2dict(rel2.endNode())
#         if neo_graph.match(start_node=targetDictOb):
#         myrel=json.dumps({"source":targetDictOb["neo_id"],  "target":sourceDictOb["neo_id"]  })
#         rellist.append(myrel)
    
    return render_template('search.html', nodeDataList=newDictList,
                          jsonNodeList=jsonNodeList,rellist=rellist)

if __name__ == '__main__':
    app.debug = True
    app.run()
