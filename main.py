# Solution for Laboratory Work #4-6
# Course: "Distributed Systems Technologies and Parallel Computing Organization"

import numpy as np
import socket
import pickle
import threading
import time
import os

# Matrices provided in the assignment
DB1 = np.array([
    [-600, 500, 50, 250, 100, 200, 50, 30, 50, 200],
    [500, -600, 50, 50, 250, 100, 80, 60, 150, 40],
    [50, 50, -525, 200, 50, 40, 100, 70, 200, 25],
    [250, 50, 200, -475, 10, 70, 40, 25, 30, 50],
    [100, 250, 50, 10, -425, 100, 150, 40, 100, 250],
    [200, 100, 40, 70, 100, -380, 100, 60, 30, 45],
    [50, 80, 100, 40, 150, 100, -300, 80, 65, 30],
    [30, 60, 70, 25, 40, 60, 80, -250, 100, 90],
    [50, 150, 200, 30, 100, 30, 65, 100, -70, 200],
    [200, 40, 25, 50, 250, 45, 30, 90, 200, -20]
])

DB2 = np.array([
    [-100, 50, 10, 25, 30],
    [50, -60, 5, 10, 25],
    [10, 5, -50, 20, 50],
    [25, 10, 20, -40, 10],
    [30, 25, 50, 10, -10]
])

# Function to calculate the largest eigenvalue using numpy
def calculate_largest_eigenvalue(matrix):
    eigenvalues = np.linalg.eigvals(matrix)
    largest_eigenvalue = max(eigenvalues, key=lambda x: abs(x))
    return largest_eigenvalue

# Semaphore to synchronize the tasks
result_ready = threading.Event()
L2_result = None

# ===== HOST COMPUTER (CLIENT) CODE =====
def host_computer():
    # Task 1: Calculate L1 using the smaller matrix (DB2)
    print("Host: Starting Task 1 - Calculating L1 from smaller matrix")
    L1 = calculate_largest_eigenvalue(DB2)
    print(f"Host: L1 calculation complete: {L1}")
    
    # Connect to slave server to request Task 2 calculation
    print("Host: Connecting to slave server for Task 2")
    host = '127.0.0.1'  # Use the appropriate slave server address
    port = 65432
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.connect((host, port))
            print("Host: Connected to slave server")
            
            # Send the larger matrix to the slave
            data = pickle.dumps(DB1)
            s.sendall(data)
            print("Host: Sent matrix data to slave server")
            
            # Wait for the result from the slave
            print("Host: Waiting for L2 result from slave server")
            result_data = b""
            while True:
                packet = s.recv(4096)
                if not packet:
                    break
                result_data += packet
            
            global L2_result
            L2_result = pickle.loads(result_data)
            print(f"Host: Received L2 result from slave: {L2_result}")
            
            # Signal that the result is ready
            result_ready.set()
            
        except Exception as e:
            print(f"Host: Error connecting to slave server: {e}")
            print("Host: Calculating L2 locally as fallback")
            L2_result = calculate_largest_eigenvalue(DB1)
            result_ready.set()
    
    # Wait for the L2 result
    print("Host: Waiting for L2 calculation to complete")
    result_ready.wait()
    L2 = L2_result
    
    # Task 3: Calculate L3 based on the comparison of L1 and L2
    print("Host: Starting Task 3 - Calculating L3")
    if abs(L1) > abs(L2):
        L3 = (L1**2) * L2
        print(f"Host: L1 > L2, using formula: L3 = (L1^2) * L2")
    else:
        L3 = L1 * (L2**2)
        print(f"Host: L1 <= L2, using formula: L3 = L1 * (L2^2)")
    
    # Print the final results
    print("\n===== FINAL RESULTS =====")
    print(f"L1: {L1}")
    print(f"L2: {L2}")
    print(f"L3: {L3}")
    print("========================\n")
    
    return L1, L2, L3

# ===== SLAVE SERVER CODE =====
def slave_server():
    host = '0.0.0.0'  # Listen on all interfaces
    port = 65432
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen()
        print(f"Slave: Server started, listening on {host}:{port}")
        
        conn, addr = s.accept()
        with conn:
            print(f"Slave: Connected by {addr}")
            
            # Receive the matrix from the host
            data = b""
            while True:
                packet = conn.recv(4096)
                if not packet:
                    break
                data += packet
            
            matrix = pickle.loads(data)
            print("Slave: Received matrix data, starting L2 calculation")
            
            # Task 2: Calculate L2 using the larger matrix
            L2 = calculate_largest_eigenvalue(matrix)
            print(f"Slave: L2 calculation complete: {L2}")
            
            # Send the result back to the host
            result_data = pickle.dumps(L2)
            conn.sendall(result_data)
            print("Slave: Sent L2 result back to host")

# Function to run the solution in a simulated environment
def run_simulation():
    # Create threads for host and slave
    slave_thread = threading.Thread(target=slave_server)
    host_thread = threading.Thread(target=host_computer)
    
    # Start the slave server first
    slave_thread.start()
    time.sleep(1)  # Give the server time to start
    
    # Then start the host client
    host_thread.start()
    
    # Wait for both threads to complete
    host_thread.join()
    slave_thread.join()

# For demonstration, show how to run the solution
if __name__ == "__main__":
    print("Starting distributed computation simulation...")
    
    # Check if we should run as host or slave
    if os.environ.get('COMPUTE_ROLE') == 'slave':
        print("Running as slave server")
        slave_server()
    else:
        print("Running as host computer")
        try:
            # Try to run the full simulation on a single machine
            run_simulation()
        except Exception as e:
            print(f"Simulation failed: {e}")
            print("Running host computation only")
            host_computer()