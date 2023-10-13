import os
import math
import mido

# Returns a list of times in format [H, M, S] given a time in seconds
def returnTime(time):
    hoursWithRemainder = time/3600
    minutesWithRemainder = 60*(hoursWithRemainder - math.floor(hoursWithRemainder))
    hours = math.floor(hoursWithRemainder)
    minutes = math.floor(minutesWithRemainder)
    seconds = round(60*(minutesWithRemainder - math.floor(minutesWithRemainder))) # Round to remove float issues
    return [hours, minutes, seconds]

# Takes a midi file as an input, and returns a list of keys pressed
def parseMidiFile(mid):
    keyList = initializeList()
    
    for msg in mid:
        if msg.type == "note_on":
            keyListIndex = msg.note
            
            # Conversion between midi value and note:
            # MIDI = note + 20
            # BUT, the list is "0-indexed", meaning that
            # A0 is note 1 but index 0 in the list!
            keyListIndex -= 21 
            keyList[keyListIndex][1] += 1

    return keyList


def initializeList():
    keyList = list()

    keys = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
    octaves = ["0", "1", "2", "3", "4", "5", "6", "7"] # Notes from A0->C8, strategy here is to create a list with
                                                       # C0->B8, then remove C0->G#0, and then add C8
    for octave in octaves:
        for key in keys:
            keyList.append([key + octave, 0]) # signature
    
    for i in range(9): #Remove the first element 9 times in a row, eg, C0->G#0
        keyList.pop(0)

    keyList.append(["C8", 0])
    return keyList

# Adds all of the keypresses from tmpKeyList to keyList
def addKeyLists(keyList, tmpKeyList):
    for i in range(len(keyList)):
        keyList[i][1] = keyList[i][1] + tmpKeyList[i][1]
    return keyList

# Prints the final key list
def printKeyList(keyList):
    print("Breakdown of how many times each key was played: ")

    for i in range(10*12):
        print("-", end="")
    print()

    print("| {:>8} | {:<10}| {:<10}| {:<10}| {:<10}| {:<10}| {:<10}| {:<10}| {:<10}| {:<10}|".\
          format("Octave","0", "1", "2", "3", "4", "5", "6", "7", "8"))
    for i in range(10*12):
        print("-", end="")
    print()

    #for i in range(len(keyList)):
    #    keyList[i][1] = i*1000000

    keys = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
    for i in range(12):
        
        #Handle special cases separetly (A0->B0 and C8 causes issues)
        if i == 0:
            print("|{:>9} | {:<10}| {:<10}| {:<10}| {:<10}| {:<10}| {:<10}| {:<10}| {:<10}| {:<10}|".format(keys[i],\
            "---", str(keyList[i+3][1]), str(keyList[i + 3 + 12][1]), str(keyList[i + 3 + 24][1]),\
            str(keyList[i + 3 + 36][1]), str(keyList[i + 3 + 48][1]), str(keyList[i + 3 + 60][1]),\
            str(keyList[i + 3 + 72][1]), str(keyList[i + 3 + 84][1])))
        elif i >= 9:
            print("|{:>9} | {:<10}| {:<10}| {:<10}| {:<10}| {:<10}| {:<10}| {:<10}| {:<10}| {:<10}|".format(keys[i],\
            str(keyList[i-9][1]), str(keyList[i+3][1]), str(keyList[i + 3 + 12][1]), str(keyList[i + 3 + 24][1]),\
            str(keyList[i + 3 + 36][1]), str(keyList[i + 3 + 48][1]), str(keyList[i + 3 + 60][1]),\
            str(keyList[i + 3 + 72][1]), "---"))
        else:
            print("|{:>9} | {:<10}| {:<10}| {:<10}| {:<10}| {:<10}| {:<10}| {:<10}| {:<10}| {:<10}|".format(keys[i],\
            "---", str(keyList[i+3][1]), str(keyList[i + 3 + 12][1]), str(keyList[i + 3 + 24][1]),\
            str(keyList[i + 3 + 36][1]), str(keyList[i + 3 + 48][1]), str(keyList[i + 3 + 60][1]),\
            str(keyList[i + 3 + 72][1]), "---"))

    for i in range(10*12):
        print("-", end="")
    print()

    # Print least used key and most used key:
    indexLeastUsed = 0
    indexMostUsed = 0

    for i in range(len(keyList)):
        if keyList[i][1] < keyList[indexLeastUsed][1]:
            indexLeastUsed = i
        if keyList[i][1] > keyList[indexMostUsed][1]:
            indexMostUsed = i

    print("Least used key: " + keyList[indexLeastUsed][0] + " with " + str(keyList[indexLeastUsed][1]) + " presses")
    print("Most used key: " + keyList[indexMostUsed][0] + " with " + str(keyList[indexMostUsed][1]) + " presses")


