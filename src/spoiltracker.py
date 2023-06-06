import argparse
import csv
from datetime import datetime, timedelta


class ErrorMessages:
    @staticmethod
    def file_not_found(file_path):
        print(f"Error: File '{file_path}' not found.")

    @staticmethod
    def invalid_date_format(date):
        print(f"Error: Invalid date format: {date}")

    @staticmethod
    def no_data_found():
        print("Error: No data found in the CSV file.")


class ExpiryTracker:
    def __init__(self, shelf_life_file='shelflife.csv', history_file='history.csv',
                 expiry_report_file='expiryreport.csv'):
        self.shelf_life_file = shelf_life_file
        self.history_file = history_file
        self.expiry_report_file = expiry_report_file
        self.shelf_life_data = {}

    def load_shelf_life_data(self):
        try:
            with open(self.shelf_life_file, 'r') as shelf_life_file:
                reader = csv.reader(shelf_life_file)
                next(reader)  # Skip header row
                for row in reader:
                    sku = row[0]
                    name = row[1]
                    brand = row[2]
                    shelf_life = int(row[3])
                    self.shelf_life_data[sku] = (name, brand, shelf_life)
        except FileNotFoundError:
            ErrorMessages.file_not_found(self.shelf_life_file)

    def calculate_expiration_date(self, production_date, shelf_life):
        return production_date + timedelta(days=shelf_life)

    def write_to_history_csv(self, data):
        try:
            with open(self.history_file, 'a', newline='') as history_csv:
                writer = csv.writer(history_csv)
                writer.writerow(data)

            # Read the entire history file
            with open(self.history_file, 'r') as history_csv:
                reader = csv.reader(history_csv)
                header = next(reader)  # Read the header row
                rows = list(reader)

            # Sort the rows by expiration date
            rows.sort(key=lambda row: datetime.strptime(row[3], "%Y-%m-%d"))

            # Write the sorted rows back to the history file
            with open(self.history_file, 'w', newline='') as history_csv:
                writer = csv.writer(history_csv)
                writer.writerow(header)
                writer.writerows(rows)

        except FileNotFoundError:
            ErrorMessages.file_not_found(self.history_file)


    def write_to_expiry_report(self, data, days, expiry_report_dest=None):
        if expiry_report_dest is None:
            expiry_report_dest = self.expiry_report_file

        today = datetime.now().date()
        within_days = []

        try:
            with open(expiry_report_dest, 'a', newline='') as expiry_csv:
                writer = csv.writer(expiry_csv)
                existing_entries = set()
                try:
                    with open(expiry_report_dest, 'r') as existing_csv:
                        reader = csv.reader(existing_csv)
                        existing_entries = set(tuple(row) for row in reader)
                except FileNotFoundError:
                    pass

                for row in data:
                    try:
                        expiration_date = datetime.strptime(row[3], "%Y-%m-%d").date()
                        if (expiration_date - today) <= timedelta(days=days):
                            unique_row = tuple(row)
                            if unique_row not in existing_entries:
                                within_days.append(row)
                                existing_entries.add(unique_row)
                    except ValueError:
                        ErrorMessages.invalid_date_format(row[3])

                # Append new records to the existing expiry report
                writer.writerows(within_days)
        except FileNotFoundError:
            ErrorMessages.file_not_found(expiry_report_dest)

        # Sort the expiry report by expiration date
        self.sort_expiry_report(expiry_report_dest)

    def sort_expiry_report(self, expiry_report_dest):
        try:
            with open(expiry_report_dest, 'r') as expiry_csv:
                rows = list(csv.reader(expiry_csv))
                # Sort the rows by the expiration date (index 3)
                sorted_rows = sorted(rows[1:], key=lambda row: datetime.strptime(row[3], "%Y-%m-%d").date())

            with open(expiry_report_dest, 'w', newline='') as expiry_csv:
                writer = csv.writer(expiry_csv)
                writer.writerow(rows[0])  # Write the header row
                writer.writerows(sorted_rows)
        except FileNotFoundError:
            ErrorMessages.file_not_found(expiry_report_dest)

    def generate_expiry_report(self, days, expiry_report_dest=None):
        if expiry_report_dest is None:
            expiry_report_dest = self.expiry_report_file

        today = datetime.now().date()
        within_days = []

        try:
            with open(self.history_file, 'r') as history_csv:
                reader = csv.reader(history_csv)
                try:
                    header = next(reader)  # Read the header row
                except StopIteration:
                    ErrorMessages.no_data_found()
                    return
                existing_entries = set(tuple(row) for row in reader)
        except FileNotFoundError:
            ErrorMessages.file_not_found(self.history_file)
            return

        for row in existing_entries:
            try:
                expiration_date = datetime.strptime(row[3], "%Y-%m-%d").date()
                if (expiration_date - today) <= timedelta(days=days):
                    within_days.append(row)
            except ValueError:
                ErrorMessages.invalid_date_format(row[3])

        try:
            with open(expiry_report_dest, 'w', newline='') as expiry_csv:
                writer = csv.writer(expiry_csv)
                writer.writerow(["SKU", "Name", "Brand", "Expiration Date"])  # Add the header row
                writer.writerows(within_days)
        except FileNotFoundError:
            ErrorMessages.file_not_found(expiry_report_dest)

        # Sort the expiry report by expiration date
        self.sort_expiry_report(expiry_report_dest)

    def remove_expired_entries(self):
        history_data = []
        expiry_skus = set()

        # Read the expiry report file and store SKUs
        try:
            with open(self.expiry_report_file, 'r') as expiry_csv:
                reader = csv.reader(expiry_csv)
                next(reader)  # Skip header row
                for row in reader:
                    expiry_skus.add(row[0])
        except FileNotFoundError:
            ErrorMessages.file_not_found(self.expiry_report_file)
            return

        # Read the history file and filter out expired entries
        try:
            with open(self.history_file, 'r') as history_csv:
                reader = csv.reader(history_csv)
                header = next(reader)  # Read the header row
                history_data.append(header)
                for row in reader:
                    sku = row[0]
                    if sku not in expiry_skus:
                        history_data.append(row)
        except FileNotFoundError:
            ErrorMessages.file_not_found(self.history_file)
            return

        # Write the updated history data to the history file
        try:
            with open(self.history_file, 'w', newline='') as history_csv:
                writer = csv.writer(history_csv)
                writer.writerows(history_data)
        except FileNotFoundError:
            ErrorMessages.file_not_found(self.history_file)

        # Clear the expiry report file
        try:
            with open(self.expiry_report_file, 'w', newline=''):
                pass  # Simply opening the file in write mode clears its contents
        except FileNotFoundError:
            ErrorMessages.file_not_found(self.expiry_report_file)

    def clear_history_file(self):
        try:
            with open(self.history_file, 'w', newline=''):
                pass  # Simply opening the file in write mode clears its contents
        except FileNotFoundError:
            ErrorMessages.file_not_found(self.history_file)

    def process_csv(self, csv_file_path, prod_date):
        history_data = []
        try:
            with open(csv_file_path, 'r') as csv_file:
                reader = csv.reader(csv_file)
                next(reader)  # Skip header row
                for row in reader:
                    sku = row[0]
                    name, brand, shelf_life = self.shelf_life_data.get(sku, ("Unknown", "Unknown", 0))
                    production_date = datetime.strptime(prod_date, "%Y-%m-%d").date()
                    expiration_date = self.calculate_expiration_date(production_date, shelf_life)
                    data = [sku, name, brand, expiration_date.strftime("%Y-%m-%d")]
                    self.write_to_history_csv(data)
                    history_data.append(data)
        except FileNotFoundError:
            ErrorMessages.file_not_found(csv_file_path)

        return history_data

    def run(self, csv_file=None, production_date=None, days=3, remove_expired=False, expiry_report_dest=None,
            clear_history=False):
        if csv_file and production_date:
            self.load_shelf_life_data()
            history_data = self.process_csv(csv_file, production_date)
            self.write_to_expiry_report(history_data, days, expiry_report_dest)
        else:
            self.generate_expiry_report(days, expiry_report_dest)

        if remove_expired:
            self.remove_expired_entries()
            print("Expired entries removed from history.csv")
            print("Expiry report cleared")

        if clear_history:
            self.clear_history_file()
            print("History file cleared")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("csv_file", help="CSV file containing SKUs", nargs="?")
    parser.add_argument("production_date", help="Production date (YYYY-MM-DD)", nargs="?")
    parser.add_argument("--days", type=int, default=3, help="Threshold for number of days until expiration", nargs="?")
    parser.add_argument("--remove-expired", action="store_true",
                        help="Remove expired entries from history.csv and clear the expiry report file")
    parser.add_argument("--expiry-report-dest", help="Destination file for the expiry report")
    parser.add_argument("--clear-history", action="store_true", help="Clear the history.csv file")
    args = parser.parse_args()

    expiry_tracker = ExpiryTracker()
    expiry_tracker.run(args.csv_file, args.production_date, args.days, args.remove_expired, args.expiry_report_dest,
                       args.clear_history)


if __name__ == "__main__":
    main()
