import os
import folium
from folium.plugins import MarkerCluster



# 국내 확진자 수를 그리는 지도
def draw_map_korea(data):
    map1 = folium.Map(location=[37, 127], locatzoom_start=10, zoom_control=True, control_scale=True)

    cluster = MarkerCluster().add_to(map1)

    # data 딕셔너리의 날짜의 key값 입력 필요 @@@@@@@@@
    date = data[]
    list = data

    for el in list:
        # data 딕셔너리의 위경도, name의 key값 입력 필요 @@@@@@@@@
        temp_lat = data[]
        temp_lon = data[]
        name = data[]
        
        temp_location = [temp_lat, temp_lon]
        
        content = f"""
        <h3>시군구: {name}</h3>
        <p>확진자 수: {}</p>
        <p>사망자 수: {}</p>
        <p>재감염률: {}</p>
        <p>재감염자 수: {}</p>
        <p>날짜: {date}</p>
        """

        # 확진자 수 데이터 필요 @@@@@@@@@@@
        temp_c = folium.Circle(temp_location,
                            radius = data[filter_date].loc[data["city_name"]==el]["confirmed_cases"].values[0]/1000,
                            popup=folium.Popup(content, max_width=200))
        temp_c.add_to(cluster)

    map_path = "./templates/covid19/covid19_map_korea.html"
    if os.path.exists(map_path):
        pass
    else:
        map1.save("./templates/covid19/covid19_map_korea.html")