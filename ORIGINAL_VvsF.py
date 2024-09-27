import struct
import serial

# Register address constants
EM2M_DEFAULT_SLAVE_ADDRESS = 0x01
FUNCTION_CODE = 0x04

TOTAL_ACTIVE_ENERGY_REG = 0x01
#IMPORT_ACTIVE_ENERGY_REG = 0x03
#EXPORT_ACTIVE_ENERGY_REG = 0x05
#TOTAL_REACTIVE_ENERGY_REG = 0x07
#IMPORT_REACTIVE_ENERGY_REG = 0x09
#EXPORT_REACTIVE_ENERGY_REG = 0x0B
APPARENT_ENERGY_REG = 0x0D
ACTIVE_POWER_REG = 0x0F
# REACTIVE_POWER_REG = 0x11  # Commented out as requested
# APPARENT_POWER_REG = 0x13  # Commented out as requested
VOLTAGE_REG = 0x15
CURRENT_REG = 0x17
POWER_FACTOR_REG = 0x19
FREQUENCY_REG = 0x1B
MAX_DEMAND_ACTIVE_POWER_REG = 0x1D
MAX_DEMAND_REACTIVE_POWER_REG = 0x1F
MAX_DEMAND_APPARENT_POWER_REG = 0x21

# COM port name (update with the correct port on your system)
COM_PORT_NAME = 'COM7'

# CRC16 Calculation (Modbus CRC)
def ModRTU_CRC(data):
    crc = 0xFFFF
    for pos in data:
        crc ^= pos
        for _ in range(8):
            if (crc & 0x0001) != 0:
                crc >>= 1
                crc ^= 0xA001
            else:
                crc >>= 1
    return crc & 0xFFFF

# Function to read data from a given register
def read_register(register):
    try:
        # Configure serial connection
        ser = serial.Serial(COM_PORT_NAME, 9600, 8, 'N', 1, timeout=3)
        if ser.is_open:
            # Prepare Modbus request
            req = [EM2M_DEFAULT_SLAVE_ADDRESS, FUNCTION_CODE, 0x00, register, 0x00, 0x02]
            crc = ModRTU_CRC(req)
            req.append(crc & 0xFF)  # Low byte of CRC
            req.append((crc >> 8) & 0xFF)  # High byte of CRC

            # Send request
            ser.write(bytearray(req))
            response = ser.read(9)  # Read expected response (9 bytes)

            if len(response) >= 7:  # At least a valid response
                data_bytes = response[3:7]  # Extract data bytes
                float_value = struct.unpack('>f', data_bytes)[0]  # Big-endian float
                ser.close()
                return "", float_value
            else:
                ser.close()
                return "FAILURE", 0.00
        else:
            return "FAILURE", 0.00
    except Exception as e:
        print(f"Error: {e}")
        return "FAILURE", 0.00

# Function to read all parameters
def read_all_parameters():
    try:
        # Reading total active energy
        status, total_active_energy = read_register(TOTAL_ACTIVE_ENERGY_REG)
        print(f"Total Active Energy Reading: {status}, Value: {total_active_energy:.2f} kWh")

        # Reading voltage
        status, voltage = read_register(VOLTAGE_REG)
        print(f"Voltage Reading: {status}, Value: {voltage:.2f} V")

        # Reading current
        status, current = read_register(CURRENT_REG)
        print(f"Current Reading: {status}, Value: {current:.2f} A")

        # Reading power factor
       # status, power_factor = read_register(POWER_FACTOR_REG)
       # print(f"Power Factor Reading: {status}, Value: {power_factor:.2f}")

        # Reading active power
        status, active_power = read_register(ACTIVE_POWER_REG)
        print(f"Active Power Reading: {status}, Value: {active_power:.2f} kW")

        # Reading frequency
        #status, frequency = read_register(FREQUENCY_REG)
       # print(f"Frequency Reading: {status}, Value: {frequency:.2f} Hz")

    except Exception as e:
        print(f"Error: {e}")

# Example usage
if __name__ == "__main__":
    read_all_parameters()
