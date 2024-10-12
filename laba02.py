import time
import datetime
import requests as re
import shutil
import os
import platform
import zipfile
import requests

NVD_DB_PATH="NVD_DB"

if (platform.system() == 'Windows'):
    path_to_reports_file = f"{NVD_DB_PATH}"
    isExist = os.path.exists(f"{NVD_DB_PATH}")
    if not isExist:
    # Create a new directory because it does not exist
        os.makedirs(f"{NVD_DB_PATH}")
elif(platform.system() == 'Linux'):
    path_to_reports_file = f"{NVD_DB_PATH}"
    isExist = os.path.exists(f"{NVD_DB_PATH}")
    if not isExist:
    # Create a new directory because it does not exist
        os.makedirs(f"{NVD_DB_PATH}")

def nvd_db_update():
    start_time = time.time()
    download_url = ""
    special_urls = [r"https://nvd.nist.gov/feeds/json/cve/1.1/nvdcve-1.1-modified.json.zip", r"https://nvd.nist.gov/feeds/json/cve/1.1/nvdcve-1.1-recent.json.zip"]
    currentYear = datetime.datetime.now().year
    for year in range(2002, currentYear+1):
        year_var = year
        #######Downloading Files
        download_url = f"https://nvd.nist.gov/feeds/json/cve/1.1/nvdcve-1.1-{year_var}.json.zip"
        print(download_url)
        r = requests.get(download_url)

        with open(f"nvdcve-1.1-{year_var}.json.zip", "wb") as code:
            code.write(r.content)
        ####### moving downloaded archives
        shutil.move(f"nvdcve-1.1-{year_var}.json.zip", f"{NVD_DB_PATH}/nvdcve-1.1-{year_var}.json.zip")
        #time.sleep(20)
    #    ###### Extracting archives
        print(f"{NVD_DB_PATH}/nvdcve-1.1-{year_var}.json.zip")
        with zipfile.ZipFile(f"{NVD_DB_PATH}/nvdcve-1.1-{year_var}.json.zip", 'r') as zip_ref:
            zip_ref.extractall(f"{NVD_DB_PATH}/")
        os.remove(f"{NVD_DB_PATH}/nvdcve-1.1-{year_var}.json.zip")
    #
    for iterat in special_urls:
        matching_pattern = re.match(r"(.*)/(.*)", iterat)
        r = requests.get(iterat)
        with open(f"{matching_pattern.group(2)}", "wb") as code:
            code.write(r.content)
    #     # moving downloaded archives
        shutil.move(f"{matching_pattern.group(2)}", f"{NVD_DB_PATH}/{matching_pattern.group(2)}")
        with zipfile.ZipFile(f"{NVD_DB_PATH}/{matching_pattern.group(2)}", 'r') as zip_ref:
            zip_ref.extractall(f"{NVD_DB_PATH}/")
        os.remove(f"{NVD_DB_PATH}/{matching_pattern.group(2)}")
        #
    print("--- %s seconds ---" % (time.time() - start_time))
    print(f" nvd_db_update() finished ")
    
nvd_db_update()
#print(time.localtime())