#Writes the output to a file
def writeKeyListToFile(keyList):
    pass

def main():
    yearList = os.listdir()  # List of all years that exist in the MIDI archive
    monthList = os.listdir() # List of all months that exist, created on a "per archive year" basis
    sumNotes = 0 # Amount of notes played
    sumTime = 0  # Amount of time played
    corruptFileWarning = False # Midi parser raises error if corrupt file is found, 
    keyList = initializeList() # A list of all midi keys on the keyboard (NOTE: assumes 88 keys), 
                               # and how much they have been played. Signature of item in keyList:
                               # ["keyname", numpressed], ex: ["C4", 5124] if the key C4 has been 
                               # played 5124 times
    print("Progress: ")
    for i in range(len(yearList)):
        if "." not in yearList[i]: # Looks for folders, and not items which contain "." (mitigation to ignore this file in search)
            print("Year " + yearList[i] + " started")
            monthList[i] = os.listdir(yearList[i])
            for j in range(len(monthList[i])):
            #for j in range(0):
                print("\tMonth " + monthList[i][j] + " started")

                try: #If the *NIX way of path resolving does not work, try the Windows way
                    archivelist = os.listdir(yearList[i] + "/" + monthList[i][j])
                except:
                    archivelist = os.listdir(yearList[i] + "\\" + monthList[i][j]) 
                
                # Calculate the sum of notes and time played
                for k in range(len(archivelist)):
                    row = archivelist[k].split() # The file name split into a list, split by space

                    # Indices for the row:
                    # 0 - Date (YYYY-MM-DD)
                    # 1 - Time (HHMM)
                    # 2 - Day of the week: (Day), Ex: (Wednesday)
                    # 3 - How many notes
                    # 4 - The word "notes,"
                    # 5 - Duration of the file (in seconds)
                    # 6 - The word "seconds" followed by file extension (.mid)

                    sumNotes += int(row[3])
                    sumTime += float(row[5])
                    midiTemp = 0 #"Declare variable"

                    try: # If the *NIX way of path resolving does not work, try the Windows way
                        midiTemp = mido.MidiFile(yearList[i] + "/" + monthList[i][j] + "/" + archivelist[k])
                        tmpKeyList = parseMidiFile(midiTemp) # Temporary list, used for adding key count of current file to total
                        keyList = addKeyLists(keyList, tmpKeyList)
                    except:
                        try:
                            midiTemp = mido.MidiFile(yearList[i] + "\\" + monthList[i][j] + "\\" + archivelist[k])
                            tmpKeyList = parseMidiFile(midiTemp) # Temporary list, used for adding key count of current file to total
                            keyList = addKeyLists(keyList, tmpKeyList)
                        except OSError:
                            print("Warning: File '" + yearList[i] + "/" + monthList[i][j] + "/" + archivelist[k] + "' is likely corrupted!") 
                            corruptFileWarning = True # MIDI module raises OSError if a MIDI file is corrupted, 
                                                      # print warning if corrupted file is found

                    


    timePlayedList = returnTime(sumTime)
    print("You've played for: " + str(timePlayedList[0]) + " hour(s), " + str(timePlayedList[1])\
          + " minute(s) and " + str(timePlayedList[2]) + " second(s), with " + str(sumNotes) + " notes! Wow!")

    printKeyList(keyList)
    if corruptFileWarning:
        print("Warning: corrupted MIDI files were detected and as such they have been excluded from the breakdown table "\
               + "but not the total note count.")

main()