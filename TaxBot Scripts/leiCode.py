from pypdf import PdfReader
import json, os
from constants import getUploadFolder, getUserVariablesLeiJson

#supporting script for PDF processing by chatbot
#hard coded by line allows for changes in the document, but not to document design

#create a text file with all values labelled as well as possible
newTextLines = []

def getSSN(text):
    ssn = text.splitlines()[1]
    newTextLines.append("EmployeeSocialSecurityNumber: " + ssn)
    return ssn

def getEIN(text):
    returnText = text.splitlines()[2]
    newTextLines.append("EmployerIdentificationNumber: " + returnText)
    return returnText

def getYerAddress(text):
    returnText = text.splitlines()[3]
    newTextLines.append("EmployerName, EmployerAddress, EmployerZIPCode: " + returnText)
    return returnText

def getControlNum(text):
    returnText = text.splitlines()[4]
    newTextLines.append("ControlNumber: " + returnText)
    return returnText

def getFirstName(text):
    returnText = text.splitlines()[5].split(" ")[0]
    newTextLines.append("EmployeeFirstName: " + returnText)
    return returnText

def getInitial(text):
    try:
        initial = text.splitlines()[5].split(" ")[1]
        if(initial.length > 1):
            initial = '0'

        newTextLines.append("EmployeeInitial: " + initial)
        return initial
    except:
        return '0'

def getLastName(text):
    returnText = text.splitlines()[5].split(" ")[1]
    newTextLines.append("EmployeeLastName: " + returnText)
    return returnText

def getSuffName(text):
    suff = text.splitlines()[5].split(" ")[-1]
    if(suff.contains(".")):
        return suff
    suff = '0'
    newTextLines.append("Suffix: " + suff)
    return suff


def getCleanEmployeeAddress(text):
    try:
        addr_line = text.splitlines()[6]
        address = addr_line.split(",")[0].strip()
        newTextLines.append("EmployeeAddress: " + address)
        return address
    except:
        return ''

def getCleanEmployeeZIP(text):
    try:
        addr_line = text.splitlines()[6]
        zip = addr_line.split(",")[1].strip()[:5]
        newTextLines.append("EmployeeZIPCode: " + zip)
        return zip
    except:
        return ''

def getWTC(text):
    wtc = text.splitlines()[7].split(" ")[0]
    newTextLines.append("WagesTipsOtherCompensation: " + wtc)
    return wtc

def getFITW(text):
    fitw = text.splitlines()[7].split(" ")[1]
    newTextLines.append("FederalIncomeTaxWithheld: " + fitw)
    return fitw

def getSSW(text):
    ssw = text.splitlines()[8].split(" ")[0]
    newTextLines.append("SocialSecurityWages: " + ssw)
    return ssw

def getSSTW(text):
    sstw = text.splitlines()[8].split(" ")[1]
    newTextLines.append("SocialSecurityTaxWithheld: " + sstw)
    return sstw

def getMWT(text):
    mwt = text.splitlines()[9].split(" ")[0]
    newTextLines.append("MedicareWagesAndTips: " + mwt)
    return mwt

def getMTW(text):
    mtw = text.splitlines()[9].split(" ")[1]
    newTextLines.append("MedicareTaxWithheld: " + mtw)
    return mtw

def getSST(text):
    sst = text.splitlines()[10].split(" ")[0]
    newTextLines.append("SocialSecurityTips: " + sst)
    return sst

def getAT(text):
    at = text.splitlines()[10].split(" ")[1]
    newTextLines.append("AllocatedTips: " + at)
    return at

def getDCB(text):
    dcb = text.splitlines()[11]
    newTextLines.append("DependentCareBenefits: " + dcb)
    return dcb

def getNP(text):
    np = text.splitlines()[12].split(" ")[0]
    newTextLines.append("NonqualifiedPlans: " + np)
    return np

def get12a1(text):
    val = text.splitlines()[12].split(" ")[1]
    newTextLines.append("Box12aLeft: " + val)
    return val

def get12a2(text):
    val = text.splitlines()[12].split(" ")[2]
    newTextLines.append("Box12aRight: " + val)
    return val

def get12b1(text):
    val = text.splitlines()[13].split(" ")[0]
    newTextLines.append("Box12bLeft: " + val)
    return val

def get12b2(text):
    val = text.splitlines()[13].split(" ")[1]
    newTextLines.append("Box12bRight: " + val)
    return val

def get12c1(text):
    val = text.splitlines()[14].split(" ")[0]
    newTextLines.append("Box12cLeft: " + val)
    return val

def get12c2(text):
    val = text.splitlines()[14].split(" ")[1]
    newTextLines.append("Box12cRight: " + val)
    return val

def get12d1(text):
    val = text.splitlines()[15].split(" ")[0]
    newTextLines.append("Box12dLeft: " + val)
    return val

