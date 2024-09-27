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

# Example usage:
data = [0x01, 0x03, 0x00, 0x00, 0x00, 0x0A]  # Sample byte array
crc_result = ModRTU_CRC(data, len(data))
print(f"CRC result: {hex(crc_result)}") -----------------------------------------------------------------
