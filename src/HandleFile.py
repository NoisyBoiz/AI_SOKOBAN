import json
from os import getcwd
from os.path import join

def readFile(path):
    string = ""
    f = open(join(getcwd(),"src", path),'r',encoding = 'utf-8')
    for i in f.readlines():
        string += i
    f.close()
    result = json.loads(string)
    return result

def saveFile(path,data):
    save = open(join(getcwd(),"src", path),'w',encoding = 'utf-8')
    save.write(json.dumps(data))
    save.close()
