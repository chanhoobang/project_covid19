import pandas as pd
import folium
from folium.plugins import MarkerCluster

df_XY = pd.read_excel("korea_lat_lon.xlsx")

# 영어 도시 명칭을 한글로 치환해주는 함수
# city: 영어 도시명
# return: 한글 도시명
def change_city_name(city):
    dic1 = {
        "Gyeonggi":"경기도",
        "Seoul":"서울특별시",
        "Gyeongsangnam":"경상남도",
        "Gyeongsangbuk":"경상북도",
        "Jeollanam":"전라남도",
        "Jeollabuk":"전라북도",
        "Chungcheongnam":"충청남도",
        "Busan":"부산광역시",
        "Gangwon":"강원특별자치도",
        "Chungcheongbuk":"충청북도",
        "Incheon":"인천광역시",
        "Daegu":"대구광역시",
        "Gwangju":"광주광역시",
        "Daejeon":"대전광역시",
        "Ulsan":"울산광역시",
        "Jeju":"제주특별자치도",
        "Sejong":"세종특별자치시",
        "Ieo":"이어도"
    }
    
    try:
        return dic1[city]
    except KeyError as e:
        return city
    

    

# 주소를 입력받아 위경도를 반환하는 함수
# address: 주소 (도, 시, 동) 순서
# return: 해당 주소의 위경도
def get_xy(address):
    arr = address.split(" ")
    
    arr[0] = change_city_name(arr[0])
    
    cond1 = df_XY["1단계"].str.contains(arr[0])
    
    size = len(arr)
    
    val = ""
    
    if size == 1:
        cond2_na = df_XY["2단계"].isnull()
        cond3_na = df_XY["3단계"].isnull()
        
        val = df_XY.loc[cond1 & cond2_na & cond3_na]
        
    elif size == 2:
        cond2 = df_XY["2단계"].str.contains(arr[1])
        cond3_na = df_XY["3단계"].isnull()
        
        val =  df_XY.loc[cond1 & cond2 & cond3_na]
    
    elif size == 3:
        cond2 = df_XY["2단계"].str.contains(arr[1])
        cond3 = df_XY["3단계"].str.contains(arr[2])
        
        val =  df_XY.loc[cond1 & cond2 & cond3]
    
    idx = val.index.tolist()[0]
    
    return val.loc[idx, "위도"], val.loc[idx, "경도"]



# 국내 확진자 수를 나타내는 지도
def draw_map_korea(data):
    map1 = folium.Map(location=[37, 127], locatzoom_start=10, zoom_control=True, control_scale=True)

    cluster = MarkerCluster().add_to(map1)

    date = "2023-04-01"
    list = data["city_name"].unique().tolist()

    for el in list:
        filter_date = data["date"] == date

        print(el)
        
        temp_lat = get_xy(el)[0]
        temp_lon = get_xy(el)[1]
        
        temp_location = [temp_lat, temp_lon]
        
        name = change_city_name(el)
        
        content = f"""
        <h3>시군구: {name}</h3>
        <p>확진자 수: {data[filter_date].loc[data["city_name"]==el]["confirmed_cases"].values[0]}</p>
        <p>사망자 수: {data[filter_date].loc[data["city_name"]==el]["death_cases"].values[0]}</p>
        <p>날짜: {date}</p>
        """
        temp_c = folium.Circle(temp_location,
                            radius = data[filter_date].loc[data["city_name"]==el]["confirmed_cases"].values[0]/1000,
                            popup=folium.Popup(content, max_width=200))
        temp_c.add_to(cluster)
    map1.save("../templates/covid19/covid19_map_korea.html")