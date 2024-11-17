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

if __name__ == "__main__":
    # 입력 좌표
    grsX = 191350.668214533
    grsY = 439828.695398716


    # 변환할 좌표계 목록
    coordinate_systems = {
        "KATEC (EPSG:2097)": {"epsg": 2097, "adjust_grsY": True, "adjust_grsX": True},
    }

    for name, params in coordinate_systems.items():
        try:
            lat, lon = convert_grs_to_gps(
                grsX,
                grsY,
                source_epsg=params["epsg"],
                adjust_grsY=params.get("adjust_grsY", False),
                adjust_grsX=params.get("adjust_grsX", False)
            )
            print(f"{name}:")
            print(f"  위도: {lat:.6f}, 경도: {lon:.6f}\n")
        except Exception as e:
            print(f"{name} 변환 중 오류 발생: {e}\n")
