import json
import os

from bs4 import BeautifulSoup
from dotenv import load_dotenv

from utils import write_to_log

load_dotenv()


def populate_country_ip_ranges(html_file_path, country_name):
    """
    Extracts IP ranges from an HTML table and populates the country_ip_ranges.json file.

    Args:
        html_file_path (str):   Path to the HTML file containing the IP ranges table.
        country_name (str):     Name of the country for which the IP ranges are being extracted.
    """
    try:
        # Load the HTML content
        with open(html_file_path, 'r', encoding='utf-8') as file:
            soup                = BeautifulSoup(file, 'html.parser')

        # Extract IP ranges from the table
        table                   = soup.find('table', {'id': 'ip-address'})
        rows                    = table.find('tbody').find_all('tr')
        ip_ranges               = []

        for row in rows:
            columns             = row.find_all('td')
            start_ip            = columns[0].text.strip()
            end_ip              = columns[1].text.strip()
            ip_ranges.append({"start": start_ip, "end": end_ip})

        # Load existing data from country_ip_ranges.json
        if os.path.exists(os.getenv("COUNTRY_DATA_PATH")):
            with open(os.getenv("COUNTRY_DATA_PATH"), 'r') as file:
                data            = json.load(file)
        else:
            data                = {}

        # Update the data with the new IP ranges for the specific country
        data[country_name]      = ip_ranges

        # Save the updated data back to country_ip_ranges.json
        with open(os.getenv("COUNTRY_DATA_PATH"), 'w') as file:
            json.dump(data, file, indent=4)

        write_to_log(f"==================================================", "")
        write_to_log(f"IP ranges for {country_name} have been successfully added to country_ip_ranges.json.", "SUCCESS")
        print(f"IP ranges for {country_name} have been successfully added to country_ip_ranges.json.")

    except Exception as e:
        print(f"Error populating IP ranges for {country_name}: {e}")


# Example usage
country                         = str(input("Enter the country name: ")).lower()
populate_country_ip_ranges(os.getenv("HTML_TABLE_FILEPATH"), country)
