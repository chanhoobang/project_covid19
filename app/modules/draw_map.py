import os
import folium
from folium.plugins import MarkerCluster
from app.modules import database

# # 국내 확진자 수를 그리는 지도
# # date: 지도를 그릴 날짜 데이터
# # type: 국내, 국외 데이터를 구분하는 타입
# def draw_map(date, type):
#     map1 = folium.Map(location=[37, 127], locatzoom_start=10, zoom_control=True, control_scale=True)

#     cluster = MarkerCluster().add_to(map1)

#     if type == "korea" | type == "global":
#         data_list = database.select(type, date)
#     else:
#         raise ValueError("올바르지않은 접근입니다!")

#     for data in data_list:
        
#         temp_lat = data[위도]
#         temp_lon = data[경도]
        
#         temp_location = [temp_lat, temp_lon]
        
#         name = data[이름]
        
#         content = f"""
#         <h3>지명: {name}</h3>
#         <p>확진자 수: {data[]}</p>
#         <p>사망자 수: {data[]}</p>
#         <p>재감염자 수: {data[]}</p>
#         <p>재감염률: {data[]}</p>
#         <p>날짜: {date}</p>
#         """
#         temp_c = folium.Circle(temp_location,
#                             radius = data[확진자 수]["confirmed_cases"].values[0]/1000,
#                             popup=folium.Popup(content, max_width=200))
#         temp_c.add_to(cluster)
#     file_path = "./templates/covid19/covid19_map.html"

#     if os.path.exists(file_path):
#         print("파일이 이미 존재합니다")
#     else:
#         map1.save(file_path)