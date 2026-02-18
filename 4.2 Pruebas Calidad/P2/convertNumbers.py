"""
convertNumbers.py
Converts numbers to Binary and Hexadecimal using Two's Complement logic.
Features a configurable bit-width (default 32-bit).
""" #pylint: disable=invalid-name

import sys
import time

# CONFIGURATION: Change this variable to 16, 32, etc., to update the bit-width
BIT_WIDTH = 32


def to_binary_twos_complement(num, bits):
    """Converts a decimal to Two's Complement binary string."""
    # Create a mask for the specified bit-width
    # Example for 10 bits: (1 << 10) is 1024, mask is 1023 (all 1s in binary)
    mask = (1 << bits) - 1

    # Apply the mask to handle negative numbers automatically
    # This effectively performs (num + 2^bits) % 2^bits
    masked_num = num & mask

    if masked_num == 0:
        return "0" * bits

    binary_digits = ""
    # We loop exactly 'bits' times to ensure fixed-width padding
    for _ in range(bits):
        remainder = masked_num % 2
        binary_digits = str(remainder) + binary_digits
        masked_num = masked_num // 2

    return binary_digits


def to_hex_twos_complement(num, bits):
    """Converts a decimal to Two's Complement hexadecimal string."""
    mask = (1 << bits) - 1
    masked_num = num & mask

    if masked_num == 0:
        # Calculate how many hex chars needed (e.g., 10 bits = 3 hex chars)
        hex_len = (bits + 3) // 4
        return "0" * hex_len

    hex_chars = "0123456789ABCDEF"
    hex_digits = ""

    # 4 bits per hexadecimal character
    hex_len = (bits + 3) // 4
    for _ in range(hex_len):
        remainder = masked_num % 16
        hex_digits = hex_chars[remainder] + hex_digits
        masked_num = masked_num // 16

    return hex_digits


def process_file(filename):
    """Reads data and performs manual conversions."""
    results = []
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            for line in file:
                clean_item = line.strip()
                if not clean_item:
                    continue
                try:
                    # Convert to float then int
                    number = int(float(clean_item))

                    # Check for overflow/underflow for the current BIT_WIDTH
                    limit = 1 << (BIT_WIDTH - 1)
                    if number < -limit or number >= limit:
                        print(f"Warning: {number} exceeds {BIT_WIDTH}-bit range.")

                    bin_val = to_binary_twos_complement(number, BIT_WIDTH)
                    hex_val = to_hex_twos_complement(number, BIT_WIDTH)
                    results.append((clean_item, bin_val, hex_val))
                except ValueError:
                    print(f"Error: Invalid numeric data: '{clean_item}' -> Writing #VALUE!")
                    # Append a tuple with 3 values so the main loop doesn't crash
                    results.append((clean_item, "#VALUE!", "#VALUE!"))
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        return None
    return results


def main():
    """Main execution flow."""
    start_time = time.time()

    if len(sys.argv) != 2:
        print("Usage: python convertNumbers.py <fileWithData.txt>")
        return

    input_file = sys.argv[1]
    data_results = process_file(input_file)

    if data_results is None:
        return

    elapsed_time = time.time() - start_time

    # Formatting Results
    output_lines = [
        f"Results for {input_file} ({BIT_WIDTH}-bit Two's Complement)",
        "-" * 60,
        f"{'ITEM':<15} {'BINARY':<20} {'HEXADECIMAL':<15}",
        "-" * 60
    ]

    for item, b_val, h_val in data_results:
        output_lines.append(f"{item:<15} {b_val:<20} {h_val:<15}")

    output_lines.append(f"\nTotal Execution Time: {elapsed_time:.6f} seconds")
    final_output = "\n".join(output_lines)

    print(final_output)
    with open("tests/ConvertionResults.txt", "w", encoding="utf-8") as out_file:
        out_file.write(final_output + "\n")


if __name__ == "__main__":
    main()
