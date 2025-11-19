from flask import Flask, jsonify, request
import json

import xml.etree.ElementTree as ET
import updateDependeciesAndBreakingChanges
app = Flask(__name__)

path = ''
@app.route('/process', methods=['POST'])
def process():
    print(request)
    if(request.method == "POST"):
        tup = []
        diction = {}
        global path
        path = request.form['nm']
        updateDependeciesAndBreakingChanges.pathchanger(path)
        pd_list = updateDependeciesAndBreakingChanges.getDepenciesUpdatable()

        def func(x):
            return {0: x[0], 1: x[1], 2: x[2]}
        # pd_list = [['org.web3j:core', '3.6.0', '5.0.0'], ['junit:junit', '4.12', '4.13.2'], [
        #     'ch.qos.logback:logback-classic', '1.2.3', '1.4.4']]
        tup = list(map(func, pd_list))
        diction = {i: tup[i] for i in range(0, len(tup))}
        print(diction)
        return diction


@app.route('/trdpd1', methods=["GET"])
def trdpd1():
    
    tup = []
    diction = {}

    updateDependeciesAndBreakingChanges.pathchanger(path)
    pd_list = updateDependeciesAndBreakingChanges.getDependencyTree()
    def func(x):
        return {0: x[0], 1: x[1]}
    # pd_list = [[0, 'kms-api-examples:kms-api-examples:jar:0.0.1-SNAPSHOT'],
    #     [1, 'org.apache.httpcomponents:httpclient:jar:4.3.2:compile'],
    #     [2, 'org.apache.httpcomponents:httpcore:jar:4.3.1:compile'],
    #     [2, 'commons-logging:commons-logging:jar:1.1.3:compile'],
    #     [2, 'commons-codec:commons-codec:jar:1.6:compile'],
    #     [1, 'org.apache.httpcomponents:httpclient-cache:jar:4.3.2:compile'],
    #     [1, 'org.apache.httpcomponents:httpmime:jar:4.3.2:compile'],
    #     [1, 'com.fasterxml.jackson.core:jackson-core:jar:2.4.0:compile'],
    #     [1, 'com.fasterxml.jackson.core:jackson-databind:jar:2.4.0:compile'],
    #     [2, 'com.fasterxml.jackson.core:jackson-annotations:jar:2.4.0:compile']]
    
    # return jsonify(pd_list)
    tup = list(map(func, pd_list))
    diction= {i: tup[i] for i in range(0, len(tup))}

    # print(diction)
    return diction

@app.route('/latest', methods=["GET"])
def trdpd2():
    updateDependeciesAndBreakingChanges.pathchanger(path)
    updateDependeciesAndBreakingChanges.updatevers(updateDependeciesAndBreakingChanges.getDepenciesUpdatable(), "pom.xml")
    pd_list = updateDependeciesAndBreakingChanges.getDependencyTree("pomUpdated.xml")
    tup = []
    diction = {}

    def func(x):
        return {0: x[0], 1: x[1]}


    # pd_list = [
    # [0, 'kms-api-examples:kms-api-examples:jar:0.0.1-SNAPSHOT'],
    # [1, 'org.apache.httpcomponents:httpclient:jar:4.5.13:compile'],
    # [2, 'org.apache.httpcomponents:httpcore:jar:4.4.13:compile'],
    # [2, 'commons-logging:commons-logging:jar:1.2:compile'],
    # [2, 'commons-codec:commons-codec:jar:1.11:compile'],
    # [1, 'org.apache.httpcomponents:httpclient-cache:jar:4.5.13:compile'],
    # [1, 'org.apache.httpcomponents:httpmime:jar:4.5.13:compile'],
    # [1, 'com.fasterxml.jackson.core:jackson-core:jar:2.14.0:compile'],
    # [1, 'com.fasterxml.jackson.core:jackson-databind:jar:2.14.0:compile'],
    # [2, 'com.fasterxml.jackson.core:jackson-annotations:jar:2.14.0:compile']
    # ]
    # return jsonify(pd_list)
    tup = list(map(func, pd_list))
    diction= {i: tup[i] for i in range(0, len(tup))}

    # print(diction)
    return diction

@app.route('/brkn', methods=["GET"])
def brkn():
    
    updateDependeciesAndBreakingChanges.pathchanger(path)
    pd_list = updateDependeciesAndBreakingChanges.breakingChanges()
    print(pd_list)
    tup = []
    diction = {}

    def func(x):
        return {0: x[0], 1: x[2]}



    # pd_list = [
    # [0, 'kms-api-examples:kms-api-examples:jar:0.0.1-SNAPSHOT'],
    # [1, 'org.apache.httpcomponents:httpclient:jar:4.5.13:compile'],
    # [2, 'org.apache.httpcomponents:httpcore:jar:4.4.13:compile'],
    # [2, 'commons-logging:commons-logging:jar:1.2:compile'],
    # [2, 'commons-codec:commons-codec:jar:1.11:compile'],
    # [1, 'org.apache.httpcomponents:httpclient-cache:jar:4.5.13:compile'],
    # [1, 'org.apache.httpcomponents:httpmime:jar:4.5.13:compile'],
    # [1, 'com.fasterxml.jackson.core:jackson-core:jar:2.14.0:compile'],
    # [1, 'com.fasterxml.jackson.core:jackson-databind:jar:2.14.0:compile'],
    # [2, 'com.fasterxml.jackson.core:jackson-annotations:jar:2.14.0:compile']
    # ]
    # return jsonify(pd_list)
    tup = list(map(func, pd_list))
    diction= {i: tup[i] for i in range(0, len(tup))}

    # print(diction)
    return diction


@ app.route("/")
def hello():
    print("Hello")
    return "hello"



if __name__ == "__main__":
    app.run(debug=True)