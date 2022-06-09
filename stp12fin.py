import easygui
import json
import pickle
import datetime
import os

#sets the date time module as a variable
date = datetime.date.today()

#easygui options
title1 = "Welcome to PPEC inventory"
bodyText1 = "Choose an option:"
choices = ["Create", "List batches", "View specified batch details", "View specified component details", "Quit"]

title2 = "Components"
bodyText2 = "Please enter the number components you wish to add to this batch"
compChoice = ["Winglet strut", "Door seal clamp", "rubberpin"]

title3 = "Type"
bodyText3 = "Please choose from the components"

title4 = "Size"
bodytext4 = "Please choose the size"
sizeChoices = ["10mm x 75mm", "12mm x 100mm", "16mm 150mm"]

title8 = "Batch Number"
bodytext8 = "Continue"

#batch class with attributes
class Batch:
    def __init__(self, BatchNo):
        self.BatchNo = BatchNo
        self.type = ""
        self.amount = 0
        self.size = ""
#component class with attributes
class Component:
    def __init__(self, status, serialNumber):
       self.status = status
       self.serialNumber = serialNumber

#checks if the batch imformation is correct
def correction(correct, BatchNo):
                if correct == True:
                    print(correct)
                    return
                else:
                    newbatch = Batch(BatchNo)
                    newbatch.amount = ""
                    newbatch.type = ""
                    newbatch.size = ""
                    newbatch.amount = easygui.integerbox(title2, bodyText2)
                    newbatch.type = easygui.multchoicebox(title2, bodyText2, compChoice)
                    newbatch.size = easygui.multchoicebox(title4, bodytext4, sizeChoices)

#main menu
def main():
    BatchNo = ""
    choice = ""
    #continues menu until quit is choosen
    while choice != "Quit":
        #easygui menu
        choice = easygui.buttonbox(bodyText1, title1, choices)
        #creates batch and component details
        if choice == "Create":
            with open('batchindex.json', 'r') as json_file:
                batchlist = json.load(json_file)
                print(type(batchlist))
                batches = batchlist["Used batches"]
                json_file.close()

            #if the list is empty it will create a batch number using the date variable and a counter
            if batches == []:
                idnum = 0
                idnum = idnum + 1

                #formats the datetime module with the counter to form a batch number
                BatchNo = date.strftime('%d%m%y') + str("{:0>3}".format('000') + str(idnum))
                newb = int(BatchNo[1:])
                nextb = newb
                BatchNo = str(nextb)
                batches.append(BatchNo)


            else:
                #if there is a batch present it will create and increment the batch number


                if BatchNo in batches:
                    samb = int(BatchNo[1:])
                    neb = samb + 1
                    BatchNo = date.strftime('%d%m%y') + str(neb)
                    batches.append(BatchNo)

            #writes teh list to a json used as a dictionery
            with open('batchindex.json', "w") as outfile:
                usedbatches = {"Used batches": batches}
                json.dump(usedbatches, outfile)
                outfile.close()

                easygui.msgbox(BatchNo, title8, bodytext8)
                newbatch = Batch(BatchNo)
                newbatch.amount = easygui.integerbox(title2, bodyText2)
                n = 0
                compout = ""

                #makes serial numbers
                while n < newbatch.amount:
                    n = n + 1
                    serialNumber = BatchNo + "-" + str("{:0>3}".format('000') + str(n))
                    status = "manufactured unfinished"
                    newcomp = Component(status,serialNumber)
                    compout = compout + newcomp.status + " " + BatchNo + newcomp.serialNumber + "\n"

                    #dumps each new component details into a seperate pickle file
                    m = open(str(newcomp.serialNumber) + '.pck', "wb")
                    pickle.dump(compout, m, pickle.HIGHEST_PROTOCOL)
                    m.close()


                newbatch.type = easygui.multchoicebox(title2, bodyText2, compChoice)
                newbatch.size = easygui.multchoicebox(title4, bodytext4, sizeChoices)
                correct = easygui.ynbox(msg='was this information correct?', choices=['Yes', 'No'])
                correction(correct, BatchNo)
                easygui.textbox(title='The batch is'+"\t"+str(newbatch.BatchNo),msg='\nthere are this many components:'+"\t"+str(newbatch.amount), text = '\nbatch type/types are:'+"\t" + str(newbatch.type)+'\t'+'\ncomponents size/sizes are:'+"\t"+str(newbatch.size)+'\t'+ "\ndate this batch was created:"+"\t"+ str(date)+
                '\nserial numbers are:\n' + (compout))

                #dumps each new batch into a seperate pickle file
                x = open(str(newbatch.BatchNo) + '.pck', "wb")
                pickle.dump(newbatch, x, pickle.HIGHEST_PROTOCOL)
                x.close()



        #lists all of the batches currently stored
        elif choice == "List batches":
            with open('batchindex.json', 'r') as json_file:
                list_of_batches = json.load(json_file)
                json_file.close()
            easygui.textbox(title='here is all the current batches present',text= str(list_of_batches))

        #selects a specific batch and views its details

        # reads the json for reference
        elif choice == "View specified batch details":
            with open('batchindex.json', 'r') as json_file:
                list_of_batches = json.load(json_file)
                json_file.close()
            old_batches = list_of_batches['Used batches']
            batch_choices = easygui.choicebox(title='batches present for choice', choices= old_batches)

            filename = batch_choices + ".pck"

            # if the file exists it will load
            if os.path.exists(filename):
                l = open(filename, "rb")
                file_contents = pickle.load(l)

                #displays batch information
                easygui.textbox(title='The batch is' + "\t" + str(file_contents.BatchNo),
                                msg='\nthere are this many components:' + "\t" + str(file_contents.amount),
                                text='\nbatch type/types are:' + "\t" + str(
                                    file_contents.type) + '\t' + '\ncomponents size/sizes are:' + "\t" + str(
                                    file_contents.size) + '\t' + "\ndate this batch was created:" + "\t" + str(date))
            else:
                return 0

        #selects a specific component and displays its status

        #reads the json for reference
        elif choice == "View specified component details":
            with open('batchindex.json', 'r') as json_file:
                list_of_batches = json.load(json_file)
                json_file.close()
            old_batches = list_of_batches['Used batches']
            batch_choices = easygui.choicebox(title='batches present for component choice', choices=old_batches)
            comp_file = batch_choices + ".pck"

            #if the file exists it will load
            if os.path.exists(comp_file):
                l = open(comp_file, "rb")
                file_contents = pickle.load(l)

                #displays batch and component information
                easygui.textbox(title='The batch is' + "\t" + str(file_contents.BatchNo),
                                msg='\nthere are this many components:' + "\t" + str(file_contents.amount),
                                text='\nbatch type/types are:' + "\t" + str(
                                    file_contents.type) + '\t' + '\ncomponents size/sizes are:' + "\t" + str(
                                    file_contents.size) + '\t' + "\ndate this batch was created:" + "\t" + str(date))
                userinput = easygui.enterbox(title='enter serial number to view status',msg='paste in serial number with .pck at the end')
                easygui.textbox(title=userinput,text = "unfinished" + "" "\ndate created" + "" + str(date))

            else:
                return 0


#if a json is not create this will write one
if __name__ == '__main__':
    batchindex = []
    usedbatches = {"Used batches": batchindex}
    if not os.path.exists('batchindex.json'):
       with open('batchindex.json', "w") as f:
        json.dump(usedbatches, f)
        f.close()


main()




