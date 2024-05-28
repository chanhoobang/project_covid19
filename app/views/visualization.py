import os

from flask import Blueprint, render_template, request
from app.database import SESSION
from app.modules import visualization_modules
from app.modules.common import Common
from app.models.detail import GlobalData

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

    visualization_modules.draw_map("korea", date+" 00:00:00")

    return render_template('_pages/covid/local.html', list_age=list_age, list_gender=list_gender)


# 해외 맵을 그리는 라우터
@visualization_bp.route("/visualization_global", methods=["GET"])
def visualization_global():
    if os.path.exists(file_path):
        os.remove("app/static/map/map.html")

    date = f'{request.args.get("date")} 00:00:00'
    page = request.args.get('page', 1, type=int)
    per_page = 20

    items, total_pages = Common.paginate(GlobalData, date, page, per_page)
    columns = Common.get_columns(GlobalData)
    visualization_modules.draw_map('global', date)

    return render_template(
        '_pages/covid/global.html',
        items=items,
        columns=columns,
        page=page,
        date=request.args.get("date"),
        total_pages=total_pages,
        global_data=items
    )


