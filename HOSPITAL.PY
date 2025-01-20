import requests
import xml.etree.ElementTree as ET
import pprint

# filepath: /c:/Workspace/Python/HOSPITAL.PY
# API 호출을 위한 기본 URL
base_url = 'http://apis.data.go.kr/B551182/hospInfoServicev2/getHospBasisList'

# 요청할 API 엔드포인트와 파라미터 설정
params = {
    'serviceKey': "Plq5DcdK7izqM+hBnYm42z5mVEr62M/BrqvrUeFYpYGFJ6kWg72jeM6kYfZciTx1bUVws+yd5GOgGjnqbH0yXQ==",
    'type': 'xml',
    'numOfRows': 1,
    'pageNo': 1,
    # 추가적인 파라미터를 여기에 추가
}

# API 호출
response = requests.get(base_url, params=params)

# 응답 결과 출력
if response.status_code == 200:
    # XML 응답 파싱
    root = ET.fromstring(response.content)
    print(type(root))
    print(root[1][0][0].find('addr').text)
    print(root[1][0][0].find('yadmNm').text)
    for child in root:
        for grandchild in child:
            for great_grandchild in grandchild:
                for great_great_grandchild in great_grandchild:
                    print(great_great_grandchild.tag, great_great_grandchild.text)
            print(grandchild.tag, grandchild.text)


    # XML 문자열로 변환하여 출력
    xml_str = ET.tostring(root, encoding='utf-8').decode('utf-8')
    # print(xml_str)
else:
    print(f"Error: {response.status_code}")