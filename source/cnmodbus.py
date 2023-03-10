#!/usr/bin/env python3
"""
This module helps to create a serial connection to a device using modbus
which is a method used for transmitting information over serial
lines between electronic devices.
This module supports read, write and write multiple operations.
Example:
    modbus_conn = CosmicNodeModbus(port=device_port, device_address=value)
    response = modbus_conn.read_register(2, 1)
"""
import ast
import minimalmodbus


class CosmicNodeModbus:
    """
    CosmicNodeModbus class enables this module to achieve the serial
    connection using minimalmodbus python package.
    """
    def __init__(self, port, device_address):
        """Instantiate the CosmicNodeModbus class
        :param port: device port such as /dev/ttyUSB or COM1
        :param device_address: Slave address (int) can start from 1
        """
        self.instrument = minimalmodbus.Instrument(port, int(device_address),
                                                   mode=minimalmodbus.MODE_RTU)
        self.instrument.serial.baudrate = 19200  # Baud Rate
        self.instrument.serial.bytesize = 8
        self.instrument.serial.parity = minimalmodbus.serial.PARITY_EVEN
        self.instrument.serial.stopbits = 1
        self.instrument.serial.timeout = 60  # seconds
        self.instrument.close_port_after_each_call = True
        self.instrument.clear_buffers_before_each_transaction = True

    def read_register(self, register_address, num_reg):
        """Read data from device using modbus protocol
        Read integers from 16-bit registers in the slave.
        The slave registers can hold integer values in the range 0 to 65535
        :param register_address: The slave register start address (use decimal
              numbers, not hex).
        :param num_reg: The number of registers to read, max 125 registers.
        :return: response from device
        """
        response = self.instrument.read_registers(int(register_address),
                                                  int(num_reg),
                                                  functioncode=3)
        return response

    def write_single_register(self, register_address, value):
        """
        Write an integer to one 16-bit register in the slave.
        The slave register can hold integer values in the range 0 to 65535.
        :param register_address: The slave register address  (use decimal
              numbers, not hex).
        :param value: The value to store in the slave register (might be
              scaled before sending).
        """
        self.instrument.write_register(int(register_address), int(value),
                                       number_of_decimals=0, functioncode=6,
                                       signed=False)

    def write_multiple_register(self, register_address, values):
        """
        Write integers to 16-bit registers in the slave.
        The slave register can hold integer values in the range 0 to 65535.
        :param register_address: The slave register start address (use decimal
              numbers, not hex).
        :param values: The values to store in the slave registers,
              max 123 values. The first value in the list is for the register
              at the given address.
        """
        self.instrument.write_registers(int(register_address),
                                        ast.literal_eval(values))

    def disconnect(self):
        """
        To close the serial port on demand. When the instrument object
        is called with disconnect it will use the internal serial port
        connection and invoke the serial.close() command on the
        current connection.
        """
        self.instrument.serial.close()
