import ipaddress
import json

# ===================
# SELECT COUNTRY
# ===================
import os

from utils import write_to_log


def select_country():
    """
    Prompts the user to select a country for IP generation.

    Returns:
        str:            The name of the selected country.
    """
    try:
        with open(os.getenv("COUNTRY_DATA_PATH"), "r") as file:
            countries   = json.load(file).keys()

            print("Available countries:")

            for index, country in enumerate(countries, 1):
                print(f"{index}. {country}")

            choice      = int(input("Select a country by number: "))

            return list(countries)[choice - 1]

    except Exception as e:
        print(f"Error selecting country: {e}")
        return ""

# ===================
# GET COUNTRY
# ===================
def get_country_ip_ranges(country):
    """
    Retrieves the IP ranges for the specified country.

    Args:
        country (str):      The name of the country.

    Returns:
        list:               A list of IP ranges for the country.
    """
    try:

        with open(os.getenv("COUNTRY_DATA_PATH"), 'r') as file:
            data            = json.load(file)
            ranges          = data.get(country, [])

            # Validate IP ranges
            valid_ranges = []
            for ip_range in ranges:
                start_ip    = ipaddress.ip_address(ip_range["start"])
                end_ip      = ipaddress.ip_address(ip_range["end"])

                if start_ip > end_ip:
                    write_to_log(f"==================================================", "")
                    write_to_log(f"Invalid IP range for {country}: {ip_range['start']} - {ip_range['end']}", "ERROR")
                    continue
                else:
                    valid_ranges.append(ip_range)

            return ranges

    except Exception as e:
        print(f"Error retrieving IP ranges for {country}: {e}")
        return []
