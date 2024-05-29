import os

from flask import Blueprint, render_template, request
from app.database import SESSION
from app.modules import visualization_modules
from app.modules.common import Common
from app.models.detail import GlobalData

visualization_bp = Blueprint("visualization", __name__)

file_path = "app/static/map/map.html"
current_date = Common.find_latest_date(GlobalData)[0].data_date


# 국내 맵을 그리는 라우터
@visualization_bp.route("/covid/visualization_korea", methods=["GET", ])
def visualization_korea():
    if os.path.exists(file_path):
        os.remove("app/static/map/map.html")
    date = request.args.get("date")
    if date:
        pass
    else:
        date = current_date[:10]

    print(date)

    list_age = visualization_modules.get_data("age", date)
    list_gender = visualization_modules.get_data("gender", date)

    print(list_age)

    if list_age:
        list_age = Common.add_comma_to_list(list_age)

    if list_gender:
        list_gender = Common.add_comma_to_list(list_gender)

    visualization_modules.draw_map("korea", date+" 00:00:00")

    return render_template('_pages/covid/local.html', list_age=list_age, list_gender=list_gender)


# 해외 맵을 그리는 라우터
@visualization_bp.route("/covid/visualization_global", methods=["GET"])
def visualization_global():
    
    date = request.args.get("date")
    if date:
        pass
    else:
        date = current_date[:10]

    if os.path.exists(file_path):
        os.remove("app/static/map/map.html")

    visualization_modules.draw_map("global", date+" 00:00:00")

    page = request.args.get('page', 1, type=int)
    per_page = 20

    items, total_pages = Common.paginate(GlobalData, date+" 00:00:00", page, per_page)
    columns = Common.get_columns(GlobalData)

    temp_global_data = []

    for data in items:
        temp_dict = {
            "nation":data.nation,
            "total_cases":Common.add_comma(data.total_cases),
            "active_cases":Common.add_comma(data.active_cases),
            "death_cases":Common.add_comma(data.death_cases),
            "re_rate":data.re_rate,
            "re_cases":Common.add_comma(data.re_cases)
        }

        temp_global_data.append(temp_dict)

    return render_template(
        '_pages/covid/global.html',
        items=items,
        columns=columns,
        page=page,
        date=request.args.get("date"),
        total_pages=total_pages,
        global_data=temp_global_data
    )


