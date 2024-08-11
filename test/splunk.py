import json
from langchain_community.llms import Ollama  
from langchain_core.output_parsers import JsonOutputParser
from prompt_template import create_prompt_template
from cpeParser import CPEParser
import requests
import nvdlib
from dotenv import load_dotenv
import os


load_dotenv()

nvdApiKey = os.getenv("NVD_API_KEY") #NVD api key header da kullanılmak üzere çekildi.


#NVD database verilerinin çekilmesi için kullanılacak olan URL ler
infoUrl = "https://services.nvd.nist.gov/rest/json/cves/2.0"
updateUrl = "https://services.nvd.nist.gov/rest/json/cvehistory/2.0"

headers = {  
    "apiKey": nvdApiKey
}



llm = Ollama(model="llama3", temperature=0.1) #llm referansı oluşturuldu model yüklendi


prompt = create_prompt_template() #oluşturulan template çağırıldı




def fetch_cve_updates(change_start_date, change_end_date):
    params = {
        "changeStartDate": change_start_date,
        "changeEndDate": change_end_date
    }
    print("API isteği gönderiliyor...")
    try:
        response = requests.get(updateUrl, headers=headers, params=params)
        if response.status_code == 200:
            print("API yanıtı alındı.")
            data = response.json()
            return data
        else:
            print("Durum kodunda hata var (update)")
    except requests.exceptions.RequestException as e:
        print(f"Error fetching CVE data: {e}")

def fetch_cve_info(cveId):


    try:
        print("API isteği gönderiliyor...")
        response = nvdlib.searchCVE(cveId=cveId)
        print("başarılı")
        cve_data_list = []
        for cve in response:
            print("**************")
            print(cve.id)
            cveId = cve.id
            print(cve.descriptions[0].value)
            cveDesc = cve.descriptions[0].value.replace("\n", " ").rstrip()
            cve_data = {
            'CVE_ID': cveId,
            'Description': cveDesc
            }
            cve_data_list.append(cve_data)
        print(f"cve_data_list {cve_data_list}")
        with open('cve_data2.json', 'w+', encoding='utf-8') as outfile:
            json.dump(cve_data_list, outfile, indent=4, ensure_ascii=False)
        print("CVE verileri JSON formatında kaydedildi.")
        return cve_data
    except requests.exceptions.RequestException as e:
        print(f"Error fetching CVE data: {e}")
    



data = fetch_cve_info("CVE-2024-36991")

with open("cve_data2.json", 'r', encoding='utf-8') as file:
                cve_data = json.load(file)


parser = JsonOutputParser(pydantic_object=CPEParser)
chain = prompt | llm | parser
cpe_results = []
for cve in cve_data:
    cve_id = cve['CVE_ID']
    description = cve['Description']

    cpe_result = chain.invoke({"cve_id": cve_id, "description": description})  #modelle oluşturulan zincir çağırıldı prompt ve model çalıştıırldı model cve_if ve description değerilerine göre 
            
    cpe_results.append({
                    'CVE_ID': cve_id,
                    'CVE_Description': description,
                    'CPE': cpe_result #boşlukları kaldırmak için 
    })
print("------------------LLM TEXT PROCESS-------------------")
print(f"Processed {cve_id}")

with open(f"./test/cve_cpe_resultsSplunk.json", 'w', encoding='utf-8') as outfile: #sonuçlar cve_cpe_resultssss.json dosyasına kaydedilir.
        json.dump(cpe_results, outfile, indent=4)





