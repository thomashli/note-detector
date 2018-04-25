import sys, select, time

while True:
    print("Looping until ENTER pressed")
    i,o,e = select.select([sys.stdin],[],[],0.0001)
    if i == [sys.stdin]: 
    	break
print("Goodbye")