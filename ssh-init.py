
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
    if not os.path.exists('/root/.ssh/'):
        os.makedirs('/root/.ssh/')

    f = get(target)
    if f.status:
        contents = f.text.split('\n')
        FOUND = [False]*5
        for i in range(len(contents)):
            searchObj = re.search(r'^.*?RSAAuthentication.*$',contents[i])
            if searchObj:
                contents[i] = 'RSAAuthentication yes'
                FOUND[0] = True
                continue

            searchObj = re.search(r'^.*?PubkeyAuthentication.*$',contents[i])
            if searchObj:
                contents[i] = 'PubkeyAuthentication yes'
                FOUND[1] = True
                continue

            searchObj = re.search(r'^.*?AuthorizedKeysFile.*$',contents[i])
            if searchObj:
                contents[i] = 'AuthorizedKeysFile ~/.ssh/authorized_keys'
                FOUND[2] = True
                continue
            
            searchObj = re.search(r'^.*?PermitRootLogin.*$',contents[i])
            if searchObj:
                contents[i] = 'PermitRootLogin yes'
                FOUND[3] = True
                continue

            searchObj = re.search(r'^.*?MaxSessions.*$',contents[i])
            if searchObj:
                contents[i] = 'MaxSessions 50'
                FOUND[4] = True
                continue
        
        if not FOUND[0]:
            contents.append('RSAAuthentication yes')
        if not FOUND[1]:
            contents.append('PubkeyAuthentication yes')
        if not FOUND[2]:
            contents.append('AuthorizedKeysFile ~/.ssh/authorized_keys')
        if not FOUND[3]:
            contents.append('PermitRootLogin yes')
        if not FOUND[4]:
            contents.append('MaxSessions 50')
        

        final = ''
        for content in contents:
            final = final + content + '\n'
        
        s = save(target,final)
        if s.status:
            print('Done! Please input "service sshd reload" to valid.')
        else:
            print('error')
    else:
        print('error')


if __name__ == "__main__":
    main()