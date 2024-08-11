import streamlit as st
import pandas as pd
import json
import glob
import os

class CVEVisualization:
    def __init__(self):
        self.last_update_time = None

    def load_json_data(self):
        try:
            list_of_files = glob.glob('cve_cpe_results_*.json')
            if not list_of_files:
                return None
            latest_file = max(list_of_files, key=os.path.getctime)
            
            with open(latest_file, 'r') as f:
                data = json.load(f)
            return data
        except Exception as e:
            st.error(f"Error loading JSON data: {e}")
            return None

    def create_dataframe(self, data):
        if not data:
            return pd.DataFrame()
        
        flattened_data = []
        for item in data:
            try:
                cpe = item['CPE'].get('cpe', [])
                if isinstance(cpe, list):
                    cpe_str = ', '.join(cpe)
                else:
                    cpe_str = cpe
                
                flat_item = {
                    'CVE_ID': item.get('CVE_ID', 'N/A'),
                    'CVE_Description': item.get('CVE_Description', 'N/A'),
                    'CPE': cpe_str
                }
                flattened_data.append(flat_item)
            except KeyError as e:
                st.warning(f"Missing key in data: {e}")
        
        df = pd.DataFrame(flattened_data)
        return df

    def run(self):
        st.title('CVE - CPE Visualization Dashboard')

        data = self.load_json_data()
        if data:
            df = self.create_dataframe(data)

            st.subheader('Vulnerabilities Data Table')
            st.dataframe(df)
        else:
            st.write("No data available yet.")

if __name__ == "__main__":
    viz = CVEVisualization()
    viz.run()
