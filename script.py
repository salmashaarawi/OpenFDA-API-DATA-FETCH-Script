import requests
import csv


def fetch_drug_data(drug_name):
    api_url_generic = f"https://api.fda.gov/drug/drugsfda.json?search=openfda.generic_name:\"{drug_name}\"&limit=1"
    api_url_brand = f"https://api.fda.gov/drug/drugsfda.json?search=openfda.brand_name:\"{drug_name}\"&limit=1"

    response = requests.get(api_url_generic)
    if response.status_code == 200:
        return response.json()
    else:
        print(
            f"Failed to fetch data for {drug_name} using generic_name. Status code: {response.status_code}")
        response_brand = requests.get(api_url_brand)
        if response_brand.status_code == 200:
            return response_brand.json()
        else:
            print(
                f"Failed to fetch data for {drug_name} using brand_name. Status code: {response_brand.status_code}")
            return {'results': None}


def concatenate_values(values_list):
    return '; '.join(values_list) if values_list else ''


def write_csv_header(csv_filename):
    with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['search_name', 'manufacturer_name', 'brand_name',
                      'generic_name', 'route', 'dosage_form', 'error', 'substance_name']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()


def append_to_csv(data, csv_filename, drug_name):
    with open(csv_filename, 'a', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['search_name', 'brand_name', 'generic_name',
                      'substance_name', 'manufacturer_name', 'route', 'dosage_form', 'error', ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        if csvfile.tell() == 0:  
            writer.writeheader() 

        if data['results'] is not None:
            for item in data['results']:
                dosage_form = ''  


                if 'products' in item:
                    products = item['products']
                    if products:
                        product = products[0]
                        dosage_form = product.get('dosage_form', '')

                writer.writerow({
                    'search_name': drug_name, 
                    'brand_name': concatenate_values(item['openfda'].get('brand_name', [])),
                    'generic_name': concatenate_values(item['openfda'].get('generic_name', [])),
                    'manufacturer_name': concatenate_values(item['openfda'].get('manufacturer_name', [])),
                    'substance_name': concatenate_values(item['openfda'].get('substance_name', [])),
                    'route': concatenate_values(item['openfda'].get('route', [])),
                    'dosage_form': dosage_form,  
                    'error': ''
                })
        else:
            writer.writerow({
                'search_name': drug_name,
                'brand_name': '',
                'generic_name': '',
                'manufacturer_name': '',
                'substance_name': '',
                'route': '',
                'dosage_form': '',
                'error': f"Search failed for {drug_name}"
            })


if __name__ == "__main__":
    input_csv_filename = "input_file.csv"
    output_csv_filename = "output_file.csv"

    searched_drug_names = set()
    try:
        with open(output_csv_filename, 'r', encoding='utf-8') as existing_csvfile:
            csv_reader = csv.reader(existing_csvfile)
            next(csv_reader)  
            for row in csv_reader:
                searched_drug_names.add(row[0]) 
    except FileNotFoundError:
        pass 

    empty_name_count = 0  

    with open(input_csv_filename, 'r', encoding='utf-8') as input_csvfile:
        csv_reader = csv.reader(input_csvfile)
        next(csv_reader) 

        for row in csv_reader:
           
            drug_name = row[2].strip()

            if not drug_name:  
                empty_name_count += 1
                if empty_name_count >= 3: 
                    print("Stopping due to three consecutive empty drug names.")
                    break
            else:
                empty_name_count = 0 

                if drug_name not in searched_drug_names: 
                    drug_data = fetch_drug_data(drug_name)
                    append_to_csv(drug_data, output_csv_filename, drug_name)
                    searched_drug_names.add(drug_name)
                    print(f"Data written for {drug_name}")

    print(f"All data written to {output_csv_filename}")
