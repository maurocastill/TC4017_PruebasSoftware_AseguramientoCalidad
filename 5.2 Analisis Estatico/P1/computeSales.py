"""
computeSales.py
Tool to calculate total sales cost from a product catalogue and sales records.
"""  # pylint: disable=invalid-name

import json
import sys
import time


def load_json_file(filename):
    """
    Loads a JSON file and returns the data.
    Handles specific I/O and JSON errors to satisfy Pylint.
    """
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Error: The file '{filename}' was not found.")
        return None
    except json.JSONDecodeError:
        print(f"Error: The file '{filename}' contains invalid JSON.")
        return None
    except OSError as e:
        print(f"Error: OS error occurred reading '{filename}': {e}")
        return None


def build_price_map(catalogue_data):
    """
    Converts the product list into a dictionary for O(1) access time.
    Returns: dict {product_title: price}
    """
    price_map = {}
    if not isinstance(catalogue_data, list):
        print("Error: Invalid catalogue format. Expected a list of products.")
        return price_map

    for item in catalogue_data:
        title = item.get("title")
        price = item.get("price")

        if title is not None and isinstance(price, (int, float)):
            price_map[title] = price
        else:
            print(f"Warning: Skipped invalid item in catalogue: {item}")

    return price_map


def compute_total_cost(price_map, sales_data):
    """
    Iterates through sales records and calculates total cost.
    Returns: tuple (total_cost, error_list)
    """
    total_cost = 0.0
    errors = []

    if not isinstance(sales_data, list):
        msg = "Error: Invalid sales format. Expected a list of sales."
        print(msg)
        errors.append(msg)
        return 0.0, errors

    for sale in sales_data:
        product = sale.get("Product")
        quantity = sale.get("Quantity")

        # Validation: Check if product exists and quantity is a number
        if product not in price_map:
            msg = f"Error: Product '{product}' not found in price catalogue."
            errors.append(msg)
            continue

        if not isinstance(quantity, (int, float)):
            msg = f"Error: Invalid quantity for product '{product}'."
            print(msg)
            errors.append(msg)
            continue

        item_price = price_map[product]
        total_cost += item_price * quantity

    return total_cost, errors


def main():
    """
    Main execution function.
    Handles argument parsing, timing, and output generation.
    """
    start_time = time.time()

    # 1. Validation: Check command line arguments
    if len(sys.argv) != 3:
        print("Usage: python computeSales.py priceCatalogue.json "
              "salesRecord.json")
        sys.exit(1)

    price_file = sys.argv[1]
    sales_file = sys.argv[2]

    # 2. Load Data
    catalogue_data = load_json_file(price_file)
    sales_data = load_json_file(sales_file)

    if catalogue_data is None or sales_data is None:
        sys.exit(1)

    # 3. Process Data
    price_map = build_price_map(catalogue_data)

    # Calculate Total and catch errors
    total_cost, error_log = compute_total_cost(price_map, sales_data)

    # 4. Final Timing and Output
    end_time = time.time()
    elapsed_time = end_time - start_time

    # Format output string
    result_lines = [
        "Sales Report",
        "-" * 30,
        f"Total Cost: ${total_cost:,.2f}",
        f"Execution Time: {elapsed_time:.6f} seconds",
        "-" * 30
    ]

    # Append errors to the output if any exist
    if error_log:
        result_lines.append("\nErrors detected during processing:")
        result_lines.extend(error_log)
        result_lines.append("-" * 30)

    output_string = "\n".join(result_lines)

    print(output_string)

    # Write to File
    try:
        with open("results/SalesResults.txt", "w", encoding='utf-8') as f:
            f.write(output_string)
    except OSError as e:
        print(f"Error writing to results file: {e}")


if __name__ == "__main__":
    main()
