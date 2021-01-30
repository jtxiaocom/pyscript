
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


def changeValue(items,rgx,content):
    FOUND = False
    for i in range(len(items)):
        searchObj = re.search(rgx,items[i])
        if searchObj:
            items[i] = content
            FOUND = True
            break
    if not FOUND:
        items.append(content)
    return items



import re
target = '/etc/ssh/sshd_config'
def main():
    if not os.path.exists('/root/.ssh/'):
        os.makedirs('/root/.ssh/')

    f = get(target)
    if f.status:
        contents = f.text.split('\n')
        contents = changeValue(contents,r'^.*?RSAAuthentication.*$','RSAAuthentication yes')
        contents = changeValue(contents,r'^.*?PubkeyAuthentication.*$','PubkeyAuthentication yes')
        contents = changeValue(contents,r'^.*?AuthorizedKeysFile.*$','AuthorizedKeysFile ~/.ssh/authorized_keys')
        contents = changeValue(contents,r'^.*?PermitRootLogin.*$','PermitRootLogin yes')
        contents = changeValue(contents,r'^.*?MaxSessions.*$','MaxSessions 50')
        contents = changeValue(contents,r'^.*?ClientAliveInterval.*$','ClientAliveInterval 60')
        contents = changeValue(contents,r'^.*?ClientAliveCountMax.*$','ClientAliveCountMax 10')

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