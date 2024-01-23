from attendance import *
from PhotoCapture import take_pic

if __name__ == "__main__":
    temp = int(input("Enter 0 for Photo capture or any key for live detection: "))
    if temp == 0:
        take_pic()
    else:
        live_detect()
    