import os
import re
import pandas as pd

class Whatsapp:
    
    def __init__(self):
        pass
       
    def prepareCSV(self,chatFileName,inviteFlag=True,emptyLinesFlag=True,userLeftFlag=True):
        self.chatFileName = chatFileName
        self.inviteFlag = inviteFlag
        self.emptyLinesFlag = emptyLinesFlag
        self.userLeftFlag = userLeftFlag

        self.msg = self.read_file()

        if self.inviteFlag:
            self.msg = self.removeJoinInvites()
        
        if self.emptyLinesFlag:
            self.msg = self.removeEmptyLines()

             
        if self.userLeftFlag:
            self.msg = self.removeUserLeftMessages()
 

        self.msg = self.groupMsgbyDate()
        self.time = self.getTimefromChat()
        self.date = self.getDatefromChat()
        self.name = self.getUserNamefromChat()
        self.content = self.getContentfromChat()

        self.df = pd.DataFrame(list(zip(self.date, self.time, self.name, self.content)), columns = ['Date', 'Time', 'Name', 'Content'])
        self.df = self.df[self.df["Content"]!='Missing Text']
        self.df.reset_index(inplace=True, drop=True)

        self.df['DateTime'] = pd.to_datetime(self.df['Date'] + ' ' + self.df['Time'])
        self.df['Day of Week'] = self.df['DateTime'].apply(lambda x: x.day_name()) 
        self.df['Letter_Count'] = self.df['Content'].apply(lambda s : len(s))
        self.df['Word_Count'] = self.df['Content'].apply(lambda s : len(s.split(' ')))
        self.df['Hour'] = self.df['Time'].apply(lambda x : x.split(':')[0]) 

        self.write_file()

        return "CSV Prepared - File name : - " + self.csvFileName



    def removeJoinInvites(self):
        chat_removed_joinInvites = [line for line in self.msg if not "joined using this" in line]
        return chat_removed_joinInvites
    
    def removeEmptyLines(self):
        chat_removed_emptyLines = [line for line in self.msg if len(line) > 1]
        return chat_removed_emptyLines

    def removeUserLeftMessages(self):
        chat_removed_userLeftMsges = [line for line in self.msg if not line.endswith("left")]
        return chat_removed_userLeftMsges
        
    def groupMsgbyDate(self):
        msg_list = [] 
        pos = 0
        for line in self.msg:
            if re.findall("\A\d+[/]", line):
                msg_list.append(line)
                pos += 1
            else:
                take = msg_list[pos-1] + ". " + line
                msg_list.append(take)
                msg_list.pop(pos-1)

        return msg_list


    def getTimefromChat(self):
        time = [self.msg[i].split(',')[1].split('-')[0] for i in range(len(self.msg))]
        time = [s.strip(' ') for s in time] 
        return time

    def getDatefromChat(self):
        date = [self.msg[i].split(',')[0] for i in range(len(self.msg))]
        return date

    def getUserNamefromChat(self):
        name = [self.msg[i].split('-')[1].split(':')[0] for i in range(len(self.msg))]
        return name

    def getContentfromChat(self):
        content = []
        for i in range(len(self.msg)):
            try:
                content.append(self.msg[i].split(':')[2])
            except IndexError:
                content.append('Missing Text')
        return content


    def read_file(self):
        
        try:
            self.path = os.path.join(os.getcwd(),self.chatFileName)
            x = open(self.path,'r', encoding = 'utf-8') 
            y = x.read() 
            content = y.splitlines() 
            return content
        except:
            print("File read error")

    def write_file(self):
        self.csvFileName = self.chatFileName.split('.')[0]+'.csv'
        try:
            self.path = os.path.join(os.getcwd(),self.csvFileName)
            self.df.to_csv(self.path) 
        except:
            print("File write error")
    

a = Whatsapp()
chatCSV = a.prepareCSV('WhatsApp Chat with family.txt',True)
print(chatCSV)