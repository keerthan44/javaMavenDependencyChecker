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

def getDepenciesUpdatable(path='pom.xml'): 

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

def getDependencyTree(path="pom.xml"):
    mavenInstalledChecker()

    mavenUrl = os.getcwd() + "/apache-maven-3.8.6/bin/mvn"
    print(mavenUrl + " dependency:tree -f " + path) 
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

def getUpdatedList(groupId,artifactId,vers, driver):
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
            if(dep.find(url + 'groupId').text == group):
                if(dep.find(url + 'artifactId').text == art):
                    if(dep.find(url + 'version').text):
                        dep.find(url + 'version').text = vers
                    else:
                        version = ET.SubElement(dep, "version")
                        version.text = vers
                        
    tree.write("./pomUpdated.xml",encoding='UTF-8',xml_declaration=True)

def updatedVersionList(li, driver):
    versionList = {}
    for i in li:
        groupId, artifactId = i[0].split(":")
        print("Processing " + groupId + " " + artifactId)
        versionList[i[0]] = getUpdatedList(groupId, artifactId, i[1], driver)
        print("Done")
    return versionList

def updatedDependencyTree():
    print(os.getcwd())
    updatevers(getDepenciesUpdatable(), 'pom.xml')
    pathModified = 'pomUpdated.xml'
    getDependencyTree(pathModified)

def breakingChanges():
    options = webdriver.ChromeOptions()
    options.accept_insecure_certs = True
    options.headless = True
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), chrome_options = options)
    versionDict = updatedVersionList(getDepenciesUpdatable(), driver)
    # versionDict = {'com.github.davidmoten:rtree': ['0.8.0.1', '0.8.0.2', '0.8.0.3', '0.8.0.4', '0.8.3', '0.8.4', '0.8.5', '0.8.6', '0.8.7', '0.9'], 'io.reactivex:rxjava': ['1.2.3', '1.2.4', '1.2.5', '1.2.6', '1.2.7', '1.2.9', '1.3.0', '1.3.1', '1.3.2', '1.3.3', '1.3.4', '1.3.5', '1.3.6', '1.3.7', '1.3.8'], 'junit:junit': ['4.2', '4.3', '4.3.1', '4.4', '4.5', '4.6', '4.7', '4.8', '4.8.1', '4.8.2', '4.9', '4.13', '4.13.1', '4.13.2']}
    for dependecy in versionDict:
        for version in reversed(versionDict[dependecy]):
            updatevers([[dependecy, "0os.remove(pathModified)", version]], 'pom.xml')
            mavenUrl = os.getcwd() + "/apache-maven-3.8.6/bin/mvn"
            # unparsedDependecyVersion = run(shlex.split(mavenUrl + " dependency:tree"), capture_output=True).stdout.decode('utf-8')
            unparsedDependecyVersion = run(shlex.split(mavenUrl + " clean install -f pomUpdated.xml"), capture_output=True).stdout.decode('utf-8').splitlines()
            os.remove("pomUpdated.xml")
            output = unparsedDependecyVersion[-5].split(']')[1]
            if output.strip() == "BUILD SUCCESS":
                versionDict[dependecy] = version
                break
    li = []
    for dependency in versionDict:
        print(dependecy)
        li.append([dependecy, "0", versionDict[dependency]])
    print(li)
    updatevers(li, "pom.xml")
    getDependencyTree('pomUpdated.xml')
    return li


# updatedVersionList(getDepenciesUpdatable(path), driver)
# print()
# getDependencyTree()
# getDepenciesUpdatable()
# getDependencyTree()
# updatedDependencyTree()
# getDependencyTree(path)
path = sys.argv[1]
os.chdir(path)
print(breakingChanges())
# line = -7
# while True:
#     li.append(output[line].spli