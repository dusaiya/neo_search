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
def dict2json(newDictOb):
    if newDictOb["label"] == "Douban":
        jsonNode = json.dumps({"id":newDictOb["neo_id"], 
                "name":newDictOb["name"], 
                "size":40, "category":0})
    elif newDictOb["label"] == "Weibo":
        jsonNode = json.dumps({"id":newDictOb["neo_id"], 
                "name":newDictOb["nick_name"], 
                "size":40, "category":1})
    return jsonNode


def neoob2dict(ob):
    '''
        将ob对象转换成dict对象
    '''
    newDictOb = dict(ob)
    labelsets = ob.labels()._SetView__items
    for nodelabel in labelsets:
        newDictOb["label"]= nodelabel.encode("utf-8")
        break ##只能有一个标签
    return newDictOb

@app.route('/search')
@app.route('/search/<nick_name>')
def search(nick_name=None):
    print nick_name
    nodelist=[]
    newDictList=[]
    rellist=[]
    ob=neo_graph.find_one("Douban", "name", nick_name)
    sourceDictOb=neoob2dict(ob)
    newDictList.append(sourceDictOb)
    nodelist.append(ob)
    for rel in neo_graph.match(start_node=ob):
        targetDictOb=neoob2dict(rel.end_node())
        newDictList.append(targetDictOb)
        nodelist.append(rel.end_node())
        myrel=json.dumps({"source":sourceDictOb["neo_id"],  "target":targetDictOb["neo_id"]  })
        rellist.append(myrel)
    jsonNodeList=[]
    for newDictOb in newDictList:
        jsonNode=dict2json(newDictOb)
        jsonNodeList.append(jsonNode)
    
    startNode=newDictList[0]
    endNode=newDictList[1]
    
    return render_template('search.html', nodeDataList=newDictList,
                           startNode=startNode,endNode=endNode,
                           jsonNode=jsonNode,jsonNodeList=jsonNodeList)

if __name__ == '__main__':
    app.debug = True
    app.run()
