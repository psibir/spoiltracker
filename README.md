# spoiltracker

![spoiltracker logo](/spoiltracker_logo.png)

Spoiltracker is a Python package that helps track the expiration dates of products. It calculates expiration dates based on the production dates and shelf life information and generates an expiry report for products that are approaching their expiration dates.

## Simple Product Expiry Management

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

The package can be installed using pip:

```shell
pip install spoiltracker
```

## Usage

Spoiltracker can be used from the command line or integrated into other Python scripts.

### Command Line Usage

To use Spoiltracker from the command line, run the following command:

```shell
python -m spoiltracker [csv_file] [production_date] [--days DAYS] [--remove-expired] [--expiry-report-dest FILE] [--clear-history]
```

- `[csv_file]` (optional): The path to the CSV file containing the product data. If not provided, Spoiltracker will generate an expiry report based on the existing history file.
- `[production_date]` (optional): The production date in the format "YYYY-MM-DD". If not provided, Spoiltracker will generate an expiry report based on the existing history file.
- `--days DAYS` (optional): The threshold for the number of days until expiration. Default is 3 days.
- `--remove-expired` (optional): Flag to remove expired entries from the history file and clear the expiry report file.
- `--expiry-report-dest FILE` (optional): Destination file for the expiry report. If not provided, the default file "expiryreport.csv" will be used.
- `--clear-history` (optional): Flag to clear the history file.

### Python Script Integration

To use Spoiltracker in a Python script, you can import the `ExpiryTracker` class and create an instance of it. Then, call the `run` method with the desired parameters.

```python
from spoiltracker import ExpiryTracker

expiry_tracker = ExpiryTracker()
expiry_tracker.run(csv_file="sku_list.csv", production_date="2023-06-01", days=5, remove_expired=True)
```

### Shelf Life Data

Spoiltracker requires shelf life data to calculate expiration dates. By default, it expects a CSV file named "shelflife.csv" in the same directory as the script or package using Spoiltracker. The file should have the following columns: SKU, Name, Brand, Shelf Life (in days).

```csv
SKU,Name,Brand,Shelf Life
123,Product 1,Brand 1,10
456,Product 2,Brand 2,7
```

You can customize the shelf life file path by providing it when creating an instance of `ExpiryTracker`.

```python
expiry_tracker = ExpiryTracker(shelf_life_file="custom_shelflife.csv")
```

## Functions

- Load Shelf Life Data:
  - The script automatically loads the shelf life data from the `shelflife.csv` file.

- Process CSV File:
  - Specify the input CSV file and the production date using the `--csv-file` and `--production-date` options.
  - The script calculates the expiration dates for the products and writes the data to the history file.

- Generate Expiry Report:
  - By default, the script generates an expiry report for products expiring within the next 3 days.
  - Use the `--days` option to specify a different threshold for the number of days until expiration.
  - The report is saved in the `expiryreport.csv` file (or a custom destination if specified).

- Remove Expired Entries:
  - Use the `--remove-expired` option to remove expired entries from the history file and clear the expiry report file.

- Clear History File:
  - Use the `--clear-history` option to clear the history file.

By running the script with different combinations of these functionalities and adjusting the command-line options accordingly, you can effectively manage product expiration dates, generate reports, and maintain an up-to-date history of your products.

## Methods

Spoiltracker provides the following functionality:

### Load Shelf Life Data

The `load_shelf_life_data` method loads the shelf life data from the shelf life file. It

 reads the CSV file and stores the data in memory for later use.

### Calculate Expiration Date

The `calculate_expiration_date` method calculates the expiration date based on the production date and shelf life information. It takes the production date and the shelf life as input and returns the expiration date.

### Write to History CSV

The `write_to_history_csv` method writes data to the history CSV file. It takes a list of data as input, appends it to the existing file, and creates a new file if it doesn't exist.

### Write to Expiry Report

The `write_to_expiry_report` method generates an expiry report based on the data provided. It compares the expiration dates with the current date and the specified threshold (number of days). It writes the report to the expiry report file, appending new entries and creating a new file if it doesn't exist.

### Sort Expiry Report

The `sort_expiry_report` method is responsible for sorting the entries in the expiry report based on the expiration date. It takes the `expiry_report_dest` parameter, which represents the path to the expiry report file.

### Generate Expiry Report

The `generate_expiry_report` method generates an expiry report based on the existing history file. It reads the history file, filters the entries that are approaching their expiration dates within the specified number of days, and writes the report to the expiry report file.

### Remove Expired Entries

The `remove_expired_entries` method removes expired entries from the history file. It reads the expiry report file to get the SKUs of expired products and filters out those entries from the history file. It also clears the expiry report file.

### Clear History File

The `clear_history_file` method clears the history file by removing all its contents.

### Process CSV

The `process_csv` method processes the provided CSV file and generates the history data. It reads the CSV file, retrieves the shelf life information for each SKU, calculates the expiration dates, and writes the data to the history file. It returns the history data.

### Run

The `run` method is the main entry point for using Spoiltracker. It accepts command line arguments or direct parameters and executes the necessary functions based on the provided options.

### Error Handling

Spoiltracker provides basic error handling for file not found errors and invalid date formats. If the shelf life file, history file, or expiry report file is not found, an error message is displayed. If an invalid date format is encountered in the CSV files, an error message is displayed as well.

## Contributions

See [Contributions](/CONTRIBUTIONS).
