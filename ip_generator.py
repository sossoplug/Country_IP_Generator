import ipaddress

# ========================
# GENERATE IP WITHIN RANGE
# ========================
def generate_ips_within_range(start_ip, end_ip):
    """
    Generates IPs within a specified range.

    Args:
        start_ip (str):     The starting IP of the range.
        end_ip (str):       The ending IP of the range.

    Returns:
        list:               A list of IPs within the specified range.
    """
    try:

        start_int           = int(ipaddress.ip_address(start_ip))
        end_int             = int(ipaddress.ip_address(end_ip))
        return [str(ipaddress.ip_address(ip)) for ip in range(start_int, end_int + 1)]

    except Exception as e:
        print(f"Error generating IPs within range: {e}")
        return []

# ========================
# IS IP PUBLIC ?
# ========================
def is_public_ip(ip_address):
    """
    Checks if a given IP address is public.

    Args:
        ip_address (str):   The IP address to check.

    Returns:
        bool:               True if the IP is public, False otherwise.
    """
    try:

        ip                  = ipaddress.ip_address(ip_address)
        return not ip.is_private

    except Exception as e:
        print(f"Error checking if IP is public: {e}")
        return False
