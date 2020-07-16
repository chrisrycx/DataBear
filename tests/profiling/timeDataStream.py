'''
Use timeit to test data stream speed
'''
from timeit import timeit
import serial
comm = serial.Serial('COM5',38400,timeout=0)
data = "X52:22:1235,target=1235,frames=60,currentloops=5000\r\n".encode('utf-8')
tests = 500

tot = timeit('comm.write(data)',globals=globals(),number=tests)
print(tot/tests)