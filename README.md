# Modbus TCP Simulation: Python Implementation

This project simulates a Modbus TCP network locally using the `pymodbus` library. It demonstrates the architectural shift from Modbus RTU (Serial) to Modbus TCP (Ethernet), specifically focusing on the inversion of network roles where the **Slave acts as the TCP Server** and the **Master acts as the TCP Client**.

## 1\. Conceptual Map

Before running the code, remember the mapping between Industrial and IT terminology:

| Modbus Role | TCP/IP Role | Responsibility |
| :--- | :--- | :--- |
| **Slave** (PLC) | **Server** | Binds to `localhost:5020`. Holds the memory registers. Waits for requests. |
| **Master** (SCADA) | **Client** | Connects to the Server. Initiates Read/Write commands. |

## 2\. Environment Setup (Windows PowerShell)

Since this requires external libraries, we will use a virtual environment to keep your system clean.

**1. Create the Virtual Environment**
Open your terminal in the project folder and run:

```powershell
python -m venv venv
```

**2. Activate the Virtual Environment**

```powershell
.\venv\Scripts\Activate
```

**3. Install Dependencies**
We only need `pymodbus` for this simulation.

```powershell
pip install pymodbus
```

## 3\. How to Run

You will need two separate PowerShell terminals to simulate the two distinct devices.

### Terminal 1: The Slave (Server)

This script initializes the memory block and opens the socket listener.

```powershell
# Make sure venv is activated
python slave_server.py
```

*You will see a message indicating the server is listening. Leave this window open.*

### Terminal 2: The Master (Client)

This script connects to the Slave, performs a Write operation, and then a Read operation.

```powershell
# Make sure venv is activated
python master_client.py
```

## 4\. Under the Hood: The Lifecycle of a Packet

Here is exactly what happens on the network stack when you run `master_client.py`:

1.  **Connection:** The Master initiates a standard TCP Handshake (SYN, SYN-ACK, ACK) to `127.0.0.1` on port `5020`.
2.  **Session:** The Slave accepts the connection; a persistent socket session is established.
3.  **Encapsulation:** The Master constructs the Modbus TCP Frame. Unlike RTU, there is no CRC checksum.
      * **MBAP Header:** `[TransID][ProtoID][Len][UnitID]`
      * **PDU:** `[0x06]` (Write Single Register) + `[Addr]` + `[Data]`
4.  **Transmission:** The Master pushes these bits through the simulated network adapter (Loopback interface).
5.  **Processing:**
      * The Slave receives the bits and parses the MBAP header.
      * It identifies Function Code `0x06` (Write).
      * It updates its internal `ModbusSequentialDataBlock` memory map.
6.  **Response:** The Slave sends a confirmation frame (Response PDU) back to the Master.
7.  **Teardown:** The Master prints the result and closes the socket connection (FIN packet).