import subprocess
from django.conf import settings
import os

def invoke(qrels, results):
    args = (os.path.normpath(settings.BASE_DIR + '/treco/trec_eval'), qrels, results)
    popen = subprocess.Popen(args, stdout=subprocess.PIPE)
    popen.wait()
    return popen.stdout.read()


def getResults(output):
    lines = output.split('\n')
    map = -1
    P10 = -1
    P20 = -1
    for num in range(0, len(lines)):
        linedata = lines[num].replace(' ','').split('\t')
        if(linedata[0] == 'map'):
            map = linedata[2]
            if not testFloat(map):
                map = -1
                break
        elif(linedata[0] == 'P_10'):
            P10 = linedata[2]
            if not testFloat(P10):
                P10 = -1
                break
        elif(linedata[0] == 'P_20'):
            P20 = linedata[2]
            if not testFloat(P20):
                P20 = -1
                break
    if(map != -1 and P10 != -1 and P20 != -1):
        return {"map": map, "P_10": P10, "P_20": P20}
    else:
        return {}

def testFloat(string):
    try:
        if(float(string) != 'NaN'):
            return True
        return False
    except:
        return False