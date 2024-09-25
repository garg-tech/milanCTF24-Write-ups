from pwn import *

# Adjust these variables for your server details
HOST = 'milanctf.kludge.co.in'  # Replace with the server address
PORT = 4560  # Replace with the server port

def main():
    # Start connection
    conn = remote(HOST, PORT)
    
    # Read the welcome message
    print(conn.recvuntil(b'Enter your first move:\n'))
    playerX, playerY = 0, 0

    # Try each cell in the key position range
    for keyY in range(0, 381):
        while playerX:
            conn.sendline(b'a')
            playerX -= 1
        for keyX in range(0, 381):            
            # Move to the key position (keyX, keyY)
            while playerY < keyY:
                conn.sendline(b's')  # Move down
                playerY += 1

            while playerX < keyX:
                conn.sendline(b'd')  # Move right
                playerX += 1

            # Check if we can capture the flag
            print(f"Trying to capture at: ({playerX}, {playerY})")
            conn.sendlineafter(b'Press \'y\' to capture the flag.\n', b'y', timeout = 0.01)  # Attempt to capture the flag
            response = conn.recvline()
        
            if b'Congratulations! You\'ve captured the flag.\n' in response:
                print(response)
                conn.sendline(b'y')
                # Now move to the exit
                while playerY < 455:
                    conn.sendline(b's')  # Move down to the bottom
                    playerY += 1

                while playerX < 455:
                    conn.sendline(b'd')  # Move right to the end
                    playerX += 1

                response = conn.recvall()
                print(response)
                conn.close()
                return


    print("Failed to capture the flag.")
    conn.close()

if __name__ == '__main__':
    main()
