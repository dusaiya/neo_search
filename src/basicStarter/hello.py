# encoding: utf-8
from flask import Flask
app = Flask(__name__)
from flask import render_template

from neo4j.v1 import GraphDatabase,basic_auth
##必须按照如下写，即使是在 10.200.6.5 这台机器上
driver = GraphDatabase.driver("bolt://10.200.6.5:7687", auth=basic_auth("neo4j", "ictsoftware"))
neo_session = driver.session()

@app.route('/search')
@app.route('/search/<name>')
def search(name=None):
    print name
    return render_template('search.html', name=name)

if __name__ == '__main__':
    app.run()
