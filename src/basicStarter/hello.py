# encoding: utf-8

from flask import Flask
app = Flask(__name__)
from flask import render_template

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
    for nodeNeo in nodelist:
        newDictOb=dict(nodeNeo)
        labelsets=nodeNeo.labels()._SetView__items
        for  nodelabel in labelsets:
            newDictOb["label"]= nodelabel.encode("utf-8")
        newDictList.append(newDictOb)
    
    startNode=newDictList[0]
    endNode=newDictList[1]
    
    return render_template('search.html', nodeDataList=newDictList,
                           startNode=startNode,endNode=endNode)

if __name__ == '__main__':
    app.debug = True
    app.run()
