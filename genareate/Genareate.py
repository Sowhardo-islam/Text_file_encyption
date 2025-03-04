import random

# Define the allowed characters:
allowed_chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()_+=-[]\\';,./?><:\"|}{"

def random_code():
    # Generate a 4-character string from the allowed pool
    return ''.join(random.choice(allowed_chars) for _ in range(4))

# Open a file to save the output in write mode (this will overwrite the file if it exists)
with open('formats.txt', 'w') as file:
    # Generate 100 formats
    for i in range(1, 101):
        file.write(f"FORMAT {i}:\n")
        
        # Iterate through the character groups to generate and print random codes
        for char in "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789abcdefghijklmnopqrstuvwxyz!@#$%^&*()_+=-[]\\';,./?><:\"|}{":
            file.write(f"{char} = ({random_code()})\n")
        
        file.write("\n")  # Adds a single empty line after each format block
