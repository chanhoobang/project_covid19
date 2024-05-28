import os
import folium
from folium import Marker
from folium.plugins import MarkerCluster
from app.models.detail import KoreaData, GlobalData, AgeData, GenderData
from app.models.position import KoreaPosition, GlobalPosition
from app.modules.common import Common

# 데이터베이스에서 데이터를 가져오는 함수
def get_data(data_type, date):

    list_data = []
    is_global = False

    if data_type == "age":
        data_all = Common.select_where_date(AgeData, date)
    elif data_type == "gender":
        data_all = Common.select_where_date(GenderData, date)
    elif data_type == "korea":
        data_all = Common.select_where_date(KoreaData, date)
    elif data_type == "global":
        data_all = Common.select_where_date(GlobalData, date)
        is_global = True
    else:
        raise ValueError("입력값이 올바르지않습니다!")
    
    list_data = Common.data_push_list(data_all, is_global)

    return list_data



# 코로나 확진자 수를 그리는 지도
# type: 국내, 국외 데이터를 구분하는 타입
# date: 지도를 그릴 날짜 데이터
def draw_map(data_type, date):

    file_path = "app/static/map/map.html"

    if data_type == "korea":
        data_all = Common.select_where_date(KoreaData, date)
        map1 = folium.Map(location=[37, 127], locatzoom_start=10, zoom_control=True, control_scale=True)
    elif data_type == "global":
        data_all = Common.select_where_date(GlobalData, date)
        map1 = folium.Map(locatzoom_start=10, zoom_control=True, control_scale=True)
    else:
        raise ValueError("입력값이 올바르지않습니다!")

    cluster = MarkerCluster().add_to(map1)

    for data in data_all:
        if data_type == "korea":
            position = Common.select_where_position(KoreaPosition, data.city_name)
            name = Common.mapping_city_name(data.city_name)
            for p in position:
                temp_location = [p.position_y, p.position_x]
        elif data_type == "global":
            position = Common.select_where_nation(GlobalPosition, data.nation)
            name = data.nation
            for p in position:
                temp_location = [p.position_x, p.position_y]

        content = f"""
        <h3>지명: {name if data_type == "korea" else data.nation}</h3>
        <p>사망자 수: {data.death_cases}</p>
        <p>누적 확진자 수: {data.total_cases}</p>
        <p>신규 확진자 수: {data.active_cases}</p>
        <p>재감염률: {data.re_rate}</p>
        <p>재감염자 수: {data.re_cases}</p>
        <p>날짜: {data.data_date[:10]}</p>
        """

        temp_c = folium.Circle(temp_location,
                            radius = data.total_cases/100,
                            popup=folium.Popup(content, max_width=200))
        temp_c.add_to(cluster)

        Marker(location = temp_location,
           popup=folium.Popup(content, max_width=200),
           icon=folium.Icon(color='blue',icon='star')
          ).add_to(map1)

    map1.save(file_path)


