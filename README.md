# IP Generator Script

## Usefulness:
This script is designed to generate IP addresses for a specified country, ensuring that the IPs generated fall within the known IP ranges for that country. The script also tracks its progress to avoid regenerating the same IPs in subsequent runs. It provides options to display the generated IPs on the console or save them to a file. The script is optimized for performance by utilizing multithreading.

## IMPORTANT Note
- By using this tool, you agree that you are using it for educational purposes only and that you will not use it for any illegal activity. You also agree to bear all risks associated with the use of this tool. I will not be responsible for direct or indirect damage caused by the use of this tool.

## Usage  🚀:
1. Set up the environment variables in the `.env` file:
   - `BATCH_SIZE`: The number of IPs to generate and process in each batch.
   - `PROGRESS_TRACKER_PATH`: Path to a file where the script will save its progress.
   - `NUMBER_OF_THREADS`: The number of threads to use for parallel processing.
   - `SAVING_FILE_PATH`: The path where the output file with the generated IPs should be saved.
   - `COUNTRY_DATA_PATH`: Path to the file containing IP ranges for different countries.
   - `LOG_OUTPUT_FILEPATH`: Path to save the log file.



2. **Setting Up a Virtual Environment**:
   - Create a virtual environment: `python -m venv venv`
   - Activate the virtual environment:
     - On Windows: `venv\Scripts\activate`
     - On macOS and Linux: `source venv/bin/activate`

3. **Install Dependencies**:
   - Install the required packages: `pip install -r requirements.txt`

4. Run the script: `python main.py`


5. Follow the on-screen prompts to specify your preferences and start the IP generation process.



## Data Files:

1. **country_ip_ranges.json**: This file contains the IP ranges for different countries. It has a basic structure as shown below:
```json
{
  "Canada": [
    {"start": "x.x.x.x", "end": "y.y.y.y"},
    {"start": "a.a.a.a", "end": "b.b.b.b"},
    ...
  ],
  "USA": [
    {"start": "c.c.c.c", "end": "d.d.d.d"},
    ...
  ],
  ...
}
