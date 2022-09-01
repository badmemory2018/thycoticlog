import json
import time
import requests
token = None
cachelist = list()
def getToken():
    url = "https://bgne.secretservercloud.com/oauth2/token"

    body = {
        'username': '????',
        'password': '???',
        'grant_type': 'password'
    }
    res = requests.post(url=url, data=body)
    token = json.loads(res.text).get('access_token')
    return token

def getLog(token)->list:
    headeres = {
        'Authorization': "Bearer "+token,
        'content-type':'application/json'
    }
    logurl = "https://bgne.secretservercloud.com/api/v2/diagnostics/system-logs?take=10"

    text = requests.get(url=logurl, headers=headeres).text
    js_content = json.loads(text)
    accessResult = js_content.get("success")
    if accessResult == True:
        return js_content.get('records') # [{}，{}]
    else:
        return False

def writeLog(content):
    with open ("/var/log/Thycotic/ThycoticSystem.log",'a') as f:
        try:
            f.write(json.dumps(content)+'\n')
        except Exception as e:
            f.write(e+'\n')

def run_1():
    global cachelist
    global token
    token = getToken()
    logs = getLog(token)
    for log in logs:
        writeLog(log)
        cachelist.append(log)

def run_2():
    global cachelist
    global token
    if len(cachelist) >= 50:
        cachelist.pop(0)
    logs = getLog(token)
    if logs:
        for log in logs:
            if log not in cachelist:
                cachelist.append()
                writeLog(log)
    else:
        token = getToken()


def run():
    while True:
        previousloglist = list()
        token = getToken()
        try:
            while True:
                if len(previousloglist) == 50:
                    previousloglist.pop(0)
                recordList = getLog(token)

                if recordList == False:
                    token = getToken()
                    continue
                for record in recordList:
                    if record in previousloglist:
                        continue
                    else:
                        writeLog(record)
                        previousloglist.append(record)
                time.sleep(5)
        except Exception as e:
            break

if __name__ == "__main__":
    run_1()
    print(token)
    while True:
        try:
            run_2()
        except Exception as e:
            writeLog(str(e))
            token = getToken()
            continue
