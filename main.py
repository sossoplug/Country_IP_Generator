import concurrent.futures
import os
import ipaddress
import ip_generator
import country_filter
import utils
import traceback
from dotenv import load_dotenv

load_dotenv()

# ========================
# DETERMINE NEXT BATCH
# ========================
def determine_next_batch(last_ip, ip_ranges, batch_size):
    """
    Determines the next batch of IPs to generate based on the last generated IP, IP ranges, and batch size.
    """

    print(f"Inside determine_next_batch with last_ip: {last_ip}")

    start_ip                = None
    end_ip                  = None

    if not last_ip:
        # print("No last_ip found. Starting from the beginning.")
        # If no last IP, start from the beginning of the IP ranges
        start_ip            = ip_ranges[0]["start"]
    else:
        # print("Last IP found. Determining start_ip.")
        for ip_range in ip_ranges:
            if ipaddress.ip_address(last_ip) < ipaddress.ip_address(ip_range["end"]):
                start_ip    = str(ipaddress.ip_address(last_ip) + 1)
                break
        else:
            # If last_ip is the last IP in the final range
            return None, None

    end_ip                  = str(ipaddress.ip_address(start_ip) + batch_size - 1)
    # print(f"end_ip: {end_ip}")

    # Ensure end_ip doesn't exceed the current range
    for ip_range in ip_ranges:
        if ipaddress.ip_address(start_ip) >= ipaddress.ip_address(ip_range["start"]) and ipaddress.ip_address(start_ip) <= ipaddress.ip_address(ip_range["end"]):
            if ipaddress.ip_address(end_ip) > ipaddress.ip_address(ip_range["end"]):
                end_ip      = ip_range["end"]
            break

    # print(f"start_ip: {start_ip}")

    return start_ip, end_ip




# ========================
# MAIN
# ========================
def main():
    """
    Main function to orchestrate the IP generation process.
    """
    try:
        # Load environment variables
        BATCH_SIZE                  = int(os.getenv("BATCH_SIZE", 1000))
        SAVING_FILE_PATH            = os.getenv("SAVING_FILE_PATH", "generated_ips.txt")
        NUMBER_OF_THREADS           = int(os.getenv("NUMBER_OF_THREADS", 4))

        # Prompt user to select a country
        country                     = country_filter.select_country()
        if not country:
            print("Invalid country selection.")
            utils.write_to_log(f"==================================================", "")
            utils.write_to_log("Invalid country selection.", "ERROR")
            return

        # Load progress for the selected country
        last_ip                     = utils.load_progress(country)

        # Determine the next batch of IPs to generate
        ip_ranges                   = country_filter.get_country_ip_ranges(country)
        start_ip, end_ip            = determine_next_batch(last_ip, ip_ranges, BATCH_SIZE)

        print("yooo")

        # Split the IP range into chunks for threading
        total_ips                   = int(ipaddress.ip_address(end_ip)) - int(ipaddress.ip_address(start_ip)) + 1
        ips_per_thread              = total_ips // NUMBER_OF_THREADS

        threads                     = []
        with concurrent.futures.ThreadPoolExecutor() as executor:
            for i in range(NUMBER_OF_THREADS):
                chunk_start_ip      = str(ipaddress.ip_address(start_ip) + i * ips_per_thread)
                if i == NUMBER_OF_THREADS - 1:  # If it's the last thread, take the remaining IPs
                    chunk_end_ip    = end_ip
                else:
                    chunk_end_ip    = str(ipaddress.ip_address(chunk_start_ip) + ips_per_thread - 1)

                threads.append(executor.submit(ip_generator.generate_ips_within_range, chunk_start_ip, chunk_end_ip))

            # Collect results from all threads
            generated_ips           = []
            for thread in threads:
                generated_ips.extend(thread.result())

        # Filter for public IPs
        public_ips                  = [ip for ip in generated_ips if ip_generator.is_public_ip(ip)]

        utils.display_ips(public_ips)
        utils.save_ips_to_file(public_ips, SAVING_FILE_PATH)

        utils.write_to_log(f"==================================================", "")
        utils.write_to_log(f"IPs saved to {SAVING_FILE_PATH}", "ERROR")
        print(f"IPs saved to {SAVING_FILE_PATH}")

        # Save progress
        utils.save_progress(country, public_ips[-1])

    except Exception as e:
        traceback.print_exc()
        utils.write_to_log(f"==================================================", "")
        utils.write_to_log(f"Error in main script: {e}", "ERROR")
        print(f"Error in main script: {e}")
    else:
        utils.write_to_log(f"==================================================", "")
        utils.write_to_log("IP generation process completed successfully.", "SUCCESS")
        print("IP generation process completed successfully.")



if __name__ == "__main__":
    main()
