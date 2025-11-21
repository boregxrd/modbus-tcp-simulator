import logging
from pymodbus.server import StartTcpServer
from pymodbus.datastore import ModbusSequentialDataBlock, ModbusServerContext, ModbusDeviceContext

logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.INFO)

store = ModbusDeviceContext(
    di=ModbusSequentialDataBlock(0, [0]*100),
    co=ModbusSequentialDataBlock(0, [0]*100),
    hr=ModbusSequentialDataBlock(0, [0]*100),
    ir=ModbusSequentialDataBlock(0, [0]*100)
)

context = ModbusServerContext(devices=store, single=True)

print("Starting Modbus TCP Slave on localhost:5020...")
print("Press Ctrl+C to stop.")

StartTcpServer(context=context, address=("127.0.0.1", 5020))