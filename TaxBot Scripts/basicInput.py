from connect import getTokenLength
from langchainMain import sendMessage

#This is the start of testing. A simple send message print response tester.


if __name__ == "__main__":
    print('\n' * 1)
    response = sendMessage(previousMessages = None) #send a default introduction request
    print(response['messages'][-1])
    print()
    #Make an interface, short term solution
    print("Choose an option from below:")
    print('===================')
    print('[1]- Ask a question')
    print('[2]- Exit')
    userMenuAnswer = input("Enter your choice: ")

    #print all the stuff. Don't worry about format or anything. 
    while True:
        print()
        print("Type a question below")
        print()
        userQuestion = input("Q: ")
        if(userQuestion.lower() == 'x'):
            break
        print('A: ', end='\n' * 2)

        response = sendMessage(previousMessages = None, message = userQuestion) #send user question
        print(response['messages'][-1].content)