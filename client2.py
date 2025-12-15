import socket
import binascii

def calculate_parity(data, parity_type='even'):
    total_ones = sum(bin(ord(char)).count('1') for char in data)
    if parity_type == 'even':
        return '0' if total_ones % 2 == 0 else '1'
    elif parity_type == 'odd':
        return '0' if total_ones % 2 != 0 else '1'
    return '0'

def calculate_crc(data):
    data_bytes = data.encode('utf-8')
    crc_value = binascii.crc_hqx(data_bytes, 0)
    return hex(crc_value)[2:].upper()

def calculate_hamming(data):
    hamming_code = ""
    for char in data:
        bin_val = f"{ord(char):08b}"
        d = [int(b) for b in bin_val]
        
        p1 = d[0] ^ d[1] ^ d[3] ^ d[4] ^ d[6]
        p2 = d[0] ^ d[2] ^ d[3] ^ d[5] ^ d[6]
        p4 = d[1] ^ d[2] ^ d[3] ^ d[7]
        p8 = d[4] ^ d[5] ^ d[6] ^ d[7]
        
        check_bits = f"{p1}{p2}{p4}{p8}"
        hex_val = hex(int(check_bits, 2))[2:].upper()
        hamming_code += hex_val
    return hamming_code

def calculate_2d_parity(data):
    row_parities = ""
    col_parity_byte = 0

    for char in data:
        val = ord(char)
        total_ones = bin(val).count('1')
        row_parities += '0' if total_ones % 2 == 0 else '1'
        col_parity_byte ^= val

    col_hex = hex(col_parity_byte)[2:].upper()
    return f"{row_parities}-{col_hex}"

def start_receiver():
    host = '127.0.0.1'
    port = 12346

    rec_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    rec_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    rec_socket.bind((host, port))
    rec_socket.listen(1)

    print(f"[Alıcı] Dinleniyor {host}:{port}...")

    while True:
        conn, addr = rec_socket.accept()
        packet = conn.recv(1024).decode('utf-8')
        
        if packet:
            try:
                data, method, incoming_control = packet.split('|')
            except ValueError:
                conn.close()
                continue

            computed_control = ""
            
            if method == "Parity":
                computed_control = calculate_parity(data, 'even')
            elif method == "Parity-Odd":
                computed_control = calculate_parity(data, 'odd')
            elif method == "2D Parity":
                computed_control = calculate_2d_parity(data)
            elif method == "CRC16":
                computed_control = calculate_crc(data)
            elif method == "Hamming":
                computed_control = calculate_hamming(data)
            
            print("\n" + "="*30)
            print(f"Received Data      : {data}")
            print(f"Method             : {method}")
            print(f"Sent Check Bits    : {incoming_control}")
            print(f"Computed Check Bits: {computed_control}")
            
            if incoming_control == computed_control:
                print("Status             : DATA CORRECT")
            else:
                print("Status             : DATA CORRUPTED")
            print("="*30 + "\n")

        conn.close()

if __name__ == "__main__":
    start_receiver()