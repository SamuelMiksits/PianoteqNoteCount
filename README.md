# Pianoteq Note Count

Uses the MIDI archiving feature to calculate how many notes have been played on your instance of Pianoteq. So in practice, if all notes have been played on one digital piano/keyboard, and that device has exclusively been used with Pianoteq, it calculates how many notes you have played on that keyboard.

Two versions of the script exists. The first one is ```NoteCount.py``` which calculates the total note count, and gives you the note count together with a sum of time played expressed in hours, minutes and seconds. The second one ```NoteCountExtended.py``` also scans the contents of all MIDI files, and computes how many times each key was pressed, and provides a per-key breakdown of how many times each individual key was pressed. This can take many minutes for a large archive and a slow computer, so a version called ```NoteCountExtendedMultiProc.py``` exists which runs the program on all cores. 

Example output for both versions of the script:

```NoteCount.py```:

```
You've played for: 429 hour(s), 36 minute(s) and 1 second(s), with 11143713 notes! Wow!
```


```NoteCountExtended.py```:

```
You've played for: 429 hour(s), 36 minute(s) and 1 second(s), with 11143713 notes! Wow!
Breakdown of how many times each key was played: 
------------------------------------------------------------------------------------------------------------------------
|   Octave | 0         | 1         | 2         | 3         | 4         | 5         | 6         | 7         | 8         |
------------------------------------------------------------------------------------------------------------------------
|        C | ---       | 4357      | 130037    | 373735    | 555040    | 490334    | 165615    | 18039     | 272       |
|       C# | ---       | 2546      | 36260     | 93852     | 171281    | 207303    | 59697     | 4051      | ---       |
|        D | ---       | 2864      | 88548     | 259628    | 290499    | 215130    | 88289     | 3617      | ---       |
|       D# | ---       | 803       | 63019     | 234153    | 344523    | 252236    | 59912     | 3452      | ---       |
|        E | ---       | 2198      | 81904     | 180308    | 227902    | 166913    | 52101     | 3303      | ---       |
|        F | ---       | 16733     | 144837    | 369813    | 367789    | 290961    | 77744     | 421       | ---       |
|       F# | ---       | 4381      | 40415     | 108568    | 121477    | 73753     | 18055     | 75        | ---       |
|        G | ---       | 34246     | 260516    | 454377    | 443335    | 251928    | 48600     | 137       | ---       |
|       G# | ---       | 15221     | 139164    | 302068    | 330024    | 175673    | 27054     | 78        | ---       |
|        A | 238       | 15033     | 89991     | 162911    | 190732    | 87240     | 25674     | 115       | ---       |
|       A# | 109       | 28655     | 154806    | 257236    | 234593    | 95681     | 7524      | 64        | ---       |
|        B | 484       | 37189     | 165396    | 201522    | 209522    | 106258    | 21023     | 83        | ---       |
------------------------------------------------------------------------------------------------------------------------
Least used key: A#7 with 64 presses
Most used key: C4 with 555040 presses
```

# Prerequisites

- Pianoteq needs to be configured with automatic recording enabled, specifically on the setting "a billion years" if you want it to count lifetime.
- Uses Python. The module ```mido``` is needed only for the ```NoteCountExtended.py``` and ```NoteCountExtendedMultiProc.py``` scripts, but not ```NoteCount.py```.
- I have only tested this script on Linux, but I have written it so that it should also be able to run on Windows. I have no idea if it will work on Mac.

# How to run it

Start by moving the scripts (the .py files) to your ```Archive``` folder. The default location should be:

```
C:\Users\YourUserName\AppData\Roaming\Modartt\Pianoteq\Archive
```

on Windows, and:

```
/home/YourUserName/.local/share/Modartt/Pianoteq/Archive
```

on Linux, and for Mac I do not know.


If you wish to run either of the versions with the per-note breakdown, you need to install the ```mido``` package.

For Windows, this could be done with the pip package manager by running:

```
pip install mido
```

On a lot of major Linux distribution nowadays, PEP668 has been adopted which prohibits installing packages systemwide as they can conflict with packages installed by the package manager. As such, the proper workaround is to use virtual environments. Start by creating a new virtual environment:

```
virtualenv pianoteqnotecount
```

though you should not place the virtual environment in your archive folder, as the script will think that this folder is part of the MIDI archive! A workaround if you want it to be in the Archive folder is to name it with a '.' at the start (so .pianoteqnotecount), as the script ignores everything in the root directory that contains a '.'. 

Activate the virtual environment:

```
source ./pianoteqnotecount/bin/activate
```

Afterwards you can install the package with:

```
pip install mido
```

and then after you have run the scripts you can write:
```
deactivate
```

to deactivate the virtual environment.

To run the script, need to enter the command (from the Archive folder):

```
python NoteCount.py
```

on Windows, and:

```
python3 ./NoteCount.py
```

on Linux, if you want to run the ```NoteCount.py``` file.