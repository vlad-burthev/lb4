import numpy as np
import socket
import pickle

def calculate_largest_eigenvalue(matrix):
    eigenvalues = np.linalg.eigvals(matrix)
    largest_eigenvalue = max(eigenvalues, key=lambda x: abs(x))
    return largest_eigenvalue

def slave_server():
    host = '0.0.0.0'  
    port = 65432
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen()
        print(f"Сервер: {host}:{port}")
        
        conn, addr = s.accept()
        with conn:
            print(f"Сервер: Підключено до {addr}")
            
            
            data = b""
            while True:
                packet = conn.recv(4096)
                if not packet:
                    break
                data += packet
            
            matrix = pickle.loads(data)
            print("Сервер: Розрахунок L2")
            
            
            L2 = calculate_largest_eigenvalue(matrix)
            print(f"Сервер: L2: {L2}")
            
            
            result_data = pickle.dumps(L2)
            conn.sendall(result_data)
            

if __name__ == "__main__":
    print("Сервер")
    slave_server()