import os
import sys
import shlex
import xml.etree.ElementTree as ET
from subprocess import run, Popen, PIPE
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By




def mavenInstalledChecker():
    preBaseCommand = "echo 3 | "
    postBaseCommand = " >/dev/null 2>&1"
    if not os.path.exists("./apache-maven-3.8.6"):
        print("Downloading Maven")
        os.system(preBaseCommand + "wget https://dlcdn.apache.org/maven/maven-3/3.8.6/binaries/apache-maven-3.8.6-bin.tar.gz" + postBaseCommand)
        print("Extracting Maven")
        os.system(preBaseCommand + "tar -xvf apache-maven-3.8.6-bin.tar.gz" + postBaseCommand)

def getDepenciesUpdatable(path): 

    mavenInstalledChecker()
    mavenUrl = os.getcwd() + "/apache-maven-3.8.6/bin/mvn"
    unparsedDependecyVersion = run(shlex.split(mavenUrl + " versions:display-dependency-updates -f " + path), capture_output=True).stdout.decode('utf-8').splitlines()
    li = []
    count = -8
    while True:
        output = unparsedDependecyVersion[count].split(']')[1]
        if output.strip() == '':
            count -= 1
            continue
        if output[1] != '-':
            output = output.split(' ')
            dependecy, currentV, updateV = output[3], output[5], output[7]
            if not currentV[0].isalpha():
                li.append([dependecy, currentV, updateV])
            count -= 1
        else:
            break
    li.reverse()
    return li

def getDependencyTree(path):
    
    mavenInstalledChecker()

    mavenUrl = os.getcwd() + "/apache-maven-3.8.6/bin/mvn"
    # unparsedDependecyVersion = run(shlex.split(mavenUrl + " dependency:tree"), capture_output=True).stdout.decode('utf-8')
    unparsedDependecyVersion = run(shlex.split(mavenUrl + " dependency:tree -f " + path), capture_output=True).stdout.decode('utf-8').splitlines()
    li = []
    count = -7
    while True:
        output = unparsedDependecyVersion[count].split(']')[1]
        if output[1] != '-':
            counter = 0
            output = output.split(' ')
            lastSeen = ""
            for i in range(1, len(output), 2):
                lastSeen = output[i]
                counter += 1
            if lastSeen[0].isalpha():
                counter -= 1
            li.append([counter, output[-1]])
            count -= 1
        else:
            break
    li.reverse()
    for i in li:
        print(i)
    return li

def getUpdatedList(groupId,artifactId,vers):
    groupId = groupId.replace('.','/')
    driver.get("https://repo.maven.apache.org/maven2/"+groupId+"/"+artifactId+"/")
    meta= driver.find_element(By.LINK_TEXT,"maven-metadata.xml")
    meta.click()
    list=[]
    test = driver.find_elements(By.TAG_NAME,"span")
    for i in range(len(test)):
        if(test[i].text=="<version>"):
            version = test[i+1].text
            l=version.split('.')
            if(l[len(l)-1].isdigit()== True):
                if(version>vers):
                    list.append(version)
    driver.quit()
    
    return list

# def updatevers(l,fil):
#     tree = ET.parse(fil)
#     root = tree.getroot()
#     url = root.tag.split('}')[0] + '}'
#     for i in root:
#         print(i.tag)
#     for i in l:
#         print(root.findall(url + 'dependency'))
#         for dep in root.findall(".//" +url + 'dependency'):
#             print(dep)
#             if(dep.find('groupId').text == i[0][:i[0].find(':')] and dep.find('artifactId').text == i[0][(i[0].find(':')+1):]):
#                 print(1)
#                 if dep.find('version') not in root.iter('dependency'):
#                     version = ET.Element('version')
#                     root.append(version)
#                 else:
#                     dep.find('version').text = i[2]
#     tree.write("./pomUpdated.xml",encoding='UTF-8',xml_declaration=True)
def updatevers(l,fil):
    tree = ET.parse(fil)
    root = tree.getroot()
    url = root.tag.split('}')[0] + '}'
    ET.register_namespace('', "http://maven.apache.org/POM/4.0.0")
    ET.register_namespace('xsi', "http://www.w3.org/2001/XMLSchema-instance")
    for i in l:
        for dep in root.iter(url + 'dependency'):
            group = i[0][:i[0].find(':')] 
            art = i[0][(i[0].find(':')+1):]
            vers = i[2]
            if(dep.find(url + 'groupId')):
                if(dep.find(url + 'groupId').text == group):
                    if(dep.find(url + 'artifactId').text == art):
                        if(dep.find(url + 'version').text):
                            dep.find(url + 'version').text = vers
                        else:
                            version = ET.SubElement(dep, "version")
                            version.text = vers
        for plug in root.iter(url + 'plugin'):
            group = i[0][:i[0].find(':')] 
            art = i[0][(i[0].find(':')+1):]
            vers = i[2]
            if(plug.find(url + 'groupId')):
                if(plug.find(url + 'groupId').text == group):
                        if(plug.find(url + 'artifactId').text == art):
                            if(plug.find(url + 'version').text):
                                plug.find(url + 'version').text = vers
                            else:
                                version = ET.SubElement(dep, "version")
                                version.text = vers
                        
    tree.write("./pomUpdated.xml",encoding='UTF-8',xml_declaration=True)

def updatedVersionList(li):
    versionList = {}
    for i in li:
        getUpdatedList(li[0], li[1], li[2])
    
def updatedDependencyTree(path):
    updatevers(getDepenciesUpdatable(path), path)
    pathModified = 'pomUpdated.xml'
    print()
    getDependencyTree(pathModified)

# options = webdriver.ChromeOptions()
# options.accept_insecure_certs = True
# driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), chrome_options = options)
path = 'pom.xml'
# print(getUpdatedList("org.apache.httpcomponents","httpclient", "4.3.2"))
# print()
updatevers(getDepenciesUpdatable(), 'pom.xml')
updatedDependencyTree(path)
# getDependencyTree(path)