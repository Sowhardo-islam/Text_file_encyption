import os
import re

# --- Load Encryption Formats ---
def load_formats(format_file="formats.txt"):
    """Loads encryption formats from a file, checking current and subdirectories."""
    formats = {}
    current_format = None

    # Search for the file in the current directory and subdirectories
    for root, dirs, files in os.walk(os.getcwd()):  # Walk through current directory and subdirectories
        if format_file in files:
            file_path = os.path.join(root, format_file)
            print(f"Found {format_file} in {root}")
            try:
                with open(file_path, "r", encoding="utf-8") as file:
                    for line in file:
                        line = line.strip()
                        if line.startswith("FORMAT"):
                            current_format = int(re.findall(r'\d+', line)[0])  # Extract format number
                            formats[current_format] = {}
                        elif "=" in line and current_format:
                            try:
                                key, value = map(str.strip, line.split("=", 1))  # Split only on the first '='
                                formats[current_format][key] = value.strip("()")  # Remove parentheses
                            except ValueError:
                                print(f"Skipping malformed line: {line}")
            except Exception as e:
                print(f"Error reading the file: {e}")
            break
    else:
        print(f"Error: {format_file} not found in the current directory or subdirectories.")

    return formats

# --- Encryption Function ---
def encrypt_text(text, mode, param, formats):
    """Encrypts text based on mode (Single or Multi) and format(s)."""
    if mode == 'S':  # Single encryption
        selected_format = formats.get(param, {})
        encrypted_text = ''.join(selected_format.get(char, char) for char in text)
    elif mode == 'M':  # Multi encryption (passes through multiple formats)
        encrypted_text = text
        for i in range(1, param + 1):
            selected_format = formats.get(i, {})
            encrypted_text = ''.join(selected_format.get(char, char) for char in encrypted_text)
    else:
        raise ValueError("Invalid mode. Use 'S' for single or 'M' for multi.")

    # Add encryption header/footer (e.g., "S1", "M3")
    header_footer = f"{mode}{param:02d}"  # Ensure always 2-digit format numbers
    return f"{header_footer}{encrypted_text}{header_footer}"

# --- Decryption Function ---
def decrypt_text(encrypted_text, formats):
    """Decrypts text based on the stored encryption header."""
    if len(encrypted_text) < 4:
        raise ValueError("Encrypted text is too short.")

    # Extract header and footer
    header, footer = encrypted_text[:3], encrypted_text[-3:]
    if header != footer:
        raise ValueError("Header/footer mismatch.")

    mode, param = header[0], int(header[1:])
    encrypted_body = encrypted_text[3:-3]  # Remove mode markers

    if mode == 'S':  # Single decryption
        decrypted_text = decrypt_with_format(encrypted_body, formats.get(param, {}))
    elif mode == 'M':  # Multi decryption (reverse multi-stage encryption)
        decrypted_text = encrypted_body
        for i in range(param, 0, -1):  # Reverse order decryption
            decrypted_text = decrypt_with_format(decrypted_text, formats.get(i, {}))
    else:
        raise ValueError("Invalid mode in header.")
    
    return decrypted_text

def decrypt_with_format(text, format_dict):
    """Decrypts text using a given format dictionary."""
    # Reverse the format mapping: encryption -> decryption
    reverse_format = {v: k for k, v in format_dict.items()}  # Reverse mapping
    decrypted_text = text

    # Ensure we replace the longest mappings first to avoid partial replacements
    for enc, dec in sorted(reverse_format.items(), key=lambda x: -len(x[0])):  # Longest first
        decrypted_text = decrypted_text.replace(enc, dec)
    
    return decrypted_text

# --- File Processing Functions ---
def encrypt_file():
    input_path = input("Enter the full path of the input text file: ").strip()
    if not os.path.exists(input_path):
        print("File not found. Please check the path.")
        return

    with open(input_path, 'r', encoding='utf-8') as infile:
        plain_text = infile.read().strip()

    formats = load_formats()  # Load encryption formats

    mode = input("Choose encryption mode - Single (S) or Multi (M): ").strip().upper()
    if mode not in ('S', 'M'):
        print("Invalid mode. Use 'S' or 'M'.")
        return

    try:
        param = int(input(f"Enter format number (1-{max(formats.keys())}): ").strip())
        if param not in formats:
            raise ValueError
    except ValueError:
        print("Invalid input. Choose a valid format.")
        return

    encrypted_text = encrypt_text(plain_text, mode, param, formats)

    output_path = os.path.join(os.path.dirname(input_path), "encrypt.txt")
    with open(output_path, 'w', encoding='utf-8') as outfile:
        outfile.write(encrypted_text)

    print(f"Encryption complete. File saved at: {output_path}")

def decrypt_file():
    input_path = input("Enter the full path of the encrypted file: ").strip()
    if not os.path.exists(input_path):
        print("File not found. Please check the path.")
        return

    with open(input_path, 'r', encoding='utf-8') as infile:
        encrypted_text = infile.read().strip()

    formats = load_formats()  # Load encryption formats

    try:
        decrypted_text = decrypt_text(encrypted_text, formats)
    except Exception as ex:
        print("Error during decryption:", ex)
        return

    output_path = os.path.join(os.path.dirname(input_path), "decrypt.txt")
    with open(output_path, 'w', encoding='utf-8') as outfile:
        outfile.write(decrypted_text)

    print(f"Decryption complete. File saved at: {output_path}")

# --- Main Program ---
def main():
    print("Custom File Encryption/Decryption Script")
    print("----------------------------------------")
    choice = input("Do you want to (e)ncrypt or (d)ecrypt? ").strip().lower()
    if choice.startswith('e'):
        encrypt_file()
    elif choice.startswith('d'):
        decrypt_file()
    else:
        print("Invalid choice. Please run the script again.")

if __name__ == '__main__':
    main()
