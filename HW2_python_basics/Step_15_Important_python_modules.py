import time, datetime, os, sys


if __name__=="__main__":
     start_time = time.time()
     print("Operating sistem is", os.name)
     print("Today is", datetime.datetime.today())
     print("Path to Python:", sys.executable)
     print("Time execute is %s seconds " % (time.time() - start_time))
     
