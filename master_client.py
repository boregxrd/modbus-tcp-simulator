from pymodbus.client import ModbusTcpClient

IP_ADDRESS = '127.0.0.1'
PORT = 5020

client = ModbusTcpClient(IP_ADDRESS, port=PORT)

if client.connect():
    print(f"Connected to {IP_ADDRESS}:{PORT}")
    
    try:
        print("Writing 123 to Register 1...")
        client.write_register(1, 123, device_id=1)
        
        print("Reading Register 1 back...")
        result = client.read_holding_registers(1, count=1, device_id=1)
        
        if not result.isError():
            print(f"Received value: {result.registers[0]}")
        else:
            print("Error reading registers")

    except Exception as e:
        print(f"An error occurred: {e}")
        
    finally:
        client.close()
        print("Connection closed.")
else:
    print("Failed to connect.")