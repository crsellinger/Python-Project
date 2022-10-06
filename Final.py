#creates empty 2D array
def createSeats():
    rows = 10
    cols = 5
    array = []
    for row in range(rows):
        new_row = []
        for col in range(cols):
            new_row.append('0')
        array.append(new_row)
    return array

#Loops through array and counts nonempty seats, totals them according to seating cost matrix
def seatingCosts(someArray):
    total = 0
    someArrayLen = sum([len(i) for i in someArray])
    seatingCostMatrix = [[300, 200, 100, 200, 300] for row in range(len(someArray))]
    
    for i in range(len(someArray)):
        for j in range(int(someArrayLen/len(someArray))):
            if someArray[i][j] == 'X':
                total += seatingCostMatrix[i][j]
    
    print("Total Sales: $", total)

#Reads reservations file and marks seats taken into array
def loadReservations(fileName, someArray):
    file = open(fileName, 'r')
    for line in file:
        line = tuple(map(str, line.split(", ")))
        name, row, col, conf_num = line
        someArray[int(row)][int(col)] = 'X'
        #every odd index is row, every even index is col
    file.close()

def adminLogin(fileName, someArray):
    file = open(fileName, 'r')
    
    usernameList = []
    passwordList = []

    #reads admins file and puts usernames and passwords into 2 lists
    for line in file:
        line = tuple(map(str, line.split(", ")))
        username, password = line
        usernameList.append(username)
        passwordList.append(password.replace("\n", ""))
        #Have to get rid of new line char
    
    print("Enter Username: ")
    inputUsername = input()
    print("Enter Password: ")
    inputPassword = input()

    #checks username and password against known ones in admin file
    if inputUsername in usernameList:
        if inputPassword in passwordList:
            print("\nPrinting seating charts...")
            printSeats(someArray)
            seatingCosts(someArray)
            print("You are now Logged Out!\n")
        else:
            print("Username and/or password incorrect!\n")
    else:
        print("Username and/or password incorrect!\n")
        
    file.close()
    
#Options menu
def menu():
    print("Mizzou IT Airlines\n"
          "------------------------------\n"
          "1. Admin Login\n"
          "2. Make a Reservation\n"
          "3. Exit\n"
          "What would you like to do? ")

#Prints current plane seats
def printSeats(someArray):
    for row in someArray:
        print(row)

#Makes a reservation
def reservation(someArray):
    print("Enter first name: ")
    firstName = input()
    print("Enter last name: ")
    lastName = input()

    printSeats(someArray)

    print("What row would you like to sit in? ")
    row = int(input())
    print("What column would you like to sit in? ")
    col = int(input())

    #Does not error check outside of bounds
    while someArray[row][col] == 'X':
        print("\nSeat is already taken!\n")
        print("What row would you like to sit in? ")
        row = int(input())
        print("What column would you like to sit in? ")
        col = int(input())

    someArray[row][col] = 'X'

    writeReservations("reservation.txt", firstName, row, col, confirmationCode(firstName))

    print("\nConfirmation code: ", confirmationCode(firstName))
    
    return someArray

#Writes new reservation to reservations file
def writeReservations(fileName, firstName, row, col, confCode):
    file = open(fileName, 'a')

    #New string formatted to look like .txt file
    newLine = [firstName + ", ", str(row) + ", ", str(col) + ", ", confCode + "\n"]
    file.writelines(newLine)

    file.close()

#Takes two strings and merges every other char
def confirmationCode(firstName):
    str1 = "INFOTC1040"
    str2 = firstName
    code = ""

    x = 0
    y = 0
    while (x < len(str1) or y < len(str2)):
        #error check if x is still in bounds
        if x in range(len(str1)):
            code = code + str1[x]
            x += 1

        #error check if y is still in bounds
        if y in range(len(str2)):
            code = code + str2[y]
            y += 1

    return code
    
def main():
    #Matrix for seats
    seats = createSeats()
    
    #Opening reservation.txt, reading seat numbers,
    #and manipulating seats array according to reservation.txt
    loadReservations('reservation.txt', seats)
    
    menu()
    choice = int(input())
    while True:
        if choice < 1 or choice > 3:
            print("\nError: Not a choice!\n")
            menu()
            choice = int(input())

        #Admin Portal
        if choice == 1:
            print("\nAdministrator Login Portal\n"
                  "-------------------------------\n")
            adminLogin("admins.txt", seats)
            menu()
            choice = int(input())
        
        #Reservation
        if choice == 2:
            print("\nMake a Reservation\n"
                  "--------------------------------\n")
            seats = reservation(seats)
            print("\nSeats Map")
            printSeats(seats)
            print("Congratulations! Your flight is now booked!\n")
            menu()
            choice = int(input())

        #Close Application
        if choice == 3:
            print("Thank you for choosing Mizzou IT Airlines! Have a good day!")
            break

if __name__ == "__main__":
    main()
