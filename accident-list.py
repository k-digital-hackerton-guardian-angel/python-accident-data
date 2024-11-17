import json
import requests
import pandas as pd
import time
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from pyproj import Transformer

def convert_grs_to_gps(grsX, grsY, source_epsg=5179, adjust_grsY=False, adjust_grsX=False):
    if adjust_grsY:
        grsY -= 302.4  # 필요한 경우 grsY 조정

    if adjust_grsX:
        grsX += 184.8  # 예시로 grsX를 150만큼 조정 (필요에 따라 값 수정)

    # Transformer 객체 생성: source_epsg -> WGS84 (EPSG:4326)
    transformer = Transformer.from_crs(f"epsg:{source_epsg}", "epsg:4326", always_xy=True)
    
    # 좌표 변환
    longitude, latitude = transformer.transform(grsX, grsY)
    
    return latitude, longitude


def create_session():
    session = requests.Session()
    
    # Configure retry strategy
    retry_strategy = Retry(
        total=3,
        backoff_factor=1,
        status_forcelist=[500, 502, 503, 504]
    )
    
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    
    return session

def get_pos_acc_list(pos_no, session):
    url = 'https://tmacs.kotsa.or.kr/webgis/accum/loadPosAccList_new.do'
    
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Cookie': 'WMONID=RNK2BTE7awS; SCOUTER=z6sn3oljcsv9mp; JSESSIONID=EAD7E5B49B01EB9E9F7BC0344AF045F4',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Encoding': 'gzip, deflate, br, zstd',
        'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
        'Origin': 'https://tmacs.kotsa.or.kr',
        'Referer': 'https://tmacs.kotsa.or.kr/webgis/main.do',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest'
    }
    
    data = {
        'posNo': pos_no,
        'cause': ''
    }
    
    try:
        response = session.post(url, data=data, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error occurred for posNo {pos_no}: {e}")
        return None

def main():
    # Read dongjak.json
    with open('dongjak.json', 'r', encoding='utf-8') as f:
        dongjak_data = json.load(f)
    
    all_accidents = []
    session = create_session()
    
    # Iterate through each entry and get similarPosNo
    for entry in dongjak_data:
        similar_pos_no = entry['similarPosNo']
        original_pos_no = entry['posNo']
        print(f"Processing similarPosNo: {similar_pos_no} for posNo: {original_pos_no}")
        
        # Get data for this similarPosNo
        accidents = get_pos_acc_list(original_pos_no, session)
        
        if accidents:
            # Add original posNo and similarPosNo to each accident record
            for accident in accidents:
                accident['grsXCrd'], accident['grsYCrd'] = convert_grs_to_gps(accident['grsXCrd'], accident['grsYCrd'], source_epsg=2097, adjust_grsY=True, adjust_grsX=True)
                accident['original_posNo'] = original_pos_no
                accident['similar_posNo'] = similar_pos_no
                all_accidents.append(accident)
        
        # Add a small delay to avoid overwhelming the server
        # time.sleep(1)
    
    if all_accidents:
        # Convert to DataFrame
        df = pd.DataFrame(all_accidents)
        
        # Save to Excel
        excel_filename = 'accidents_data.xlsx'
        df.to_excel(excel_filename, index=False)
        print(f"Data saved to {excel_filename}")
        print(f"Total accidents collected: {len(all_accidents)}")
    else:
        print("No data to save")

if __name__ == "__main__":
    main()