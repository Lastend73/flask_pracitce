import requests
import xml.etree.ElementTree as ET
import pprint
import pandas as pd

def get_hospital_list(pageNo):
    # 응답 결과 출력
    base_url = 'http://apis.data.go.kr/B551182/hospInfoServicev2/getHospBasisList'

# 요청할 API 엔드포인트와 파라미터 설정
    params = {
        'serviceKey': "Plq5DcdK7izqM+hBnYm42z5mVEr62M/BrqvrUeFYpYGFJ6kWg72jeM6kYfZciTx1bUVws+yd5GOgGjnqbH0yXQ==",
        'type': 'xml',
        'numOfRows': 1000,
        'pageNo': pageNo,
        'dgsbjtCd': 14
        # 추가적인 파라미터를 여기에 추가
    }
    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        # XML 응답 파싱
        root = ET.fromstring(response.content)
        total_data = int(root[1][3].text)
        data_lists = []
        root_datas = root[1][0]
        for root_data in root_datas:
            data_list = []
            data_list.append(root_data.find('addr').text)
            data_list.append(root_data.find('yadmNm').text)
            data_list.append(root_data.find('clCdNm').text)
            data_list.append(root_data.find('sgguCdNm').text)
            data_lists.append(data_list)
        return data_lists
    else:
        print(f"Error: {response.status_code}")

# filepath: /c:/Workspace/Python/HOSPITAL.PY
# API 호출을 위한 기본 URL
base_url = 'http://apis.data.go.kr/B551182/hospInfoServicev2/getHospBasisList'

# 요청할 API 엔드포인트와 파라미터 설정
params = {
    'serviceKey': "Plq5DcdK7izqM+hBnYm42z5mVEr62M/BrqvrUeFYpYGFJ6kWg72jeM6kYfZciTx1bUVws+yd5GOgGjnqbH0yXQ==",
    'type': 'xml',
    'numOfRows': 1,
    'pageNo': 1
    # 추가적인 파라미터를 여기에 추가
}

# API 호출
response = requests.get(base_url, params=params)

# 응답 결과 출력
if response.status_code == 200:
    # XML 응답 파싱
    root = ET.fromstring(response.content)
    data_lists = []
    total_data = int(int(root[1][3].text)/1000)
    for i in range(5, total_data+1):
        data = get_hospital_list(i)
        data_lists.extend(data)
        break
    print(data_lists)

    # 데이터프레임 생성
    df = pd.DataFrame(data_lists, columns=['Address', 'Hospital Name' , 'Classification', 'City'])

    # 엑셀 파일로 저장
    df.to_excel('hospital_list.xlsx', index=False)
