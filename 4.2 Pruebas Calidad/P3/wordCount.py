"""
wordCount.py
A tool to count distinct words in a file and calculate their frequency.
Results are printed to the console and saved to WordCountResults.txt.
""" #pylint: disable=invalid-name

import sys
import time

def manual_sort(data):
    """
    Implementation of Bubble Sort to sort a list of items alphabetically.
    Used to ensure the output is deterministic and ordered.
    """
    n = 0
    # Calculate length manually
    for _ in data:
        n += 1

    arr = list(data)
    # Basic Bubble Sort algorithm
    for i in range(n):
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr


def read_file(filename):
    """
    Reads the file and extracts words.
    Handles specific file system and encoding errors.
    """
    words = []
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            for line in file:
                clean_line = line.strip()
                if not clean_line:
                    continue

                # Split line into words
                line_words = clean_line.split()
                for word in line_words:
                    # Basic sanitization
                    # Treat words as case-insensitive (optional but standard)
                    # or strictly as they appear. The samples provided suggests exact match.
                    words.append(word)

    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        return None
    # CHANGE IS HERE: Catch specific IO and Encoding errors
    except (OSError, UnicodeDecodeError) as e:
        print(f"Error reading file: {e}")
        return None

    return words

def count_frequencies(word_list):
    """
    Counts the frequency of each word.
    """
    frequency_map = {}

    for word in word_list:
        if word in frequency_map:
            frequency_map[word] += 1
        else:
            frequency_map[word] = 1

    return frequency_map

def main():
    """Main execution flow."""
    start_time = time.time()

    # 1. Validate Arguments
    if len(sys.argv) != 2:
        print("Usage: python wordCount.py <fileWithData.txt>")
        return

    input_file = sys.argv[1]

    # 2. Read Data
    words = read_file(input_file)
    if words is None:
        return # Exit if file error occurred

    if not words:
        print("Info: File is empty or contains no valid words.")
        return

    # 3. Calculate Frequencies
    freq_map = count_frequencies(words)

    # 4. Sort Results (Alphabetical order for consistency)
    # Extract keys, sort them manually, then lookup the count.
    distinct_words = list(freq_map.keys())
    sorted_words = manual_sort(distinct_words)

    elapsed_time = time.time() - start_time

    # 5. Format Output
    results = []
    header = f"{'WORD':<20} {'COUNT'}"
    results.append(header)
    results.append("-" * 30)

    total_count = 0
    for word in sorted_words:
        count = freq_map[word]
        total_count += count
        results.append(f"{word:<20} {count}")

    # Add Grand Total
    results.append("-" * 30)
    results.append(f"{'Grand Total':<20} {total_count}")
    results.append("-" * 30)
    results.append(f"Execution Time: {elapsed_time:.4f} seconds")

    final_output = "\n".join(results)

    # 6. Print and Save
    print(final_output)

    try:
        with open("tests/WordCountResults.txt", "w", encoding="utf-8") as f:
            f.write(final_output)
        print("\nResults saved to WordCountResults.txt")
    except OSError as e:
        print(f"Error writing results: {e}")

if __name__ == "__main__":
    main()
