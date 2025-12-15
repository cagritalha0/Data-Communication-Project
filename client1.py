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

def start_client():
    host = '127.0.0.1'
    port = 12345

    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((host, port))
        print(f"[Bağlandı] Server: {host}:{port}")

        while True:
            data = input("\nGönderilecek mesajı girin (Çıkış için 'exit'): ")
            if data.lower() == 'exit':
                break

            print("\n--- Yöntem Seçimi ---")
            print("1. Parity (Even)")
            print("2. Parity (Odd)")
            print("3. 2D Parity")
            print("4. CRC-16")
            print("5. Hamming Code")
            choice = input("Seçiminiz (1-5): ")

            method = ""
            control_info = ""

            if choice == '1':
                method = "Parity"
                control_info = calculate_parity(data, 'even')
            elif choice == '2':
                method = "Parity-Odd"
                control_info = calculate_parity(data, 'odd')
            elif choice == '3':
                method = "2D Parity"
                control_info = calculate_2d_parity(data)
            elif choice == '4':
                method = "CRC16"
                control_info = calculate_crc(data)
            elif choice == '5':
                method = "Hamming"
                control_info = calculate_hamming(data)
            else:
                method = "Parity"
                control_info = calculate_parity(data, 'even')

            packet = f"{data}|{method}|{control_info}"
            client_socket.send(packet.encode('utf-8'))
            print(f"-> Gönderilen Paket: {packet}")

    except Exception as e:
        print(f"Hata: {e}")
    finally:
        client_socket.close()

if __name__ == "__main__":
    start_client()