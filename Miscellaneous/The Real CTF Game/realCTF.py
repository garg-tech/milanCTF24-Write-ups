from pwn import *

# Adjust these variables for your server details
HOST = 'milanctf.kludge.co.in'  # Replace with the server address
PORT = 4560  # Replace with the server port

def main():
    # Start connection with the server at the specified HOST and PORT
    conn = remote(HOST, PORT)
    
    # Read the initial welcome message until the prompt for the first move
    print(conn.recvuntil(b'Enter your first move:\n'))
    
    # Initial player position (X, Y) on the grid
    playerX, playerY = 0, 0

    # Try every cell in a grid of 381x381 to find the correct key position
    for keyY in range(0, 381):  # Loop through all possible Y positions
        # If the player is not at the leftmost side, move them to the start of the row (X=0)
        while playerX:
            conn.sendline(b'a')  # Move left
            playerX -= 1
        
        # Now try each X position in the current row (keyY)
        for keyX in range(0, 381):  # Loop through all possible X positions
            # Move vertically downwards until the player is at the target Y (keyY)
            while playerY < keyY:
                conn.sendline(b's')  # Move down
                playerY += 1

            # Move horizontally rightwards until the player is at the target X (keyX)
            while playerX < keyX:
                conn.sendline(b'd')  # Move right
                playerX += 1

            # Attempt to capture the flag at the current player position (playerX, playerY)
            print(f"Trying to capture at: ({playerX}, {playerY})")
            
            # Send 'y' to attempt to capture the flag
            conn.sendlineafter(b'Press \'y\' to capture the flag.\n', b'y', timeout = 0.01)
            
            # Get the response from the server after trying to capture the flag
            response = conn.recvline()
        
            # If the flag capture is successful, the success message is found in the response
            if b'Congratulations! You\'ve captured the flag.\n' in response:
                print(response)  # Print the success message

                # Send 'y' to confirm and proceed after capturing the flag
                conn.sendline(b'y')

                # Now move the player to the exit of the grid (bottom-right corner at (455, 455))
                while playerY < 455:
                    conn.sendline(b's')  # Move down to the bottom
                    playerY += 1

                while playerX < 455:
                    conn.sendline(b'd')  # Move right to the far right side
                    playerX += 1

                # Receive the final response (likely indicating the game end) and print it
                response = conn.recvall()
                print(response)
                
                # Close the connection after successfully capturing the flag and reaching the exit
                conn.close()
                return

    # If no key position works after all attempts, print a failure message and close the connection
    print("Failed to capture the flag.")
    conn.close()

# Entry point for the script
if __name__ == '__main__':
    main()
