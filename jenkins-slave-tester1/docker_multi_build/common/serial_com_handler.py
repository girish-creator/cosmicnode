import serial
from common import configuration
import logging
import time


class SerialConnException(Exception):
    pass


class SerialConn:
    def __init__(self):
        self.logger = logging.getLogger(name="serial_handler.log")
        self.serial_obj = ""
        self.timeout = 600

    def connect(self):
        try:
            self.serial_obj = serial.Serial(port=configuration.SERIAL_RX_COM_PORT,
                                            baudrate=configuration.SERIAL_RX_BAUD_RATE,
                                            parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE,
                                            bytesize=serial.EIGHTBITS, timeout=0)
        except Exception as error:
            raise SerialConnException(str.format("SerialConn: connect: {0}", error))

    def wait_for_message(self):
        try:
            char_string = ""
            loop = True
            count = 0
            while loop:
                count += 1
                for serial_line in self.serial_obj.read():
                    xt = type(serial_line)
                    xts = str(serial_line)
                    char_string = char_string + str(chr(serial_line))
                    if "\n" in chr(serial_line):
                        loop = False
                if count >= self.timeout:
                    raise TimeoutError("no message received within time limit")
                time.sleep(0.1)
            return char_string
        except Exception as error:
            raise SerialConnException(str.format("SerialConn: wait_for_message: {0}", error))

    def write_message(self, message):
        count = 1
        for serial_line in self.serial_obj.write():
            print(str(count) + str(': ') + chr(serial_line))

            count = count + 1

    def disconnect(self):
        try:
            self.serial_obj.close()
        except Exception as error:
            raise SerialConnException(str.format("SerialConn: wait_for_message: {0}", error))


if __name__ == "__main__":
    ser_obj = SerialConn()
    ser_obj.connect()
    message = "LGT¯CMD¯LIGHT¯BRIGHTNESS: 5"
    x = ser_obj.wait_for_message()
    print("message found...!!!!!!!!")
    print(x)