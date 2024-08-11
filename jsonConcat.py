import json

# JSON dosyalarını okur
with open('./allJsonfiles/nvdcve-1.1-2019.json', 'r', encoding="utf-8") as file2019, \
     open('./allJsonfiles/nvdcve-1.1-2020.json', 'r', encoding="utf-8") as file2020, \
     open('./allJsonfiles/nvdcve-1.1-2021.json', 'r', encoding="utf-8") as file2021, \
     open('./allJsonfiles/nvdcve-1.1-2022.json', 'r', encoding="utf-8") as file2022, \
     open('./allJsonfiles/nvdcve-1.1-2023.json', 'r', encoding="utf-8") as file2023:

  
    cve2019 = json.load(file2019)
    cve2020 = json.load(file2020)
    cve2021 = json.load(file2021)
    cve2022 = json.load(file2022)
    cve2023 = json.load(file2023)


combined_data = {}        # JSON verilerini birleştirir (sözlük birleştirme)
for data in [ cve2019, cve2020, cve2021, cve2022, cve2023]:
    combined_data.update(data)


with open('allCVEdata.json', 'w', encoding="utf-8") as outfile: # Birleştirilmiş veriyi yeni bir dosyaya yazar
    json.dump(combined_data, outfile, indent=4)
