import json
import re
from langchain_community.llms import Ollama  
from langchain_core.output_parsers import JsonOutputParser
from prompt_template import create_prompt_template
from langchain_core.pydantic_v1 import BaseModel, Field 
from cpeParser import CPEParser
from dotenv import load_dotenv
import os


class FileCPE():
    
    def clean_json(self, data):
        json_str = json.dumps(data, indent=4)
        cleaned_json_str = re.sub(r',(\s*[\}\]])', r'\1', json_str)
        return json.loads(cleaned_json_str)
    
    def old_cve_file(self, file):
        llm = Ollama(model="llama3", temperature=0.1)
        prompt = create_prompt_template()
        parser = JsonOutputParser(pydantic_object=CPEParser)
        chain = prompt | llm | parser

        with open(file, 'r') as oldFile:
            data = json.load(oldFile)
        
        cpe_results = []

        for i in data:
            cve_id = i['cve_id']
            description = i['description']
                    
            try:
                cpe_result = chain.invoke({"cve_id": cve_id,  "description": description})
                cpe_results.append({
                    'CVE_ID': cve_id,
                    'CVE_Description': description,
                    'CPE': cpe_result
                })
                print("------------------LLM TEXT PROCESS-------------------")
                print(f"Processed {cve_id}")
            except Exception as e:
                print(f"Error processing {cve_id}: {e}")
        
        # Temizleme işlemini yap
        cleaned_results = self.clean_json(cpe_results)

        with open('./test/cve_cpe_2017_results.json', 'w', encoding='utf-8') as outfile:
            json.dump(cleaned_results, outfile, indent=4)

        print("Processing complete. Results saved to cve_cpe_2017_results.json")

if __name__ == "__main__":
    file_cpe = FileCPE()
    file_cpe.old_cve_file("./test/cve2017.json")
