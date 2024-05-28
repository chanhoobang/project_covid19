from flask import Blueprint, render_template, request, url_for
from app.modules import visualization_modules
from app.modules.common import Common
from app.models.detail import GlobalData
import os

visualization_bp = Blueprint("visualization", __name__)

file_path = "app/static/map/map.html"

# 국내 맵을 그리는 라우터
@visualization_bp.route("/visualization_korea", methods=["GET", ])
def visualization_korea():
    if os.path.exists(file_path):
        os.remove("app/static/map/map.html")

    date = request.args.get("date")

    list_age = visualization_modules.get_data("age", date)
    list_gender = visualization_modules.get_data("gender", date)

    if list_age:
        list_age = Common.add_comma_to_list(list_age)

    if list_gender:
        list_gender = Common.add_comma_to_list(list_gender)

    visualization_modules.draw_map("korea", date+" 00:00:00")

    return render_template('_pages/covid/local.html', list_age=list_age, list_gender=list_gender)

# 해외 맵을 그리는 라우터
@visualization_bp.route("/visualization_global", methods=["GET"])
def visualization_global():

    if os.path.exists(file_path):
        os.remove("app/static/map/map.html")

    date = request.args.get("date")

    page = request.args.get("page", type=int, default=1)
    global_data = Common.get_model_page(GlobalData, date+" 00:00:00", page, 20)

    visualization_modules.draw_map("global", date+" 00:00:00")
    
    temp_global_data = global_data

    for idx in range(len(temp_global_data)):
        temp_global_data[idx].total_cases = Common.add_comma(temp_global_data[idx].total_cases)
        temp_global_data[idx].active_cases = Common.add_comma(temp_global_data[idx].active_cases)
        temp_global_data[idx].death_cases = Common.add_comma(temp_global_data[idx].death_cases)
        temp_global_data[idx].re_cases = Common.add_comma(temp_global_data[idx].re_cases)

    return render_template('_pages/covid/global.html', global_data=temp_global_data, page=page, date=date)
