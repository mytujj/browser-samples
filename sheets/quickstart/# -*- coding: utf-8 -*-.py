# -*- coding: utf-8 -*-
"""
Configuration Parser for SPKR Project

This script reads configuration settings from an INI file,
parses the sections and key-value pairs, and converts
values to appropriate Python types (int, float, bool, str).
"""

import configparser
import io
import json
import os # Added for file path handling

# --- Default/Example Configuration Data (as a multi-line string) ---
# This can be used for testing or as a fallback if the file is missing.
DEFAULT_CONFIG_DATA = """
[Company]
name = SPKR
year = 2
currency = USD

[Subscription]
paid_users = 20000
monthly_fee = 9.99
annual_multiplier = 12

[Advertising]
free_users = 40000
monthly_revenue_per_user = 2.00
annual_multiplier = 12

[Licensing]
artist_revenue = 105750.00

[DistributionServices]
spotify_distribution = true
apple_music_distribution = true
cd_baby_fee = 99.00
vevo_distribution_fee = 99.00
analytics_package_fee = 40.00

[PRO]
ascap_bmi_simulation = true
estimated_streaming_revenue_per_1000 = 4.37
estimated_radio_play_revenue_per_play = 0.12
performance_rights_simulation = true

[Expenses]
artist_payouts = 250000.00
marketing = 300000.00
support = 250000.00
bandwidth = 150000.00

[TaxSettings]
deductible_percentage = 0.80

[ReportFormat]
decimal_places = 2
use_thousands_separator = true
"""

# --- Configuration File ---
# Define the expected name of the configuration file.
# It's good practice to keep config files separate from code.
CONFIG_FILENAME = "config.ini"

# --- Parsing Logic ---
def parse_config(config_source):
    """
    Parses configuration data from a file path or a string.

    Args:
        config_source (str): Either a file path to an INI file or a string
                             containing INI-formatted data.

    Returns:
        dict: A nested dictionary representing the configuration data.
              Returns an empty dictionary if parsing fails.
    """
    config = configparser.ConfigParser()
    parsed_successfully = False

    # Check if the source is a file that exists
    if os.path.isfile(config_source):
        try:
            # Read directly from the file
            config.read(config_source, encoding='utf-8')
            parsed_successfully = True
            print(f"Successfully read configuration from file: {config_source}")
        except configparser.Error as e:
            print(f"Error parsing configuration file '{config_source}': {e}")
            return {} # Return empty dict on file parsing error
        except IOError as e:
            print(f"Error reading configuration file '{config_source}': {e}")
            return {} # Return empty dict on file reading error
    else:
        # Assume config_source is a string containing the data
        try:
            config.read_file(io.StringIO(config_source))
            parsed_successfully = True
            print("Successfully parsed configuration from string.")
        except configparser.Error as e:
            print(f"Error parsing configuration string: {e}")
            return {} # Return empty dict on string parsing error

    if not parsed_successfully:
        return {}

    # --- Convert to Dictionary with Type Conversion ---
    config_dict = {}
    for section in config.sections():
        config_dict[section] = {}
        for key, value in config.items(section):
            # Attempt type conversion
            processed_value = value
            # Try boolean first (case-insensitive)
            if value.lower() == 'true':
                processed_value = True
            elif value.lower() == 'false':
                processed_value = False
            else:
                # Try integer
                try:
                    processed_value = int(value)
                except ValueError:
                    # Try float if integer conversion fails
                    try:
                        processed_value = float(value)
                    except ValueError:
                        # Keep as string if it's not a boolean, int, or float
                        pass # Keep as original string
            config_dict[section][key] = processed_value

    return config_dict

# --- Main Execution Block ---
if __name__ == "__main__":
    print("Attempting to load configuration...")

    # Try loading from the standard config file first
    parsed_config = parse_config(CONFIG_FILENAME)

    # If loading from file failed (e.g., file not found or parse error),
    # try parsing the default string data as a fallback.
    if not parsed_config:
        print(f"\nCould not load from '{CONFIG_FILENAME}'. Falling back to default config string.")
        # Create the config.ini file with default data if it doesn't exist
        if not os.path.exists(CONFIG_FILENAME):
            try:
                with open(CONFIG_FILENAME, 'w', encoding='utf-8') as f:
                    f.write(DEFAULT_CONFIG_DATA.strip())
                print(f"Created default configuration file: '{CONFIG_FILENAME}'")
                # Try parsing the newly created file
                parsed_config = parse_config(CONFIG_FILENAME)
            except IOError as e:
                print(f"Error writing default config file: {e}")
                # If writing fails, parse the string directly
                parsed_config = parse_config(DEFAULT_CONFIG_DATA)
        else:
             # If file exists but parsing failed earlier, parse the string
             parsed_config = parse_config(DEFAULT_CONFIG_DATA)


    # --- Output the Parsed Configuration ---
    if parsed_config:
        print("\nParsed Configuration:")
        # Use json.dumps for pretty printing the dictionary
        print(json.dumps(parsed_config, indent=4))

        # --- Example: Accessing a value ---
        print("\nExample Access:")
        company_name = parsed_config.get('Company', {}).get('name', 'N/A')
        monthly_fee = parsed_config.get('Subscription', {}).get('monthly_fee', 0.0)
        spotify_enabled = parsed_config.get('DistributionServices', {}).get('spotify_distribution', False)

        print(f"Company Name: {company_name}")
        print(f"Monthly Subscription Fee: {monthly_fee}")
        print(f"Spotify Distribution Enabled: {spotify_enabled}")
    else:
        print("\nFailed to load or parse any configuration.")

# This script can be run directly to test the configuration parsing.
# It will attempt to read from 'config.ini' and fall back to the default data if necessary.
# The parsed configuration will be printed in a structured format.
# Note: The script assumes the config file is in the same directory as the script.
# Ensure the script is executable and can handle both file and string inputs gracefully.
# The script is designed to be robust against common errors like file not found or parsing issues.
# It also provides informative messages to help diagnose issues.
# The configuration data is structured to allow easy access to various settings,
# including company details, subscription plans, advertising revenue, licensing,