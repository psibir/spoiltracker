# spoiltracker

![spoiltracker logo](https://github.com/psibir/psibir.github.io/blob/main/assets/images/spoiltracker_logo.png?raw=true)

Spoiltracker is a Python package that helps track the expiration dates of products. It calculates expiration dates based on the production dates and shelf life information and generates an expiry report for products that are approaching their expiration dates.

## Simple Product Expiration Date Management

Spoiltracker is useful for businesses that deal with perishable products and need to keep track of their expiration dates. It can be used in various industries such as food and beverage, agriculture, perishable goods logistics, warehousing, pharmaceuticals, and cosmetics. The package helps businesses to:

- Maintain a record of product SKUs, names, brands, and expiration dates.
- Calculate expiration dates based on the production dates and shelf life information.
- Generate an expiry report that lists products approaching their expiration dates within a specified number of days.
- Remove expired entries from the history file to keep the record up to date.
- Clear the history file when necessary.

## Business Use Case: Deli and Cheese Counters Spoilage Mitigation

Spoiltracker is a valuable tool for deli and cheese counters, as well as any industry where spoilage mitigation is crucial. It helps track the expiration dates of perishable products, such as deli meats, cheeses, and other fresh foods, allowing businesses to effectively manage inventory, reduce waste, and ensure product quality and safety.

By utilizing Spoiltracker in deli and cheese counters, businesses can:

- Optimize inventory management: Spoiltracker enables businesses to keep a record of products along with their production dates and shelf life information. This helps deli and cheese counter managers to efficiently manage their inventory by identifying products that are approaching their expiration dates. By staying proactive, managers can ensure that products are used or sold before they spoil, reducing waste and optimizing stock levels.

- Minimize spoilage and waste: Spoiltracker assists in identifying products that are close to their expiration dates. With the generated expiry reports based on specified criteria, such as the number of days until expiration, businesses can take proactive measures to minimize spoilage and waste. This can include implementing promotional activities, such as discounts or special offers, to encourage customers to purchase products before they expire.

- Ensure product quality and safety: Maintaining accurate and up-to-date records of product expiration dates is crucial for ensuring product quality and safety. Spoiltracker allows businesses to monitor and manage expiration dates effectively, reducing the risk of serving or selling expired products to customers. By staying on top of product freshness, businesses can enhance customer satisfaction and reputation.

- Streamline operations: Spoiltracker streamlines the process of managing product expiration dates. With its ability to remove expired entries from the history file and clear the history file, businesses can maintain a clean and organized record of products. This streamlines operations, making it easier for deli and cheese counter staff to access information, plan for product usage, and maintain compliance with food safety regulations.

## Installation

To install Spoiltracker, follow these steps:

1. Clone the repository from GitHub:

   ```shell
   git clone https://github.com/psibir/spoiltracker.git
   ```

2. Navigate to the `spoiltracker/src` directory:

   ```shell
   cd spoiltracker/src
   ```

3. Create a virtual environment and install the required dependencies:

   ```shell
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

4. Run the `spoiltracker.py` script:

   ```shell
   python spoiltracker.py
   ```

   This will execute the SpoilerTracker script.

The package can also be installed using pip:

```shell
pip install spoiltracker
```

## Usage

### Single CSV Processing

To process a single CSV file, use the `--csv_file` and `--production_date` arguments. Specify the path to the CSV file and the production date in the format `YYYY-MM-DD`.

```bash
spoiltracker --csv_file path/to/file.csv --production_date 2023-06-01
```

This command will process the specified CSV file, calculate the expiration dates based on the shelf life data, and append the results to the history file.

### Batch Processing

To batch process multiple CSV files, place the files in a directory and use the `--batch` argument to specify the directory path. The files in the directory must be named in the format `YYYY-MM-DD.csv`, representing the production dates.

```bash
spoiltracker --batch path/to/directory
```

SpoilTracker will process each CSV file in the batch, calculate the expiration dates, and append the results to the history file.

### Expiry Report

To generate an expiry report, use the `--days` argument to set the threshold for the number of days until expiration. By default, SpoilTracker uses a threshold of 3 days. The expiry report includes the SKUs, names, brands, and expiration dates of the products that fall within the specified threshold.

```bash
spoiltracker --days 5
```

The expiry report will be saved in the default output file `./output/expiryreport.csv`. You can also specify a custom output file using the `--output-dest` argument.

### Clearing Expired Entries

If you want to remove expired entries from the history file and clear the expiry report file, use the `--clear-expired` flag.

```bash
spoiltracker --clear-expired
```

This command will remove expired entries from the history file and clear the expiry report file.

### Clearing History File

To clear the history file, use the `--clear-history` flag.

```bash
spoiltracker --clear-history
```

This command will clear the history file, removing all entries.

### Outputting a Pretty-Printed Expiry Report

To output a pretty-printed expiry report as a text file, use the `--table` flag.

```bash
spoiltracker --table
```

This command will generate the expiry report and save it as `./output/expiryreport.txt`. The text file will contain a nicely formatted table with the SKUs, names, brands, and expiration dates of the products that fall within the specified threshold.

## Method Description

The SpoilTracker package provides the following methods:

- `load_shelf_life_data()`: Loads the shelf life data from the shelf life file.
- `calculate_expiration_date(production_date, shelf_life)`: Calculates the expiration date based on the production date and shelf life.
- `append_to_history(data)`: Appends data to the history file.
- `append_to_expiry_report(data, days, output_dest=None)`: Appends data to the expiry report file for products that fall within the specified threshold.
- `sort_expiry_report(output_dest)`: Sorts the expiry report file by expiration date.
- `generate_expiry_report(days, output_dest=None)`: Generates the expiry report for products that fall within the specified threshold.
- `clear_expired_entries()`: Removes expired entries from the history file and clears the expiry report file.
- `clear_history_file()`: Clears the history file.
- `process_csv(csv_file_path, prod_date)`: Processes a CSV file, calculates expiration dates, and returns the processed data.
- `print_table(output_dest=None, show_console=False)`: Prints a pretty-formatted table of the expiry report and saves it as a text file.
- `run(csv_file=None, production_date=None, days=3, clear_expired=False, output_dest=None, clear_history=False, print_table=False)`: Runs the SpoilTracker functionality based on the provided arguments.

### Python Script Integration

To use Spoiltracker in a Python script, you can import the `ExpiryTracker` class and create an instance of it. Then, call the `run` method with the desired parameters.

```python
from spoiltracker import ExpiryTracker

expiry_tracker = ExpiryTracker()
expiry_tracker.run(csv_file="sku_list.csv", production_date="2023-06-01", days=5, remove_expired=True)
```

## Customize Shelf Life Data

Spoiltracker requires shelf life data to calculate expiration dates. By default, it expects a CSV file named "shelflife.csv" in the `./csv` directory. The file should have the following columns: SKU, Name, Brand, "Shelf Life" (in days).

```csv
SKU,Name,Brand,Shelf Life
123,Product 1,Brand 1,10
456,Product 2,Brand 2,7
```

You can customize the shelf life file path by providing it when creating an instance of `ExpiryTracker`.

```python
expiry_tracker = ExpiryTracker(shelf_life_file="custom_shelflife.csv")
```

## Dependencies

SpoilTracker has the following dependencies:

- `argparse`: For parsing command-line arguments.
- `csv`: For reading and writing CSV files.
- `os`: For working with file paths and directories.
- `datetime`, `timedelta`: For working with dates and calculating expiration dates.
- `tabulate`: For generating formatted tables.

Make sure to install these dependencies before using SpoilTracker.

## Contributions

See [Contributions](/CONTRIBUTIONS).
