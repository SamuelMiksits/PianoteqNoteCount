import os
import math

#returns a list of times in format [H, M, S] given a time in seconds
def returnTime(time):
    hoursWithRemainder = time/3600
    minutesWithRemainder = 60*(hoursWithRemainder - math.floor(hoursWithRemainder))
    hours = math.floor(hoursWithRemainder)
    minutes = math.floor(minutesWithRemainder)
    seconds = round(60*(minutesWithRemainder - math.floor(minutesWithRemainder))) #Round to remove float issues
    return [hours, minutes, seconds]

def main():
    yearList = os.listdir() #List of all years that exist in the MIDI archive
    monthList = os.listdir() #List of all months that exist, created on a "per archive year" basis
    sumNotes = 0 #Amount of notes played
    sumTime = 0 #Amount of time played
    for i in range(len(yearList)):

        if "." not in yearList[i]: #Looks for folders, and not items which contain "." (mitigation to ignore this file in search)
            monthList[i] = os.listdir(yearList[i])
            for j in range(len(monthList[i])):
                try: #If the *NIX way of path resolving does not work, try the Windows way
                    archivelist = os.listdir(yearList[i] + "/" + monthList[i][j])
                except:
                    archivelist = os.listdir(yearList[i] + "\\" + monthList[i][j]) 
                
                #Calculate the sum of notes and
                for k in range(len(archivelist)):
                    row = archivelist[k].split() #The file name split into a list, split by space

                    #Indices for the row:
                    # 0 - Date (YYYY-MM-DD)
                    # 1 - Time (HHMM)
                    # 2 - Day of the week: (Day), Ex: (Wednesday)
                    # 3 - How many notes
                    # 4 - The word "notes,"
                    # 5 - Duration of the file (in seconds)
                    # 6 - The word "seconds" followed by file extension (.mid)

                    sumNotes += int(row[3])
                    sumTime += float(row[5])

    timePlayedList = returnTime(sumTime)
    print("You've played for: " + str(timePlayedList[0]) + " hour(s), " + str(timePlayedList[1])\
          + " minute(s) and " + str(timePlayedList[2]) + " second(s), with " + str(sumNotes) + " notes! Wow!")

main();
