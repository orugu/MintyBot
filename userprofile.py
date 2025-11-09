

class userprofile:
    username = ""
    id = 0
    level = 1
    def __init__(self):
        print("init")
        self.username=""
        self.id = 0
        #super().__init__()
        
    def __new__(self,name):
        self.name = name
        self.id = 1
        print("new user added")
        print("name: "+self.name)
        return super().__new__(self)
    
   # def __name__(self):
          
    def idreturn(self):
        
        return self.id
    
    def idinput(self,newid):
        self.id = newid
    
    def usernamereturn(self):
        return self.username
    
    def usernameinput(self,name):
        self.username = name

    def levelreturn(self):
        return self.level
    
    def increase_level(self,num):
        self.level +=num

    def initialize(self,name):
        self.__new__(name)

userdata = []
menu=input()
if menu == "1":
    print("계정 추가",end="")
    temp= input()
    userdata.append()

elif menu == "2":
    print(userdata)
