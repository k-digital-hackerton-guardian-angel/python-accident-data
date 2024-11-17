# 사고 데이터 정제

## 사고 데이터 추출

### 사고 데이터 추출 프로그램



i.py
초기 데이터
위도 경도 값 조정하기 위한 파일
```
    if adjust_grsY:
        grsY -= 302.4  # 필요한 경우 grsY 조정

    if adjust_grsX:
        grsX += 184.8  # 예시로 grsX를 150만큼 조정 (필요에 따라 값 수정)
```


accident-list.py
사고 데이터 추출 프로그램
- dongjak.json 파일 생성 (위도 경도 변경 전 데이터)
- dongjack.json 에서 사고 id 추출해서, 상세정보 불러오기
- accidents_data.xlsx 파일 생성 (위도 경도 변경 후 데이터)



