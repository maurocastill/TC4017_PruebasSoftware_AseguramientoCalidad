"""
computeStatistics.py
A tool to calculate descriptive statistics from a file.
Matches Excel's COUNTA, AVERAGE, MEDIAN, MODE, STDEVP, and VAR.S.
""" #pylint: disable=invalid-name

import sys
import time
import os


def manual_sort(data):
    """Implementation of Bubble Sort."""
    n = 0
    for _ in data:
        n += 1

    arr = list(data)
    for i in range(n):
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr


def get_mode(valid_numbers, counts):
    """Calculates the mode based on frequency counts."""
    max_freq = 0
    for freq in counts.values():
        if freq > max_freq:
            max_freq = freq

    if max_freq <= 1:
        return "#N/A"

    for item in valid_numbers:
        if counts[item] == max_freq:
            return item
    return "#N/A"


def read_data(filename):
    """Reads file and returns valid numbers and total count."""
    valid_numbers = []
    count_a = 0
    with open(filename, 'r', encoding='utf-8') as file:
        for line in file:
            clean_line = line.strip('\n\r')
            if clean_line != "":
                count_a += 1
            try:
                if clean_line.strip():
                    valid_numbers.append(float(clean_line))
            except ValueError:
                if clean_line.strip():
                    print(f"Error: Invalid numeric data: '{clean_line}'")
    return valid_numbers, count_a


def calculate_stats(valid_numbers):
    """Computes the required descriptive statistics."""
    n_valid = 0
    total_sum = 0
    counts = {}
    for val in valid_numbers:
        n_valid += 1
        total_sum += val
        counts[val] = counts.get(val, 0) + 1

    mean = total_sum / n_valid
    sorted_data = manual_sort(valid_numbers)
    mid = n_valid // 2
    median = (sorted_data[mid - 1] + sorted_data[mid]) / 2 if n_valid % 2 == 0 \
        else sorted_data[mid]

    mode = get_mode(valid_numbers, counts)

    sum_sq_diff = 0
    for number in valid_numbers:
        sum_sq_diff += (number - mean) ** 2

    variance = sum_sq_diff / (n_valid - 1) if n_valid > 1 else 0
    std_dev = (sum_sq_diff / n_valid) ** 0.5

    return mean, median, mode, std_dev, variance


def main():
    """Main execution flow."""
    start_time = time.time()
    if len(sys.argv) != 2:
        print("Usage: python computeStatistics.py <fileWithData.txt>")
        return

    try:
        valid_numbers, count_a = read_data(sys.argv[1])
        if not valid_numbers:
            print("Error: No valid numeric data found.")
            return

        mean, median, mode, std_p, var_s = calculate_stats(valid_numbers)
        elapsed_time = time.time() - start_time

        output = (
            f"Results for {sys.argv[1]}\n"
            f"------------------------------\n"
            f"Count:      {count_a}\n"
            f"Mean:       {mean:.4f}\n"
            f"Median:     {median:.4f}\n"
            f"Mode:       {mode}\n"
            f"SD.P:       {std_p:.4f}\n"
            f"Variance.S: {var_s:.4f}\n"
            f"Time:       {elapsed_time:.6f} seconds\n"
        )

        print(output)
        os.makedirs("results", exist_ok=True)
        with open("tests/StatisticsResults.txt", "w", encoding="utf-8") as f:
            f.write(output + "\n")

    except FileNotFoundError:
        print(f"Error: File '{sys.argv[1]}' not found.")


if __name__ == "__main__":
    main()
