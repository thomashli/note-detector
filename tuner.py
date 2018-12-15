"""
USAGE: Run python3 tuner.py (threshold value)

Threshold value will be the range the frequency is allowed to deviate from the frequency of an actual note and still register. The higher the tolerance, the easier it is to pick up high notes, but the less accurate low notes become. 
"""

from recording_function import *
from note_detector_function import *

import sys, select, time

def main():
    if len ( sys.argv ) != 2:
        print("Input Threshold Value")
        print("Closing")
        sys.exit(1)

    threshold = int(sys.argv[1])
    count = 0
    while True:
        recorder("note.wav")
        tuner("note.wav", threshold)
        print(count, "seconds passed")
        count += 1
        i,o,e = select.select([sys.stdin],[],[],0.0001)
        if i == [sys.stdin]:
            break

if __name__ == "__main__":
    main()