def get12d2(text):
    val = text.splitlines()[15].split(" ")[1]
    newTextLines.append("Box12dRight: " + val)
    return val

def getOther(text):
    other = text.splitlines()[16]
    newTextLines.append("Box14Other: " + other)
    return other

def getState(text):
    state = text.splitlines()[17].split(" ")[0]
    newTextLines.append("State: " + state)
    return state

def getESIDN(text):
    idn = text.splitlines()[17].split(" ")[1]
    newTextLines.append("EmployerStateIDNumber: " + idn)
    return idn

def getSWTE(text):
    val = text.splitlines()[19]
    newTextLines.append("StateWagesTipsEtc: " + val)
    return val

def getSIX(text):
    val = text.splitlines()[21]
    newTextLines.append("StateIncomeTax: " + val)
    return val

def getLWTE(text):
    val = text.splitlines()[23]
    newTextLines.append("LocalWagesTipsEtc: " + val)
    return val

def getLIT(text):
    val = text.splitlines()[25]
    newTextLines.append("LocalIncomeTax: " + val)
    return val


def getLN(text):
    val = text.splitlines()[27]
    newTextLines.append("LocalityName: " + val)
    return val

#write new text document with values labled with a header
def writeHeaders():
    output = ''
    for lines in newTextLines:
        output += lines + "\n"

    fileName = 'userDataLabeled.txt'
    filePath = os.path.join(getUploadFolder(), fileName)#from constants

    #open the output file and write all data
    with open(filePath, "w", encoding="utf-8") as file:
        file.write(output)

    return filePath

#write to target json file the given data
def write_to_json(data, file_path):
    with open(file_path, "w") as json_file:
        json.dump(data, json_file, indent=4)

#main method to strip and set all values. 
def main(file):
    UPLOAD_FOLDER = getUploadFolder()
    filepath = os.path.join(UPLOAD_FOLDER, file)
    reader = PdfReader(filepath)
    relevent_text = reader.pages[0].extract_text().split("Copy 1—For State, City, or Local Tax Department")[1]

    user_variables = {
        "EmployeeSocialSecurityNumber": getSSN(relevent_text).strip(),
        "EmployerIdentificationNumber": getEIN(relevent_text).strip(),
        "EmployerName": getYerAddress(relevent_text).split(",")[0].strip(),
        "EmployerAddress": getYerAddress(relevent_text).split(",")[1].strip(),  
        "EmployerZIPCode": getYerAddress(relevent_text).split(",")[2].strip(), 
        "ControlNumber": getControlNum(relevent_text).strip(),
        "EmployeeFirstName": getFirstName(relevent_text).strip(),
        "EmployeeInitial": getInitial(relevent_text).strip(),
        "EmployeeLastName": getLastName(relevent_text).strip(),
        "EmployeeAddress": getCleanEmployeeAddress(relevent_text),
        "EmployeeZIPCode": getCleanEmployeeZIP(relevent_text),
        "WagesTipsOtherCompensation": getWTC(relevent_text).strip(),
        "FederalIncomeTaxWithheld": (getFITW(relevent_text)),
        "SocialSecurityWages": getSSW(relevent_text).strip(),
        "SocialSecurityTaxWithheld": getSSTW(relevent_text).strip(),
        "MedicareWagesAndTips": getMWT(relevent_text).strip(),
        "MedicareTaxWithheld": getMTW(relevent_text).strip(),
        "SocialSecurityTips": getSST(relevent_text).strip(),
        "AllocatedTips": getAT(relevent_text).strip(),
        "DependentCareBenefits": getDCB(relevent_text).strip(),
        "NonqualifiedPlans": getNP(relevent_text).strip(),
        "Box12aLeft": (get12a1(relevent_text)),
        "Box12aRight": get12a2(relevent_text).strip(),
        "Box12bLeft": get12b1(relevent_text).strip(),
        "Box12bRight": get12b2(relevent_text).strip(),
        "Box12cLeft": get12c1(relevent_text).strip(),
        "Box12cRight": get12c2(relevent_text).strip(),
        "Box12dLeft": get12d1(relevent_text).strip(),
        "Box12dRight": get12d2(relevent_text).strip(),
        "Box13Checked": 'false',
        "Box14Other": (getOther(relevent_text)),
        "State": getState(relevent_text).strip(),
        "EmployerStateIDNumber": getESIDN(relevent_text).strip(),
        "StateWagesTipsEtc": getSWTE(relevent_text).strip(),
        "StateIncomeTax": getSIX(relevent_text).strip(),
        "LocalWagesTipsEtc": getLWTE(relevent_text).strip(),
        "LocalIncomeTax": getLIT(relevent_text).strip(),
        "LocalityName": getLN(relevent_text).strip(),
    }

    write_to_json(user_variables, getUserVariablesLeiJson())

#if you run this file, use example pdf to show operations.
if __name__ == "__main__":
    main("Sample2-fw2.pdf")