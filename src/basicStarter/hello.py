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

@app.route('/search')
@app.route('/search/<nick_name>')
def search(nick_name=None):
    print nick_name
    nodelist=[]
    myrel=None
    ob=neo_graph.find_one("Douban", "name", nick_name)
    print ob
    nodelist.append(ob)
    for rel in neo_graph.match(start_node=ob):
        nodelist.append(rel.end_node())
        myrel=rel
        break
    newDictList=[]
    jsonNodeList=[]
    for nodeNeo in nodelist:
        newDictOb=dict(nodeNeo)
        labelsets=nodeNeo.labels()._SetView__items
        for nodelabel in labelsets:
            newDictOb["label"]= nodelabel.encode("utf-8")
            break ##只能有一个标签
        newDictList.append(newDictOb)
        if newDictOb["label"]=="Douban":
            jsonNode=json.dumps({"id":newDictOb["neo_id"],
                                 "name":newDictOb["name"]  })
        else:
             jsonNode=json.dumps({"id":newDictOb["neo_id"],
                                 "name":newDictOb["nick_name"]  })
        jsonNodeList.append(jsonNode)
    
    startNode=newDictList[0]
    endNode=newDictList[1]
    jsonNode=json.dumps({"id":newDictList[0]["neo_id"],
                         "name":newDictList[0]["name"]  })
    jsonNodeList=[json.dumps({"id":newDictList[0]["neo_id"],
                         "name":newDictList[0]["name"]  }),
                            json.dumps({"id":newDictList[1]["neo_id"],
                         "name":newDictList[1]["nick_name"]  }) ] 
    
    return render_template('search.html', nodeDataList=newDictList,
                           startNode=startNode,endNode=endNode,
                           jsonNode=jsonNode,jsonNodeList=jsonNodeList)

if __name__ == '__main__':
    app.debug = True
    app.run()
