import time
import unittest
import os
import sys

import minimalmodbus

sys.path.append(os.path.abspath(os.curdir))
sys.path.append(os.path.dirname(os.path.abspath(os.curdir)))
from source import cnmodbus


class SerialTests(unittest.TestCase):
    def setUp(self):
        self.modbus_conn = cnmodbus.CosmicNodeModbus(port="/dev/ttyUSB0", device_address=1)

    def tearDown(self):
        pass

    def test_01_slaveid(self):
        try:
            # Reading a slave ID
            response = self.modbus_conn.read_register(1, 1)
            time.sleep(3)
            print(f'Test case 1 Reading the current slave ID.\nThe Current Slave ID is {response}\n')
            self.assertEqual(response, [1])
            #self.modbus_conn.write_single_register(1, 1)

            # Writing the Slave ID to 2
            self.modbus_conn.write_single_register(1, 2)
            self.modbus_conn = cnmodbus.CosmicNodeModbus(port="/dev/ttyUSB0", device_address=2)
            response = self.modbus_conn.read_register(1, 1)
            time.sleep(3)
            print(f'Writing and reading back the Slave ID.\nNow The Slave ID is {response}\n')
            self.assertEqual(response, [2])
            self.modbus_conn.write_single_register(1, 1)
            time.sleep(3)
            self.modbus_conn = cnmodbus.CosmicNodeModbus(port="/dev/ttyUSB0", device_address=1)
            response = self.modbus_conn.read_register(1, 1)
            time.sleep(3)
            print(f'Writing and reading back the Slave ID.\nNow The Slave ID is {response}\n')

        except Exception as error:
            raise (error)

    def test_02_default_dimming_mode_rw_register(self):
        try:
            # Reading a default dimming mode and writing the dimming mode to Linear incase the default dimming mode is not in Linear
            response = self.modbus_conn.read_register(2, 1)
            time.sleep(3)
            if response == [2]:
                self.assertEqual(response, [2])
                print(f'Test case 2: Reading the Default Dimming mode.\nThe Default dimming mode is in Linear {response}\n')
                time.sleep(1)
            else:
                self.modbus_conn.write_single_register(2, 2)
                time.sleep(5)
                response = self.modbus_conn.read_register(2, 1)
                time.sleep(3)
                self.assertEqual(response, [2])
                print(f'Test case 2:Writing and reading back the Dimming mode.\nNow the dimming mode is set to Linear {response}\n')

            # Writing dimming values for 10 zones using the Multiple Register in the Linear mode
            self.modbus_conn.write_multiple_register(32882, "[10, 20, 30, 40, 50, 60, 70, 80, 90, 0]")
            time.sleep(15)
            print(f'Linear mode multiple Register: Brightness level of the lights in the zone 32891 should be in 0\n')

            # Writing dimming value for the 123rd zone using the single Register in the Linear mode
            self.modbus_conn.write_single_register(32891, 100)
            time.sleep(10)
            print(f'Linear mode single Register: Brightness level of the lights in the zone 32891 should be in 100\n')

            # Reading dimming values for all 10 zones
            response = self.modbus_conn.read_register(32882, 10)
            time.sleep(3)
            self.assertEqual(response, [10, 20, 30, 40, 50, 60, 70, 80, 90, 100])
            print(f'Writing and Reading dimming value for 10 registers in Linear mode:\n{response}\n')

        except Exception as error:
            raise(error)

    def test_03_logarithmic_dimming_mode_RW_Register(self):
        try:
            # Writing the dimming mode to Logarithmic
            self.modbus_conn.write_single_register(2, 1)
            time.sleep(5)
            response = self.modbus_conn.read_register(2, 1)
            time.sleep(3)
            self.assertEqual(response, [1])
            print(f'Test case 3: Writing and reading back the Dimming mode.\nNow the dimming mode is set to Logarithmic {response}.\n')

            # Reading dimming values for all 123 zones in Logarithmic to check the Values conversion
            response = self.modbus_conn.read_register(32882, 10)
            time.sleep(3)
            self.assertEqual(response, [2734, 3144, 3383, 3553, 3685, 3793, 3884, 3963, 4032, 4095])
            print(f'Reading the dimming value for 10 register in Logarithmic mode to check the conversion:\n{response}\n')

            # Writing dimming values for 123 zones using the Multiple Register in the Logarithmic mode
            self.modbus_conn.write_multiple_register(32769, "[0, 0, 0, 0, 0, 0, 0, 0, 2734, 2734, 0, 0, 0, 0, 0, 0, 0, 0, 3144, 3144, 0, 0, 0, 0, 0, 0, 0, 0, 3383, 3383, 0, 0, 0, 0, 0, 0, 0, 0, 3553, 3553, 0, 0, 0, 0, 0, 0, 0, 0, 3686, 3685, 0, 0, 0, 0, 0, 0, 0, 0, 3793, 3793, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3884, 3884, 0, 0, 0, 0, 0, 0, 0, 0, 3963, 3963, 0, 0, 0, 0, 0, 0, 0, 0, 4032, 4032, 0, 0, 0, 0, 0, 0, 0, 0, 4095, 4095, 0, 0, 0, 0, 0, 0, 0, 0, 4095, 2790, 0, 0, 0, 0, 0, 0, 0, 0, 4095, 3200, 0, 0]")
            time.sleep(55)
            print(f'Logarithmic mode Multiple Register: Brightn cess level of the lights in the zone 32891 should be in 0\n')

            # Writing dimming value for the 123rd zone using the single Register in the Logarithmic mode
            self.modbus_conn.write_single_register(32891, 4095)
            time.sleep(10)
            print(f'Logarithmic mode single Register: Brightness level of the lights in the zone 32891 should be in 100\n')

            # Reading dimming values for all 123 zones
            response = self.modbus_conn.read_register(32769, 123)
            time.sleep(3)
            self.assertEqual(response, [0, 0, 0, 0, 0, 0, 0, 0, 2734, 2734, 0, 0, 0, 0, 0, 0, 0, 0, 3144, 3144, 0, 0, 0, 0, 0, 0, 0, 0, 3383, 3383, 0, 0, 0, 0, 0, 0, 0, 0, 3553, 3553, 0, 0, 0, 0, 0, 0, 0, 0, 3686, 3685, 0, 0, 0, 0, 0, 0, 0, 0, 3793, 3793, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3884, 3884, 0, 0, 0, 0, 0, 0, 0, 0, 3963, 3963, 0, 0, 0, 0, 0, 0, 0, 0, 4032, 4032, 0, 0, 0, 0, 0, 0, 0, 0, 4095, 4095, 0, 0, 0, 0, 0, 0, 0, 0, 4095, 2790, 0, 0, 0, 0, 0, 0, 0, 0, 4095, 3200, 0, 4095])
            print(f'Writing and Reading the dimming value for 123 registers in Logarithmic mode:\n{response}\n')

        except Exception as error:
            raise(error)

    def test_04_channel2_rw_register(self):
        try:
            # Reading a default channel Value
            response = self.modbus_conn.read_register(3, 1)
            time.sleep(3)
            #self.assertEqual(response, [1])
            print(f'Test case 4: The default channel value is {response}\n')

            # Writing the channel value to 2
            self.modbus_conn.write_single_register(3, 2)
            time.sleep(3)
            response = self.modbus_conn.read_register(3, 1)
            time.sleep(3)
            self.assertEqual(response, [2])
            print(f'Writing and reading back the channel value \nNow the channel value is set to {response}.\n')

            # Writing the dimming mode to Linear
            self.modbus_conn.write_single_register(2, 2)
            time.sleep(5)
            response = self.modbus_conn.read_register(2, 1)
            time.sleep(3)
            self.assertEqual(response, [2])
            print(f'Writing and reading back the Dimming mode.\nNow the dimming mode is set to Linear {response}\n')

            # Writing dimming values for 6 zones using the Multiple Register in the Linear mode
            self.modbus_conn.write_multiple_register(32886, "[100, 70, 50, 30, 10, 50]")
            time.sleep(15)
            print(f'Channel 2, Linear mode multiple Register: Brightness level of the lights in the zone 32891 should be in 50\n')

            # Writing dimming value for the 123rd zone using the single Register in the Linear mode
            self.modbus_conn.write_single_register(32891, 0)
            time.sleep(10)
            print(f'Channel 2, Linear mode single Register: Brightness level of the lights in the zone 32891 should be in 0\n')

            # Reading dimming values for all 7 zones
            response = self.modbus_conn.read_register(32885, 7)
            time.sleep(5)
            self.assertEqual(response, [0, 100, 70, 50, 30, 10, 0])
            print(f'Writing and Reading the dimming value for 7 registers in Linear mode via channel 2:\n{response}\n')

        except Exception as error:
            raise(error)

    def test_05_set_start_zone_address_rw_register(self):
        try:
            # Reading a default starting zone address
            response = self.modbus_conn.read_register(4, 1)
            time.sleep(3)
            self.assertEqual(response, [32769])
            print(f'Test case 5: The default starting zone address is {response}\n')

            # Writing the starting zone address to 32892
            self.modbus_conn.write_single_register(4, 32770)
            time.sleep(3)
            response = self.modbus_conn.read_register(4, 1)
            time.sleep(3)
            self.assertEqual(response, [32770])
            print(f'Writing and reading back the starting zone address \nNow the starting zone address is set to {response}.\n')

            # Writing the Channel value to 1
            self.modbus_conn.write_single_register(3, 1)
            time.sleep(5)
            response = self.modbus_conn.read_register(3, 1)
            time.sleep(3)
            self.assertEqual(response, [1])
            print(f'Writing and reading back the channel value.\nNow the channel value is set to {response}\n')

            # Writing dimming values for all 123 zones using the Multiple Register in the Linear mode
            self.modbus_conn.write_multiple_register(32770, "[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 0, 0, 0, 0, 0, 0, 0, 0, 0, 100, 0, 0, 0, 0, 0, 0, 0, 0, 0, 100, 100, 0]")
            time.sleep(55)
            print(f'Linear mode multiple Register: Brightness level of the lights in the zone 32891 should be in 100\n')

            # Writing dimming value for the 123rd zone using the single Register in the Linear mode
            self.modbus_conn.write_single_register(32891, 0)
            time.sleep(10)
            print(f'Linear mode single Register: Brightness level of the lights in the zone 32891 should be in 0\n')

            # Reading dimming values for all 123 zones
            response = self.modbus_conn.read_register(32770, 123)
            time.sleep(10)
            self.assertEqual(response, [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 0, 0, 0, 0, 0, 0, 0, 0, 0, 100, 0, 0, 0, 0, 0, 0, 0, 0, 0, 100, 0, 0])
            print(f'Writing and Reading the 123 register in Linear mode (here starting zone address is 32770):\n{response}\n')

            # writing back the starting zone address to 32769
            self.modbus_conn.write_single_register(4, 32769)
            time.sleep(3)

        except Exception as error:
            raise(error)

if __name__ == '__main__':
    unittest.main()
