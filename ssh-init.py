
import sys
import os
import codecs
class rt: #return
    status = False
    text = ''
    msg = ''
    def __init__(self,status=False,text=''):
        self.status = status
        self.text = text

def get(filePath):
    r = rt()
    try:
        with codecs.open(filePath, 'r', 'utf-8') as f:
            r.text = f.read()
    except FileNotFoundError as err:
        msg = "FileNotFoundError: "+ str(err)
        print(msg)
        r.msg = msg
        r.status = False
    except:
        msg = "Unexpected error: "+ str(sys.exc_info()[0])
        print(msg)
        r.msg = msg
        r.status = False
    else:
        r.status = True
    return r

def save(filePath,content):
    r = rt()
    dirname = os.path.dirname(filePath)
    if not os.path.exists(dirname):
        os.makedirs(dirname)
    try:
        with codecs.open(filePath, 'w', 'utf-8', errors='strict') as f:
            f.write(content)
    except:
        print("Unexpected error:", sys.exc_info()[0])
        r.status = False
        r.msg = sys.exc_info()[0]
    else:
        r.status = True
    return r




import re

def main():
    f = get('/etc/ssh/sshd_config')
    if f.status:
        print(f.text)
        contents = f.text.split('\n')
        for content in contents:
            searchObj = re.search(r'^.*?RSAAuthentication.*$',content)
            if searchObj:
                print(content)


if __name__ == "__main__":
    main()