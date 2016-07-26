from django.forms import ValidationError

def validateResultFile(filefield):
    line = filefield.readline().strip('\n\r').split("\t")
    while(line):
        if(len(line) == 6):
            if not(testInt(line[0]) and testInt(line[3]) and testFloat(line[4])):
                raise ValidationError("Invalid results file. Should be delimited by tabs.")
        else:
            raise ValidationError("Invalid results file. Should be delimited by tabs.")
        line = filefield.readline().strip('\n\r').split("\t")
        if(line[0] == ''):
            break
    filefield.seek(0)



#301 0 CR93E-10505 0

def validateJudgementFile(filefield):
    line = filefield.readline().strip('\n\r').split(" ")
    while(line):
        if(len(line) == 4):
            if not(testInt(line[0]) and testInt(line[1]) and testInt(line[3])):
                raise ValidationError("Invalid judgement file. Should be delimited by spaces.")
        else:
            raise ValidationError("Invalid judgement file. Should be delimited by spaces.")
        line = filefield.readline().strip('\n\r').split(" ")
        if(line[0] == ''):
            break
    filefield.seek(0)


def testFloat(string):
    try:
        if(float(string) != 'NaN'):
            return True
        return False
    except:
        return False

def testInt(string):
    try:
        if(int(string) != 'NaN'):
            return True
        return False
    except:
        return False    



