import argparse
import csv
import os
from datetime import datetime, timedelta

def calculate_expiration_date(production_date, shelf_life):
    return production_date + timedelta(days=shelf_life)

def write_to_history_csv(file_name, data):
    with open(file_name, 'a', newline='') as csv_file:
        writer = csv.writer(csv_file)

        # Check if the file is empty
        if os.stat(file_name).st_size == 0:
            writer.writerow(["SKU", "Name", "Brand", "Expiration Date"])

        writer.writerow(data)


def write_to_expiry_report(file_name, data, days):
    today = datetime.now().date()
    within_days = []

    with open(file_name, 'r') as csv_file:
        reader = csv.reader(csv_file)
        existing_entries = set(tuple(row) for row in reader)

    for row in data:
        expiration_date = datetime.strptime(row[3], "%Y-%m-%d").date()
        if (expiration_date - today) <= timedelta(days=days):
            unique_row = tuple(row)
            if unique_row not in existing_entries:
                within_days.append(row)
                existing_entries.add(unique_row)

    with open(file_name, 'a', newline='') as csv_file:
        writer = csv.writer(csv_file)
        if len(existing_entries) == 0:
            writer.writerow(["SKU", "Name", "Brand", "Expiration Date"])
        writer.writerows(within_days)


def generate_expiry_report(file_name, days):
    today = datetime.now().date()
    within_days = []

    with open(file_name, 'r') as csv_file:
        reader = csv.reader(csv_file)
        try:
            header = next(reader)  # Read the header row
        except StopIteration:
            print("No data found in the CSV file.")
            return

        existing_entries = set(tuple(row) for row in reader)

    with open('expiryreport.csv', 'w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(["SKU", "Name", "Brand", "Expiration Date"])  # Add the header row
        for row in existing_entries:
            expiration_date = datetime.strptime(row[3], "%Y-%m-%d").date()
            if (expiration_date - today) <= timedelta(days=days):
                within_days.append(row)
        writer.writerows(within_days)




def remove_expired_entries(history_file, expiry_file):
    history_data = []
    expiry_skus = set()

    # Read the expiry report file and store SKUs
    with open(expiry_file, 'r') as expiry_csv:
        reader = csv.reader(expiry_csv)
        next(reader)  # Skip header row
        for row in reader:
            expiry_skus.add(row[0])

    # Read the history file and filter out expired entries
    with open(history_file, 'r') as history_csv:
        reader = csv.reader(history_csv)
        header = next(reader)  # Read the header row
        history_data.append(header)
        for row in reader:
            sku = row[0]
            if sku not in expiry_skus:
                history_data.append(row)

    # Write the updated history data to the history file
    with open(history_file, 'w', newline='') as history_csv:
        writer = csv.writer(history_csv)
        writer.writerows(history_data)

    # Clear the expiry report file
    if os.path.exists(expiry_file):
        with open(expiry_file, 'w', newline='') as expiry_csv:
            pass  # Simply opening the file in write mode clears its contents

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("csv_file", help="CSV file containing SKUs", nargs="?")
    parser.add_argument("production_date", help="Production date (YYYY-MM-DD)", nargs="?")
    parser.add_argument("--days", type=int, default=3, help="Threshold for number of days until expiration", nargs="?")
    parser.add_argument("--remove-expired", action="store_true", help="Remove expired entries from history.csv and clear the expiry report file")
    args = parser.parse_args()

    # Load shelf life data from shelflife.csv
    shelf_life_data = {}
    with open('shelflife.csv', 'r') as shelf_life_file:
        reader = csv.reader(shelf_life_file)
        next(reader)  # Skip header row
        for row in reader:
            sku = row[0]
            name = row[1]
            brand = row[2]
            shelf_life = int(row[3])
            shelf_life_data[sku] = (name, brand, shelf_life)

    # Calculate expiration date and write to history.csv
    history_data = []
    if args.csv_file and args.production_date:
        with open(args.csv_file, 'r') as csv_file:
            reader = csv.reader(csv_file)
            next(reader)  # Skip header row
            for row in reader:
                sku = row[0]
                name = shelf_life_data.get(sku, ("Unknown", "Unknown", 0))[0]
                brand = shelf_life_data.get(sku, ("Unknown", "Unknown", 0))[1]
                shelf_life = shelf_life_data.get(sku, ("Unknown", "Unknown", 0))[2]
                production_date = datetime.strptime(args.production_date, "%Y-%m-%d").date()
                expiration_date = calculate_expiration_date(production_date, shelf_life)
                data = [sku, name, brand, expiration_date.strftime("%Y-%m-%d")]
                write_to_history_csv('history.csv', data)
                history_data.append(data)

        # Update expiry report with within specified days data
        write_to_expiry_report('expiryreport.csv', history_data, args.days)
    else:
        # Generate expiry report from history.csv if no SKUs and production date provided
        generate_expiry_report('history.csv', args.days)

    if args.remove_expired:
        remove_expired_entries('history.csv', 'expiryreport.csv')
        print("Expired entries removed from history.csv")
        print("Expiry report cleared")

if __name__ == "__main__":
    main()
