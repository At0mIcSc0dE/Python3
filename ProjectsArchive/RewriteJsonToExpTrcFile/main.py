import json


with open("D:\\dev\\ProgramFiles\\ExpTrc\\Data.json", "r") as file:
    data = json.load(file)


def ReadWriteExp(expense: str, filename: str):
    for i in range(data["General"]["expID"]["0"][expense]):
        with open("D:\\dev\\ProgramFiles\\ExpTrc\\" + filename + ".exptrc", "a+") as file:
            file.write("#" + str(i + 1) + "\n")
            file.write(str(data[expense]["0"]
                           [str(i + 1)]["expName"]) + '\n')
            file.write(str(data[expense]["0"]
                           [str(i + 1)]["expPrice"]) + '\n')

            if(data[expense]["0"][str(i + 1)]["expInfo"] == ""):
                file.write("NULL" + '\n')
            else:
                file.write(str(data[expense]["0"]
                               [str(i + 1)]["expInfo"]) + "\n")

            file.write(str(data[expense]["0"]
                           [str(i + 1)]["expDay"]) + "\n")
            file.write(str(data[expense]["0"]
                           [str(i + 1)]["expMonth"]) + "\n")
            file.write(str(data[expense]["0"]
                           [str(i + 1)]["expYear"]) + "\n")


def ReadWriteGeneral():
    with open("D:\\dev\\ProgramFiles\\ExpTrc\\General.exptrc", "a+") as file:
        file.write(str(data["General"]["expID"]["0"]["OneTimeExpense"]) + '\n')
        file.write(str(data["General"]["expID"]["0"]["MonthlyExpense"]) + '\n')
        file.write(str(data["General"]["expID"]["0"]["OneTimeTakings"]) + '\n')
        file.write(str(data["General"]["expID"]["0"]["MonthlyTakings"]) + '\n')
        file.write(str(data["General"]["userID"]) + '\n')
        file.write(str(data["General"]["groupID"]) + '\n')
        file.write(str(data["General"]["0"]["BankBalance"]) + '\n')


ReadWriteExp("OneTimeExpense", "OneTimeExpenses")
ReadWriteExp("MonthlyExpense", "MonthlyExpenses")
ReadWriteExp("OneTimeTakings", "OneTimeTakings")
ReadWriteExp("MonthlyTakings", "MonthlyTakings")

ReadWriteGeneral()
