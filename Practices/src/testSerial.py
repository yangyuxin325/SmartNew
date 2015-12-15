import serial
ser = serial.Serial(0)
print ser.name
ser.write("hello")
ser.close()