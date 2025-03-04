import random

# Define the allowed characters:
allowed_chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()_+=-[]\\';,./?><:\"|}{"

def random_code():
    # Generate a 4-character string from the allowed pool
    return ''.join(random.choice(allowed_chars) for _ in range(4))

# Generate 100 formats
for i in range(1, 101):
    print(f"FORMAT {i}:")
    
    # Iterate through the character groups to generate and print random codes
    for char in "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789abcdefghijklmnopqrstuvwxyz!@#$%^&*()_+=-[]\\';,./?><:\"|}{":
        print(f"{char} = ({random_code()})")
    
    print()  # Outputs a single empty line
