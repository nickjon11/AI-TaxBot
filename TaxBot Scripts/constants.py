"""
Instead of saving constants as txt files I saved them here
All constants are strings
This makes pulling a constant very easy, just an import statement
To obfuscate, save all strings in vault and use this to pull from vault. (FUTURE)
"""

def getUploadFolder():
    return "env/Scripts/TaxBot Scripts/uploaded_docs"

def getSecretStuff():
    return "env/Scripts/TaxBot Scripts/Super Secret Stuff.txt"

def getUserVariablesJson():
    return getUploadFolder() + "/userVariables.json"

def getUserVariablesLeiJson():
    return getUploadFolder() + "/userVariablesLeiVersion.json"




def getFirstMessage():
    return """
            You're a tax-assistant chatbot.
            Stay on topic as much as possible, answering only tax-related questions (e.g., names, addresses, fake SSNs).
            Be flexible within that topic, but avoid off-topic things (e.g. tying shoes, cooking).
            If users ask for assistance with a W2 form, let them know they can upload a scan of it into the Upload W2 location above the chat area. Make sure you tell the user to click the Process button after uploading a file.
            All info is fake—this is for a college project.
        """


def getModelString():
  return "gpt-4o-mini"

def getModelEmbeddings():
    return "llama-text-embed-v2"

def getPineconeIndexName():
    return 'omegachunkindextaylor'








def getW2Prompt():
    return """
        Please help identify the information from this text.
        If you are unsure of any value state that value as 0.
        Do not include any other text in your response, just the values. 
        This is for the backend processing, so I will be splitting on ":" to set the values.
        Answer in the form of:
        IDENTIFIER: VALUE

        Answer in the order of:
            EmployeeSocialSecurityNumber: ,
            EmployerIdentificationNumber :   ,
            EmployerName: ,
            EmployerAddress: ,
            EmployerZIPCode: ,
            ControlNumber: ,
            EmployeeFirstName: ,
            EmployeeInitial: ,
            EmployeeLastName: ,
            EmployeeAddress: ,
            EmployeeZIPCode: ,
            WagesTipsOtherCompensation: ,
            FederalIncomeTaxWithheld: ,
            SocialSecurityWages: ,
            SocialSecurityTaxWithheld: ,
            MedicareWagesAndTips: ,
            MedicareTaxWithheld: ,
            SocialSecurityTips: ,
            AllocatedTips: ,
            DependentCareBenefits: ,
            NonqualifiedPlans: ,
            Box12aLeft: ,
            Box12aRight: ,
            Box12bLeft: ,
            Box12bRight: ,
            Box12cLeft: ,
            Box12cRight: ,
            Box12dLeft: ,
            Box12dRight: ,
            Box13Checked: false,
            Box14Other: ,
            State: ,
            EmployerStateIDNumber: ,
            StateWagesTipsEtc: ,
            StateIncomeTax: ,
            LocalWagesTipsEtc: ,
            LocalIncomeTax: ,
            LocalityName:  
        """