import datetime
import json

# ===================
# LOAD PROGRESS
# ===================
import os


def load_progress(country):
    """
    Loads the progress for the specified country from the progress_tracker.json file.

    Args:
        country (str): The name of the country.

    Returns:
        str:            The last generated IP for the country.
    """
    try:
        with open(os.getenv("PROGRESS_TRACKER_PATH"), "r") as file:
            data        = json.load(file)
            return data.get(country, "")
    except Exception as e:
        print(f"Error loading progress for {country}: {e}")
        return ""

# ===================
# SAVE PROGRESS
# ===================
def save_progress(country, last_ip):
    """
    Saves the current progress for the specified country to the progress_tracker.json file.

    Args:
        country (str):      The name of the country.
        last_ip (str):      The last generated IP for the country.

    Returns:
        None
    """
    try:
        with open(os.getenv("PROGRESS_TRACKER_PATH"), "r") as file:
            data            = json.load(file)
            data[country]   = last_ip
        with open(os.getenv("PROGRESS_TRACKER_PATH"), "w") as file:
            json.dump(data, file)
    except Exception as e:
        print(f"Error saving progress for {country}: {e}")

# ===================
# SAVE IP TO FILE
# ===================
def save_ips_to_file(ip_list, file_path):
    """
    Saves a list of IPs to a specified file.

    Args:
        ip_list (list):     The list of IPs to save.
        file_path (str):    The path to the file where the IPs should be saved.

    Returns:
        None
    """
    try:
        with open(file_path, "a") as file:
            for ip in ip_list:
                file.write(ip + "\n")
    except Exception as e:
        print(f"Error saving IPs to file: {e}")


# ===================
# DISPLAY IPS
# ===================
def display_ips(ip_list):
    """
    Displays a list of IPs on the console.

    Args:
        ip_list (list): The list of IPs to display.

    Returns:
        None
    """
    try:
        for ip in ip_list:
            print(ip)
    except Exception as e:
        print(f"Error displaying IPs: {e}")


# ==================
# Write to Log
# ==================
def write_to_log(message, status):
    """
    Write a message to the log file.

    Args:
    - message (str):                    The message to be logged.
    - status (str):                     The status of the message (ERROR/SUCCESS).

    Returns:
    - None
    """
    try:
        timestamp                       = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        with open(os.getenv("LOG_OUTPUT_FILEPATH"), "a") as log_file:
            log_file.write(f"[{timestamp}] INFO: [{status}]: {message}\n")
    except Exception as e:
        print(f"[ERROR]: Failed to write to log. {str(e)}")