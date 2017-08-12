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
    ob=neo_graph.find_one("Weibo", "nick_name", nick_name)
    newDictOb=dict(ob)
    labels=ob.labels()._SetView__items #获取label集合
    return render_template('search.html', name=newDictOb,labels=labels)

if __name__ == '__main__':
    app.debug = True
    app.run()
