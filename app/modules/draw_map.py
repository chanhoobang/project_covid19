import os
import folium
import MarkerCluster

# 국내 확진자 수를 그리는 지도
# date: 지도를 그릴 날짜 데이터
# type: 국내, 국외 데이터를 구분하는 타입
def draw_map(date, type):
    map1 = folium.Map(location=[37, 127], locatzoom_start=10, zoom_control=True, control_scale=True)

    if type == 

    cluster = MarkerCluster().add_to(map1)

    date = "2023-04-01"
    list = data["city_name"].unique().tolist()

    for el in list:
        filter_date = data["date"] == date
        
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
    file_path = "./templates/covid19/covid19_map.html"

    if os.path.exists(file_path):
        print("파일이 이미 존재합니다")
    else:
        map1.save(file_path)