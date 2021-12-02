partEmployeeList=[]
FullEmployeeList=[]

# employee class
class Employee:
    employeeCount=0
    # Constructor
    def __init__(self,id,name,department,salary):
        self.id=id
        self.name=name
        self.department=department
        self.salary=float(salary)
        self.isemployed=True
        self.balance=0
    #returns boolean value
    def isEmployed(self):
        return self.isemployed

class Full_Time(Employee):

    def __init__(self,id,name,department,salary):
        super().__init__(id,name,department,salary)
        
    def giveRaise(self,r=10):#default value assigned
        p=r/100
        self.salary+=p*self.salary
      



class Part_Time(Employee):
    def __init__(self,id,name,department,salary):
        super().__init__(id,name,department,salary)

    def giveRaise(self,r=5):#default value assigned
        self.salary+=(r/100)*self.salary
       
def pay():
    print("in pay")
    for emp in partEmployeeList:
        if(emp.isEmployed()): #checks if employed and then pays
            emp.balance=emp.salary
            print("paid")
    for emp in FullEmployeeList:
        if(emp.isEmployed()):
            emp.balance=emp.salary
            print("paid")
def fire(arg):
    print("in fire")
    for emp in FullEmployeeList:
        if(getattr(emp,'id')==arg): #fins the employee with id and changes status of isemployed
            print("matched")
            emp.isemployed=False
            print("Fired")
            break
        else:
            print("employee not found")
    for emp in partEmployeeList:
        if(getattr(emp,'id')==arg):
            print("matched")
            emp.isemployed=False
            print("Fired")
            break
        else:
            print("employee not found")
#parttime employees average salaery
def part_average_salary():
    sum_salary=0
    for emp in partEmployeeList: #Extractcs salaries of employees and average is caluclated
        sum_salary+=emp.salary
    part_average_salary=sum_salary/len(partEmployeeList)
    return part_average_salary
#Full time employees salary
def full_average_salary():
    sum_salary=0
    for emp in FullEmployeeList:
        sum_salary+=emp.salary
        print(sum_salary)
    full_average_salary=sum_salary/len(FullEmployeeList)
    return full_average_salary


def operations():
    command=""
    f=open("input.txt","r") #opening input.txt file in read mode
    for line in f:
        # print(line)
        words=line.split(" ")
        command=words[0]    #extracting the command
        if(command.lower()=="new"):
            values=words[1].strip().split(",")
            #checking if employee is partime and retains his data
            if(values[len(values)-1]=="P"):
                PartTime_Employee=Part_Time(values[0],values[1],values[2],float(values[3]))
                partEmployeeList.append(PartTime_Employee)
                employeeCount=len(partEmployeeList)+len(FullEmployeeList)
            # checking if employee is full time and retaining data
            if(values[len(values)-1]=="F"):
                FullTime_Employee=Full_Time(values[0],values[1],values[2],values[3])
                FullEmployeeList.append(FullTime_Employee)
                employeeCount=len(partEmployeeList)+len(FullEmployeeList)
        # raising the emp salary with respective id in the input file
        if(command.lower()=="raise"):
            values=words[1].strip().split(",")
            for emp in partEmployeeList:
                if(emp.id==values[0]):
                    emp.giveRaise()
                    break
            for emp in FullEmployeeList:
                if(emp.id==values[0]):
                    emp.giveRaise()
                    break
        #calls pay method if pay is there in input.txt
        if(command.lower()=="pay"):
            print("calling pay")
            pay()
            #calls fire method if pay is there in input.txt
        if(command.lower()=="fire"):
            arg=words[2]
            print("calling fire")
            fire(arg)
#ethodto write conent to output.txt file
def write_to_file():
    file=open("output.txt","w")#openeing file in write mode
    c=0
    for emp in partEmployeeList:
        if(emp.isEmployed()):
            s="EMP. " + emp.name + ", ID: "+ emp.id + ", Department: " + emp.department + ", Current Salary: " + str(emp.salary) + ", Pay earned to date: "+ str(emp.balance)+ ", Type: "+ "Part time"+"\n"
        else:
            s="EMP. " + emp.name + ", ID: "+ emp.id + ", Department: " + emp.department + ", Not Employed with the company" + ", Pay earned to date: "+ str(emp.balance) + ", Type: "+ "Part time"+"\n"
        c+=1
        file.write(s)#writing into file
        file.write("......\n")
    for emp in FullEmployeeList:
       if(emp.isEmployed()):
            s="EMP. " + emp.name + ", ID: "+ emp.id + ", Department: " + emp.department + ", Current Salary " + str(emp.salary)+ ", Pay earned to date: "+ str(emp.balance) + ", Type: "+ "Full time"+ "\n"
       else:
            s="EMP. " + emp.name + ", ID: "+ emp.id + ", Department: " + emp.department + ", Not Employed with the company"+ ", Pay earned to date: "+ str(emp.balance)+ ", Type: "+ "Full time" + "\n"
       c+=1
       file.write(s)
       file.write("......\n")
    file.write("Total no.of employees : " + str(c) + "\n")
    file.write("Average Salaries paid to Part Time employees is: "+ str(part_average_salary())+ "\n")
    file.write("Average Salaries paid to Full Time employees is: "+ str(full_average_salary())+ "\n")
    file.close() #closing the file

                    
operations()
write_to_file()


