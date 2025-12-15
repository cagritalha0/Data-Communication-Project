import socket
import random
import string

def apply_corruption(data_part, choice):
    if not data_part: return data_part
    
    data_list = list(data_part)
    length = len(data_list)

    if choice == '1':
        idx = random.randint(0, length - 1)
        char_code = ord(data_list[idx])
        bit_to_flip = 1 << random.randint(0, 6)
        data_list[idx] = chr(char_code ^ bit_to_flip)

    elif choice == '2':
        idx = random.randint(0, length - 1)
        new_char = random.choice(string.ascii_letters)
        data_list[idx] = new_char

    elif choice == '3':
        if length > 0:
            idx = random.randint(0, length - 1)
            data_list.pop(idx)

    elif choice == '4':
        idx = random.randint(0, length)
        char_to_add = random.choice(string.ascii_letters)
        data_list.insert(idx, char_to_add)

    elif choice == '5':
        if length >= 2:
            idx = random.randint(0, length - 2)
            data_list[idx], data_list[idx+1] = data_list[idx+1], data_list[idx]

    elif choice == '6':
        for _ in range(random.randint(2, 4)):
            idx = random.randint(0, len(data_list) - 1)
            char_code = ord(data_list[idx])
            bit_to_flip = 1 << random.randint(0, 6)
            data_list[idx] = chr(char_code ^ bit_to_flip)

    elif choice == '7':
        if length > 0:
            burst_len = random.randint(3, 8)
            start_idx = random.randint(0, max(0, length - burst_len))
            end_idx = min(length, start_idx + burst_len)
            for i in range(start_idx, end_idx):
                data_list[i] = 'X'

    return "".join(data_list)

def start_server():
    server_host = '127.0.0.1'
    server_port = 12345

    dest_host = '127.0.0.1'
    dest_port = 12346

    s_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s_socket.bind((server_host, server_port))
    s_socket.listen(1)

    print(f"[Server] Dinleniyor {server_host}:{server_port}...")
    
    conn, addr = s_socket.accept()
    print(f"[Bağlantı Kabul Edildi] Gönderici: {addr}")

    while True:
        try:
            packet = conn.recv(1024).decode('utf-8')
            if not packet: break

            parts = packet.split('|')
            if len(parts) < 3:
                continue
            
            raw_data = parts[0]
            method = parts[1]
            control = parts[2]

            print(f"\n--- Gelen Paket ---\nVeri: {raw_data}\nYöntem: {method}\nKontrol: {control}")

            print("\n[BOZMA MENÜSÜ]")
            print("0. Bozmadan İlet (No Error)")
            print("1. Bit Flip")
            print("2. Character Substitution")
            print("3. Character Deletion")
            print("4. Character Insertion")
            print("5. Character Swapping")
            print("6. Multiple Bit Flips")
            print("7. Burst Error")
            
            choice = input("Seçiminiz (0-7): ")

            corrupted_data = raw_data
            if choice != '0':
                corrupted_data = apply_corruption(raw_data, choice)

            final_packet = f"{corrupted_data}|{method}|{control}"

            try:
                sender_to_client2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sender_to_client2.connect((dest_host, dest_port))
                sender_to_client2.send(final_packet.encode('utf-8'))
                sender_to_client2.close()
                print(f"-> Client 2'ye iletildi: {final_packet}")
            except ConnectionRefusedError:
                print("HATA: Client 2 (Alıcı) çalışmıyor! Veri iletilemedi.")

        except Exception as e:
            print(f"Hata: {e}")
            break

    conn.close()
    s_socket.close()

if __name__ == "__main__":
    start_server()