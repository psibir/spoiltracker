import glob
import argparse
import csv
import os
from datetime import datetime, timedelta
from tabulate import tabulate


class ErrorMessage:
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
    def __init__(self, shelf_life_file='./csv/shelflife.csv', history_file='./csv/history.csv',
                 expiry_report_file='./output/expiryreport.csv', days=3):
        self.shelf_life_file = shelf_life_file
        self.history_file = history_file
        self.expiry_report_file = expiry_report_file
        self.days = days
        self.shelf_life_data = {}


    def load_shelf_life_data(self):
        try:
            with open(self.shelf_life_file, 'r') as shelf_life_file:
                reader = csv.reader(shelf_life_file)
                next(reader)  # Skip header row
                self.shelf_life_data = {row[0]: (row[1], row[2], int(row[3])) for row in reader}
        except FileNotFoundError:
            ErrorMessage.file_not_found(self.shelf_life_file)

    def calculate_expiration_date(self, production_date, shelf_life):
        return production_date + timedelta(days=shelf_life)

    def append_to_history(self, data):
        try:
            with open(self.history_file, 'a', newline='') as history_csv:
                writer = csv.writer(history_csv)
                writer.writerow(data)

            with open(self.history_file, 'r') as history_csv:
                reader = csv.reader(history_csv)
                header = next(reader)
                rows = sorted(reader, key=lambda row: datetime.strptime(row[3], "%Y-%m-%d"))
                with open(self.history_file, 'w', newline='') as history_csv:
                    writer = csv.writer(history_csv)
                    writer.writerow(header)
                    writer.writerows(rows)
        except FileNotFoundError:
            ErrorMessage.file_not_found(self.history_file)

    def append_to_expiry_report(self, data, days, output_dest=None):
        if output_dest is None:
            output_dest = self.expiry_report_file

        today = datetime.now().date()
        within_days = []

        try:
            with open(output_dest, 'a', newline='') as expiry_csv:
                writer = csv.writer(expiry_csv)
                existing_entries = set()
                try:
                    with open(output_dest, 'r') as existing_csv:
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
                        ErrorMessage.invalid_date_format(row[3])

                writer.writerows(within_days)
        except FileNotFoundError:
            ErrorMessage.file_not_found(output_dest)

        self.sort_expiry_report(output_dest)

    def sort_expiry_report(self, output_dest):
        try:
            with open(output_dest, 'r') as expiry_csv:
                rows = list(csv.reader(expiry_csv))
                sorted_rows = sorted(rows[1:], key=lambda row: datetime.strptime(row[3], "%Y-%m-%d").date())

            with open(output_dest, 'w', newline='') as expiry_csv:
                writer = csv.writer(expiry_csv)
                writer.writerow(rows[0])
                writer.writerows(sorted_rows)
        except FileNotFoundError:
            ErrorMessage.file_not_found(output_dest)

    def generate_expiry_report(self, days, output_dest=None):
        if output_dest is None:
            output_dest = self.expiry_report_file

        today = datetime.now().date()
        within_days = []

        try:
            with open(self.history_file, 'r') as history_csv:
                reader = csv.reader(history_csv)
                header = next(reader)
                existing_entries = set(tuple(row) for row in reader)
        except FileNotFoundError:
            ErrorMessage.file_not_found(self.history_file)
            return

        for row in existing_entries:
            try:
                expiration_date = datetime.strptime(row[3], "%Y-%m-%d").date()
                if (expiration_date - today) <= timedelta(days=days):
                    within_days.append(row)
            except ValueError:
                ErrorMessage.invalid_date_format(row[3])

        try:
            with open(output_dest, 'w', newline='') as expiry_csv:
                writer = csv.writer(expiry_csv)
                writer.writerow(["SKU", "Name", "Brand", "Expiration Date"])
                writer.writerows(within_days)
        except FileNotFoundError:
            ErrorMessage.file_not_found(output_dest)

        self.sort_expiry_report(output_dest)

    def clear_expired_entries(self):
        expiry_skus = set()

        try:
            with open(self.expiry_report_file, 'r') as expiry_csv:
                reader = csv.reader(expiry_csv)
                next(reader)
                expiry_skus = {row[0] for row in reader}
        except FileNotFoundError:
            ErrorMessage.file_not_found(self.expiry_report_file)
            return

        history_data = []

        try:
            with open(self.history_file, 'r') as history_csv:
                reader = csv.reader(history_csv)
                header = next(reader)
                history_data.append(header)
                for row in reader:
                    sku = row[0]
                    if sku not in expiry_skus:
                        history_data.append(row)
        except FileNotFoundError:
            ErrorMessage.file_not_found(self.history_file)
            return

        try:
            with open(self.history_file, 'w', newline='') as history_csv:
                writer = csv.writer(history_csv)
                writer.writerows(history_data)
        except FileNotFoundError:
            ErrorMessage.file_not_found(self.history_file)

        try:
            with open(self.expiry_report_file, 'w', newline='') as expiry_csv:
                writer = csv.writer(expiry_csv)
                writer.writerow(["SKU", "Name", "Brand", "Expiration Date"])  # Write the header
        except FileNotFoundError:
            ErrorMessage.file_not_found(self.expiry_report_file)


    def clear_history_file(self):
        header = ["SKU", "Name", "Brand", "Expiration Date"]

        try:
            with open(self.history_file, 'w', newline='') as history_csv:
                writer = csv.writer(history_csv)
                writer.writerow(header)
        except FileNotFoundError:
            ErrorMessage.file_not_found(self.history_file)

    def process_csv(self, csv_file_path, prod_date):
        history_data = []
        try:
            with open(csv_file_path, 'r') as csv_file:
                reader = csv.reader(csv_file)
                next(reader)
                for row in reader:
                    sku = row[0]
                    name, brand, shelf_life = self.shelf_life_data.get(sku, ("Unknown", "Unknown", 0))
                    production_date = datetime.strptime(str(prod_date), "%Y-%m-%d").date()
                    expiration_date = self.calculate_expiration_date(production_date, shelf_life)
                    data = [sku, name, brand, expiration_date.strftime("%Y-%m-%d")]
                    self.append_to_history(data)
                    history_data.append(data)
        except FileNotFoundError:
            ErrorMessage.file_not_found(csv_file_path)

        return history_data

    def print_table(self, output_dest=None, show_console=False):
        if output_dest is None:
            output_dest = self.expiry_report_file

        try:
            with open(output_dest, 'r') as expiry_csv:
                reader = csv.reader(expiry_csv)
                table_data = list(reader)
                if len(table_data) > 0:
                    headers = ["SKU", "Name", "Brand", "Expiration Date"]
                    table_data = table_data[1:]

                    # Filter table data based on the new 'days' value
                    today = datetime.now().date()
                    filtered_data = []
                    for row in table_data:
                        expiration_date = datetime.strptime(row[3], "%Y-%m-%d").date()
                        if (expiration_date - today) <= timedelta(days=self.days):
                            filtered_data.append(row)

                    # Generate the table with the filtered data
                    pretty_table = tabulate(filtered_data, headers, tablefmt="pretty")

                    if show_console:
                        print(pretty_table)

                    txt_filename = os.path.splitext(output_dest)[0] + ".txt"
                    with open(txt_filename, "w") as txt_file:
                        txt_file.write(pretty_table)
                else:
                    print("No data found in the expiry report.")
        except FileNotFoundError:
            ErrorMessage.file_not_found(output_dest)


    def run(self, csv_file=None, production_date=None, days=3, clear_expired=False, output_dest=None,
            clear_history=False, print_table=False):
        if csv_file and production_date:
            self.load_shelf_life_data()
            history_data = self.process_csv(csv_file, production_date)
            self.append_to_expiry_report(history_data, days, output_dest)
        else:
            self.generate_expiry_report(days, output_dest)

        if print_table:
            self.generate_expiry_report(days, output_dest)
            self.print_table(output_dest)

        if clear_expired:
            self.clear_expired_entries()
            print("Expired entries removed from history")
            print("Expiry report cleared")

        if clear_history:
            if self.clear_history_file():
                print("History file cleared")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--csv_file", help="CSV file containing SKUs", nargs="?")
    parser.add_argument("--production_date", help="Production date (YYYY-MM-DD)", nargs="?")
    parser.add_argument("--days", type=int, default=3, help="Threshold for number of days until expiration", nargs="?")
    parser.add_argument("--clear-expired", action="store_true", help="Remove expired entries from history.csv and clear the expiry report file")
    parser.add_argument("--output-dest", help="Destination file for the expiry report")
    parser.add_argument("--clear-history", action="store_true", help="Clear the history file")
    parser.add_argument("--batch", help="Directory containing files with SKUs to batch process (files must be named YYYY-MM-DD)", nargs="?")
    parser.add_argument("--table", action="store_true", help="Outputs a pretty-printed expiry report as expiryreport.txt")
    args = parser.parse_args()

    expiry_tracker = ExpiryTracker(days=args.days)

    if args.batch:
        batch_directory = args.batch
        if not os.path.isdir(batch_directory):
            print("Error: Invalid batch directory path.")
            return

        batch_files = glob.glob(os.path.join(batch_directory, "*.csv"))
        for file_path in batch_files:
            date_str = os.path.splitext(os.path.basename(file_path))[0]
            production_date = datetime.strptime(date_str, "%Y-%m-%d").date()
            expiry_tracker.run(file_path, production_date, args.days, args.clear_expired, args.output_dest,
                               args.clear_history)
    else:
        expiry_tracker.run(args.csv_file, args.production_date, args.days, args.clear_expired, args.output_dest,
                           args.clear_history, args.table)

if __name__ == "__main__":
    main()
