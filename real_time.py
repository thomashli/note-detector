from recording_function import *
from note_detector_function import *

import sys, select, time

#count = 0
while True:
	recorder("lala.wav")
	tuner("lala.wav")
	#print(count, "seconds passed")
	#count += 1
	i,o,e = select.select([sys.stdin],[],[],0.0001)
	if i == [sys.stdin]:
		break