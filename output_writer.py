import csv
import logging
from tabulate import tabulate

logger = logging.getLogger(__name__)

def write_output(filename, data, fieldnames):
    logger.info(f"Outputs writing to file: {filename}...")
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for item in data:
            writer.writerow(item)
    
    logger.info(f"The results were successfully printed to {filename}")

def print_table(data, fieldnames):
    logger.info("Outputs writing to table...")
    table = [ [item[field] for field in fieldnames] for item in data ]
    print(tabulate(table, headers=fieldnames, tablefmt='grid'))
    logger.info("Results have been printed as a table...")
