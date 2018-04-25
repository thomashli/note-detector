from recording_function import *
from note_detector_function import *

import sys, select, time


if len ( sys.argv ) != 2:
        print("Input Threshold Value")
        sys.exit(1)

threshold = int(sys.argv[1])

#count = 0
while True:
	recorder("lala.wav")
	tuner("lala.wav", threshold)
	#print(count, "seconds passed")
	#count += 1
	i,o,e = select.select([sys.stdin],[],[],0.0001)
	if i == [sys.stdin]:
		break