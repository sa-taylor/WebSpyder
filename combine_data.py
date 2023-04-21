import csv
import os
from collections import defaultdict

#Process the price string and separate MSRP and listed price
def process_prices(price_str):
    prices = price_str.split('  ')
    prices = [p.strip() for p in prices if p.strip()]

    if len(prices) == 1:
        return '', prices[0]
    elif len(prices) == 2:
        return prices[0], prices[1]
    elif len(prices) == 3:
        return prices[0], prices[2]
    else:
        return '', ''

#Split and capitalize the filename to get Category and Sub-Category
def split_and_capitalize(filename):
    parts = filename.split('_')
    return ' '.join(word.capitalize() for word in parts[0].split('-')), ' '.join(word.capitalize() for word in parts[1].split('-'))

#Combine CSV files in the input folder into a single output file
def combine_csv_files(input_folder, output_file):
    combined_data = []
    fieldnames = ['Category', 'Sub-Category']

    # Iterate through files in the input folder
    for file in os.listdir(input_folder):
        if file.endswith('.csv'):
            with open(os.path.join(input_folder, file), 'r') as csvfile:
                reader = csv.DictReader(csvfile, delimiter=',', quotechar='"')

                # Process each row in the CSV file
                for row in reader:
                    if 'Price' in row:
                        msrp, listed_price = process_prices(row['Price'])
                        row['MSRP'] = msrp
                        row['Listed Price'] = listed_price
                        del row['Price']

                    # Extract category and sub-category from the filename
                    col1, col2 = split_and_capitalize(os.path.splitext(file)[0])
                    row['Category'] = col1
                    row['Sub-Category'] = col2

                    combined_data.append(row)

            # Update fieldnames
            fieldnames.extend(reader.fieldnames)

    # Remove duplicate fieldnames and reorder
    fieldnames = [fn for fn in fieldnames if fn not in ['Price', 'Sizes']] + ['MSRP', 'Listed Price', 'Sizes']
    fieldnames = list(dict.fromkeys(fieldnames))

    # Write combined data to output file
    with open(output_file, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writeheader()
        writer.writerows(combined_data)

#Define input and output in directory
if __name__ == '__main__':
    input_folder = 'scraped_data'
    output_file = 'all_extracted_data.csv'
    combine_csv_files(input_folder, output_file)