import requests

def get_pos_acc_list(pos_no):
    url = 'https://tmacs.kotsa.or.kr/webgis/accum/loadPosAccList_new.do'
    
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Cookie': 'WMONID=RNK2BTE7awS; SCOUTER=z6sn3oljcsv9mp; JSESSIONID=EAD7E5B49B01EB9E9F7BC0344AF045F4',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Encoding': 'gzip, deflate, br, zstd',
        'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
        'Origin': 'https://tmacs.kotsa.or.kr',
        'Referer': 'https://tmacs.kotsa.or.kr/webgis/main.do',
        'User-Agent': 'Mozilla/5.0 (iPad; CPU OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1',
        'X-Requested-With': 'XMLHttpRequest'
    }
    
    data = {
        'posNo': pos_no,
        'cause': ''
    }
    
    session = requests.Session()
    session.headers.update(headers)
    
    try:
        response = session.post(url, data=data)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error occurred: {e}")
        return None

# 사용 예시
pos_no = "2023031100100098"
result = get_pos_acc_list(pos_no)

if result:
    print(result)
