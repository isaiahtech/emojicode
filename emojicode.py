import sys

def byte_to_variation_selector(byte: int) -> str:
    """Turns a number (0-255) into a special Unicode character (a variation selector)."""
    if not 0 <= byte <= 255:
        raise ValueError("Byte value must be between 0 and 255")

    if byte < 16:
        # Use the first set of variation selectors.
        return chr(0xFE00 + byte)
    else:
        # Use the second, larger set of variation selectors.
        return chr(0xE0100 + (byte - 16))

def variation_selector_to_byte(char: str) -> int:
    """Converts a variation selector character back into its original number (0-255)."""
    codepoint = ord(char)

    if 0xFE00 <= codepoint <= 0xFE0F:
        # It's from the first set of variation selectors.
        return codepoint - 0xFE00
    elif 0xE0100 <= codepoint <= 0xE01EF:
        # It's from the second set.
        return (codepoint - 0xE0100) + 16
    else:
        raise ValueError("Not a valid variation selector character")

def encode(base_char: str, data: bytes) -> str:
    """Hides a sequence of bytes within a string by adding variation selectors."""
    result = base_char
    for byte in data:
        # Add the variation selector for each byte to the base character.
        result += byte_to_variation_selector(byte)
    return result

def decode(encoded_string: str) -> bytes:
    """Extracts the hidden bytes from a string containing variation selectors."""
    if not encoded_string:
        return b""  # Nothing to decode

    # Skip the first character (the base character), we only want the selectors.
    variation_selectors = encoded_string[1:]
    decoded_bytes = bytearray()

    for char in variation_selectors:
        try:
            # Convert each variation selector back to its byte value.
            decoded_bytes.append(variation_selector_to_byte(char))
        except ValueError:
            pass  # Ignore characters that aren't variation selectors.

    return bytes(decoded_bytes)

def main():
    """Main function: asks the user if they want to encode or decode, then does it."""

    while True:  # Keep going until the user wants to quit
        choice = input("Do you want to (e)ncode or (d)ecode? (Enter 'e' or 'd', or 'q' to quit): ").lower()

        if choice == 'e':
            # --- Encoding ---
            base_character = "😊"  # Pick a starting emoji

            print("Enter the text you want to encode (press Ctrl+D (Unix/Linux) or Ctrl+Z (Windows) on an empty line to finish):")
            lines = []
            # Read input line by line until the user signals the end.
            while True:
                try:
                    line = input()
                    lines.append(line)
                except EOFError:
                    break
            input_text = "\n".join(lines)  # Combine the lines into a single string

            if not input_text:
                print("No input provided.  Please try again.\n")
                continue

            # Convert the text to bytes, then encode it.
            input_bytes = input_text.encode('utf-8')
            encoded_string = encode(base_character, input_bytes)

            print("\nEncoded emoji (copy and paste this):")
            print(encoded_string)

        elif choice == 'd':
            # --- Decoding ---
            print("Paste the encoded emoji here (press Enter):")
            encoded_string = input()

            if not encoded_string:
                print("No input provided. Please try again.\n")
                continue

            # Decode the string back into bytes.
            decoded_bytes = decode(encoded_string)
            try:
                # Try to convert the bytes back into text (assuming UTF-8).
                decoded_text = decoded_bytes.decode('utf-8')
                print("\nDecoded text:")
                print(decoded_text)
            except UnicodeDecodeError:
                # If it's not valid UTF-8, just show the raw bytes.
                print("\nDecoded bytes (could not decode as UTF-8):")
                print(decoded_bytes)

        elif choice == 'q':
            break  # Quit the program

        else:
            print("Invalid choice. Please enter 'e', 'd', or 'q'.\n")

if __name__ == "__main__":
    main()
