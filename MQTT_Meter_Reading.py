import struct
import serial
import time
import paho.mqtt.client as mqtt
import json

# MQTT setup
MQTT_BROKER = "192.168.68.106"  # Replace with your MQTT broker IP or domain (106 -> NWO, 131 -> CellProp)
MQTT_PORT = 1884  # Default MQTT port
MQTT_TOPIC = "Energy_Meter_P01"  # Topic to publish Modbus data

# MQTT Client initialization
client = mqtt.Client()

# Register address constants
EM2M_DEFAULT_SLAVE_ADDRESS = 0x01
FUNCTION_CODE = 0x04

# Registers
TOTAL_ACTIVE_ENERGY_REG = 0x01
VOLTAGE_REG = 0x15
CURRENT_REG = 0x17
ACTIVE_POWER_REG = 0x0F  # Added Active Power Register

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

# Function to send Modbus requests and read responses
def read_register(register):
    try:
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

            ser.close()  # Close port after reading

            # Process response
            if len(response) >= 7:  # Ensure valid response
                data_bytes = response[3:7]  # Extract data bytes
                float_value = struct.unpack('>f', data_bytes)[0]  # Big-endian float
                return "", float_value  # Removed SUCCESS message for simplicity
            else:
                return "FAILURE", 0.00
        else:
            print("Serial port failed to open")
            return "FAILURE", 0.00
    except Exception as e:
        print(f"Error: {e}")
        return "FAILURE", 0.00

# Continuous function to read and print voltage, current, active power, and total active energy, and send via MQTT
def read_data_continuously():
    try:
        while True:
            # Reading voltage
            status, voltage = read_register(VOLTAGE_REG)
            print(f"Voltage Reading: {status}, Value: {voltage:.2f} V")

            # Reading current
            status, current = read_register(CURRENT_REG)
            print(f"Current Reading: {status}, Value: {current:.2f} A")

            # Reading active power
            status, active_power = read_register(ACTIVE_POWER_REG)
            print(f"Active Power Reading: {status}, Value: {active_power:.2f} KW")

            # Reading total active energy
            status, total_active_energy = read_register(TOTAL_ACTIVE_ENERGY_REG)
            print(f"Total Active Energy Reading: {status}, Value: {total_active_energy:.2f} kWh")

            # Prepare data for MQTT
            modbus_data = {
                "voltage": voltage,
                "current": current,
                "active_power": active_power,
                "total_active_energy": total_active_energy
            }

            # Publish data to MQTT
            client.publish(MQTT_TOPIC, json.dumps({"type": 'energyMonitoring', "message": modbus_data}))
            print(f"Published to MQTT: {modbus_data}")

            # Add a short delay to avoid overwhelming the device with requests
            time.sleep(2)  # Adjust the delay as needed
    except KeyboardInterrupt:
        print("Reading stopped by user (keyboard interrupt)")

# Example usage
if __name__ == "__main__":
    # Connect to the MQTT broker
    client.connect(MQTT_BROKER, MQTT_PORT, 60)
    client.loop_start()  # Start the MQTT loop in a background thread
    
    # Start reading and sending data
    read_data_continuously()
    
    # Stop MQTT loop when done
    client.loop_stop()
