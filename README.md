# OpenFDA-API-Script
# FDA Drug Data Fetcher 

This Python script fetches drug data from the FDA OpenFDA API and saves it to a CSV file. It can be used to gather information about drugs based on their generic or brand names.

## Features

- Fetches drug data from the FDA OpenFDA API using generic or brand names.
- Stores drug data in a CSV file for analysis and record-keeping.
- Handles empty drug names and stops after encountering three consecutive empty names.
- Avoids duplicate searches by checking for existing drug names in the output CSV file.

## Requirements

- Python 3.x
- `requests` library (install using `pip install requests`)

## Usage

1. Prepare an input CSV file named `input_file.csv` with drug names in a column.
2. Run the script using `python script.py`.
3. The script will fetch drug data and store it in the `output_file.csv` CSV file.

## Configuration

- `input_file.csv`: Input CSV file with drug names (one per row).
- `output_file.csv`: Output CSV file for storing drug data.

## Notes

- The script handles API responses, including failed requests and empty responses.
- Consecutive empty drug names are monitored to prevent unnecessary processing.
- Fields "brand_name", "generic_name", "substance_name", "manufacturer_name" and "route" are under "openfda" in the JSON file.
- The field "dosage_form" is under "products" and is handled differently in the script. 

## Key Personal Learnings

- Writing a script using Python
- Working with an API
- Managing data output formatting
- Using ChatGPT to gather missing information
- Using ChatGPT for code generation
- Using Jupyter Notebook on VSCode
- Using Postman to visualize JSON output
- Time-management skills

  
## Future Work

It will be recommended to switch the API used to the Product Labeling API. in order to add field "strength".
The data for drug strength can be found under "dosage_forms_and_strengths".
The script will need to account for the existence of multiple strengths of the same drug. These strengths should be displayed under different rows/entries in the CSV. The link below is an example query on the Product Labeling API, with no specified search field: 
https://api.fda.gov/drug/label.json?search=&limit=10

The script should also output its results in CSV format, as well as a JSON file. Refer to the link below for help:
https://pythonexamples.org/python-csv-to-json/

## Contact

Salma Shaarawi - salma@shaarawy.com

## Acknowledgements

This script uses the FDA OpenFDA API to retrieve drug data.

---

Feel free to contribute to the project by opening issues or submitting pull requests!



