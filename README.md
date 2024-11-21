# Energy_meter
Single phase DIN RAIL Energy Meter New
Product: EM2M
Compatible with 1 phase 2 wire system, Self-Supplied
176 to 276V AC measurement.
Direct current measurement up to 100A
Accuracy of ± 0.5% for voltage & current, 0.1% for Frequency, 0.01% for PF, 1% for Power, Class 1 for Active energy, Class 2 for reactive energy
Two pulse outputs configurable for Import/Export Energy measurement
RS485 Modbus communication, Mbus variant available --------------------------------------------------------

**CRC-TEST**
def ModRTU_CRC(buf, length):
    crc = 0xFFFF  # Initialize CRC to 0xFFFF
    
    for pos in range(length):
        crc ^= buf[pos]  # XOR byte into least significant byte of crc

        for _ in range(8):  # Loop over each bit in the byte
            if (crc & 0x0001) != 0:  # If the LSB is set
                crc >>= 1  # Shift right
                crc ^= 0xA001  # XOR with 0xA001
            else:
                crc >>= 1  # Just shift right if LSB is not set

    # Return the calculated CRC (unsigned 16-bit integer)
    return crc & 0xFFFF

# ALL REGISTER ADDRESSES:
# Register address:
EM2M_DEFAULT_SLAVE_ADDRESS = 0x01
FUNCTION_CODE = 0x04
TOTAL_ACTIVE_ENERGY_REG = 0x01
IMPORT_ACTIVE_ENERGY_REG = 0x03
EXPORT_ACTIVE_ENERGY_REG = 0x05
TOTAL_REACTIVE_ENERGY_REG = 0x07
IMPORT_REACTIVE_ENERGY_REG = 0x09
EXPORT_REACTIVE_ENERGY_REG = 0x0B
APPARENT_ENERGY_REG = 0x0D
ACTIVE_POWER_REG = 0x0F
REACTIVE_POWER_REG = 0x11
APPARENT_POWER_REG = 0x13
VOLTAGE_REG = 0x15
CURRENT_REG = 0x17
POWER_FACTOR_REG = 0x19 
FREQUENCY_REG = 0x1B
MAX_DEMAND_ACTIVE_POWER_REG = 0x1D
MAX_DEMAND_REACTIVE_POWER_REG = 0x1F
MAX_DEMAND_APPARENT_POWER_REG = 0x21

