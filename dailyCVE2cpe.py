import json
from langchain_community.llms import Ollama  
from langchain_core.output_parsers import JsonOutputParser
from prompt_template import create_prompt_template
from langchain_core.pydantic_v1 import BaseModel, Field 
from cpeParser import CPEParser
import requests
import nvdlib
import datetime
import time
from dotenv import load_dotenv
import os

load_dotenv()

nvdApiKey = os.getenv("NVD_API_KEY")

infoUrl = "https://services.nvd.nist.gov/rest/json/cves/2.0"
updateUrl = "https://services.nvd.nist.gov/rest/json/cvehistory/2.0"

headers = {  
    "apiKey": nvdApiKey
}

llm = Ollama(model="llama3", temperature=0.1)
prompt = create_prompt_template()
parser = JsonOutputParser(pydantic_object=CPEParser)
chain = prompt | llm | parser

def fetch_cve_info(start_date, end_date):
    try:
        print("API isteği gönderiliyor...")
        response = nvdlib.searchCVE(pubStartDate=start_date, pubEndDate=end_date)
        print("başarılı")
        cve_data_list = []
        for cve in response:
            cveId = cve.id
            cveDesc = cve.descriptions[0].value.replace("\n", " ").rstrip()
            cve_data = {
                'CVE_ID': cveId,
                'Description': cveDesc
            }
            cve_data_list.append(cve_data)
        return cve_data_list
    except requests.exceptions.RequestException as e:
        print(f"Error fetching CVE data: {e}")
        return []

def process_cve_data(cve_data):
    cpe_results = []
    for cve in cve_data:
        cve_id = cve['CVE_ID']
        description = cve['Description']
        cpe_result = chain.invoke({"cve_id": cve_id, "description": description})
        cpe_results.append({
            'CVE_ID': cve_id,
            'CVE_Description': description,
            'CPE': cpe_result
        })
        print(f"Processed {cve_id}")
    return cpe_results

def save_to_json(data, filename):
    with open(filename, 'w', encoding='utf-8') as outfile:
        json.dump(data, outfile, indent=4, ensure_ascii=False)

def clear_temp_file(temp_file):
    if os.path.exists(temp_file):
        os.remove(temp_file)
        print(f"Temporary file {temp_file} has been deleted.")

def main():
    interval_hours = 6
    temp_file = "temp_cve_data.json"
    
    while True:
        now = datetime.datetime.now()
        
        # Check if it's a new day
        if now.hour == 14 and now.minute == 33:
            # Create a new file for the day
            daily_file = f"cve_cpe_results_{now.strftime('%Y-%m-%d')}.json"
            save_to_json([], daily_file)  # Initialize with an empty list
        
        start = now - datetime.timedelta(hours=interval_hours)
        start_date = start.strftime("%Y-%m-%d %H:%M")
        end_date = now.strftime("%Y-%m-%d %H:%M")

        print(f"Fetching data from {start_date} to {end_date}")
        
        # Clear previous temp file if it exists
        clear_temp_file(temp_file)
        
        # Fetch and save to temp file
        cve_data = fetch_cve_info(start_date, end_date)
        save_to_json(cve_data, temp_file)
        
        # Process the data
        processed_data = process_cve_data(cve_data)
        
        # Append to the daily file
        daily_file = f"cve_cpe_results_{now.strftime('%Y-%m-%d')}.json"
        with open(daily_file, 'r+', encoding='utf-8') as file:
            existing_data = json.load(file)
            existing_data.extend(processed_data)
            file.seek(0)
            json.dump(existing_data, file, indent=4, ensure_ascii=False)
        
        print(f"Updated {daily_file} with new data")
        
        # Streamlit uygulamasını güncellemek için bir sinyal gönder
        with open("update_signal.txt", "w") as f:
            f.write(now.strftime("%Y-%m-%d %H:%M:%S"))
        # Calculate time until next run
        next_run = (now + datetime.timedelta(hours=interval_hours)).replace(minute=0, second=0, microsecond=0)
        if next_run.hour >= 24:  # If next run would be after midnight
            next_run = next_run.replace(hour=0)  # Set to midnight
            next_run += datetime.timedelta(days=1)  # Move to next day
        
        sleep_seconds = (next_run - now).total_seconds()
        print(f"Sleeping until {next_run}")
        time.sleep(sleep_seconds)

if __name__ == "__main__":
    main()