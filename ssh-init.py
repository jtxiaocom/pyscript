
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

target = '/etc/ssh/sshd_config'

def main():
    f = get(target)
    if f.status:
        contents = f.text.split('\n')
        print(contents)
        for i in range(len(contents)):
            searchObj = re.search(r'^.*?RSAAuthentication.*$',contents[i])
            if searchObj:
                print('get it 1')
                contents[i] = 'RSAAuthentication yes'
                continue

            searchObj = re.search(r'^.*?PubkeyAuthentication.*$',contents[i])
            if searchObj:
                print('get it 2')
                contents[i] = 'PubkeyAuthentication yes'
                continue

            searchObj = re.search(r'^.*?AuthorizedKeysFile.*$',contents[i])
            if searchObj:
                print('get it 3')
                contents[i] = 'AuthorizedKeysFile ~/.ssh/authorized_keys'
                continue
            
            searchObj = re.search(r'^.*?PermitRootLogin.*$',contents[i])
            if searchObj:
                print('get it 4')
                contents[i] = 'PermitRootLogin yes'
                continue

            searchObj = re.search(r'^.*MaxSessions.*$',contents[i])
            if searchObj:
                contents[i] = 'MaxSessions 50'
                print('get it 5')
                continue

        final = ''
        for content in contents:
            final = final + content + '\n'
        
        print(final)
        s = save(target,final)
        if s.status:
            print('Done! Please input "service sshd reload" to valid.')
        else:
            print('error')
    else:
        print('error')


if __name__ == "__main__":
    main()