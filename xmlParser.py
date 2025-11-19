import xml.etree.ElementTree as xml

class xmlParser:
    def __init__(self, path):
        pomFile = xml.parse(path)
        self.root = pomFile.getroot()

    def getDependecies(self):
        baseUrl = self.root.tag.split("}")[0] + '}'
        dependencies = self.root.findall(baseUrl + 'dependencies')
        return dependencies
    
    