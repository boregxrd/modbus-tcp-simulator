import logging
from pymodbus.server import StartTcpServer
from pymodbus.datastore import ModbusSequentialDataBlock, ModbusServerContext
from pymodbus.datastore.context import ModbusSlaveContext

logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.INFO)

# Define the Memory Map (The "Registers")
# We create a block of memory.
# store initializes registers with 0.
store = ModbusSlaveContext(
    di=ModbusSequentialDataBlock(0, [0]*100), # Discrete Inputs
    co=ModbusSequentialDataBlock(0, [0]*100), # Coils
    hr=ModbusSequentialDataBlock(0, [0]*100), # Holding Registers
    ir=ModbusSequentialDataBlock(0, [0]*100)  # Input Registers
)

context = ModbusServerContext(slaves=store, single=True)

print("Starting Modbus TCP Slave on localhost:5020...")
print("Press Ctrl+C to stop.")

StartTcpServer(context=context, address=("127.0.0.1", 5020))