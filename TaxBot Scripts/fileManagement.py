import os
import pypdf, pdfplumber, docx, json
import shutil
import gradio as gr
from langchainMain import sendSystemMessage
from leiCode import main, writeHeaders
from constants import *

#This manage file uploading and reading

UPLOAD_FOLDER = getUploadFolder()#from constants
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

#Triggers when users click process button
def process_file(document, prompt):
    analyze_with_gpt(document, prompt) #analyze document
    compareW2Values(document) #Ensure data accuracy
    updateUserInfo() #Tell the bot the info from the W2


#Save copy of file tp UPLOAD_FOLDER
def save_file(filepath):
    #name the file the same thing, overwrite existing
    filename = "userW2" + os.path.splitext(filepath)[1]
    save_path = os.path.join(UPLOAD_FOLDER, filename)

    # Open the file before using it in copyfileobj
    with open(filepath, "rb") as uploaded_file, open(save_path, "wb") as out_file:
        shutil.copyfileobj(uploaded_file, out_file)

    return save_path
    
# Read from many File Types, return string version of document
def read_file(file_obj):
    #if a file object was passed, save a copy, and run Lei's code
    try:
        file_path = file_obj.name
        save_file(file_path)
        main(file_path)
    #if a file path was passed, set the file path
    except:
        file_path=file_obj
    
    #if text file
    if file_path.endswith(".txt"):
        if(file_path != file_obj):#reruns always use txt files. The file_path=file_obj on reruns
            content = file_obj.read()
            return content.decode("utf-8") if isinstance(content, bytes) else content
        else: #on reruns, the file_path has to be openned since it is not a file_obj yet
            with open(file_path, "r", encoding="utf-8") as file:
                content = file.read()
                return content.decode("utf-8") if isinstance(content, bytes) else content
    
    #if pdf file use pypdf library
    elif file_path.endswith(".pdf"):
        with pdfplumber.open(file_path) as pdfFile:
            targetPage = pdfFile.pages[0]
            return targetPage.extract_text()
    
    #if docx file use docx library
    elif file_path.endswith(".docx"):
        doc = docx.Document(file_obj)
        return "\n".join([p.text for p in doc.paragraphs])
    
    #if not pdf, txt, or docx skip and say unsupported. Should be impossible.
    else:
        return "Unsupported File Type, Please upload .txt, .pdf, or .docx"

#Get the content from the document and send it to the bot. Write the response into a JSON file
def analyze_with_gpt(document, prompt):
    if isinstance(document, tuple): # Tuple is storing multiple items as a single variable
        document = document[0] #We only want the first in this case. 
    content = read_file(document)
    response = sendSystemMessage(f"{prompt}\n\n{content}") 
    writeW2Values(response['messages'][-1].content)

#Write from W2 PDF to userVariables.json
def writeW2Values(input):
    with open(getUserVariablesJson(), "r+", encoding='utf-8') as file: #from constants
        data = json.load(file)
        #write from input to data json object
        for line in input.splitlines():
            if ":" in line:
                key, value = line.split(":", 1)
                data[key.strip()] = value.replace(",", "").strip()
        
        #from the start of the file, overwrite all fields that exist in data with data's values. 
        file.seek(0)
        json.dump(data, file, indent=4)
        file.truncate() #Delete all fields not in data

#Delete PII of user
def clearW2Values():
    #clear userVariables.json
    with open(getUserVariablesJson(), "r+", encoding='utf-8') as file: #from constants
        data = json.load(file)

        for key in data:
            data[key] = ""

        file.seek(0)
        json.dump(data, file, indent=4)
        file.truncate()

    #delete Lei's code helper json
    if(os.path.exists(getUserVariablesLeiJson())):#from constants
        os.remove(getUserVariablesLeiJson())

    #delete w2 copy used for Lei's code
    userW2Path = os.path.join(getUploadFolder(), 'userW2.pdf')
    if(os.path.exists(userW2Path)):
        os.remove(userW2Path)

    #delete bot data pulled from W2
    userDataLabeled = os.path.join(getUploadFolder(), 'userDataLabeled.txt')
    if(os.path.exists(userDataLabeled)):
        os.remove(userDataLabeled)



#Compare bot response to expected values
def compareW2Values(document):
    failureKeys = [] #areas where the data does not match
    with open(getUserVariablesJson(), "r+", encoding='utf-8') as file:
        botData = json.load(file)
    with open(getUserVariablesLeiJson(), "r+", encoding='utf-8') as file:
        leiData = json.load(file)
        
    #compare the two data sets. Find keys that have none matching values
    for key in botData:
        if botData[key] != leiData[key]:
            failureKeys.append(key)

    #if a document was provided (not a rerun)
    if (document):        
        prompt = getW2Prompt()#from constants
        newDocument = writeHeaders() #create a new text document with labeled data to help the bot
        
        #Give the chatbot a second attempt
        analyze_with_gpt(newDocument, prompt)#this will overwrite to botData with the new data
        compareW2Values(None)#compare again
    #if the second attempt failed, just overwrite with hardcoded
    else:          
        #if any key failed
        if(failureKeys):
            print(" ".join(failureKeys))
            if not (len(failureKeys) == 1 and failureKeys == 'EmployeeInitial'):#other than EmployeeInitial
                #print all failure keys
                #overwrite AI data with data pulled from lines with hardcode
                print("Copying from Lei's Code")
                with open(getUserVariablesLeiJson(), "r+", encoding='utf-8') as file:
                    leiData = json.load(file)
                with open(getUserVariablesJson(), "w", encoding='utf-8') as file:
                     json.dump(leiData, file, indent=4)
            else:#If the middle initial is wrong, the bot still works fine. The IRS rarely sees this as an error.
                print('Middle Initial May be Wrong')

#Tell the bot to use the data in userVariables.json as PII
def updateUserInfo():
    prompt = """
    Update the user's personal information with the following information. The user is the Employee.

    """

    with open(getUserVariablesJson(), "r", encoding='utf-8') as file:
        data = json.load(file)

    if(data):
        prompt += json.dumps(data, indent=4)
    sendSystemMessage(prompt)


#Unused
def confirm_shutdown():
    return gr.update(visible=True)

#Unused
def cancel_shutdown():
    return gr.update(visible=False)

#Delete all PII, Stop the bot.
def shutdownfn():
    clearW2Values()
    print("Chatbot has been close, Please Restart Program")
    os._exit(0)

#testing
if __name__ == '__main__':
    filePath = getUploadFolder()
    filePath = os.path.join(filePath, 'Sample2-fw2.pdf')

    with pdfplumber.open(filePath) as pdfFile:
        targetPage = pdfFile.pages[0]
        txt = targetPage.extract_text()

    with open(os.path.join(getUploadFolder(), 'test.txt'), "w") as file_obj:
        file_obj.write(txt)