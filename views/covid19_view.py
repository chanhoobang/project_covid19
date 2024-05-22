from flask import Blueprint, render_template, request

bp = Blueprint("covid19", __name__, url_prefix="/covid19")


# covid19.html 파일을 화면에 띄우는 라우터
@bp.route("/")
def covid19():
    return render_template("covid19/covid19.html")


# 나잇대별, 성별 확진자 데이터를 받아 JSON 형태로 반환하는 라우터

# TF: 데이터 베이스에 데이터가 존재하는지 여부 표기
# data_type: 받아올 데이터의 종류
# current_date: 데이터베이스에서 가져올 날짜 정보
# col_name: 받아온 데이터의 컬럼명 (국가명(country), 성별(gender), 나잇대(age) 등 고유 컬럼 포함)
# row_data: 사용할 데이터 [[항목1], [항목2]... [항목n]]
# 예) 항목1 = [male, total_cases, active_cases, death_cases, re_cases, re_rate]
# get_data 함수: 데이터베이스에서 데이터를 가져오는 기능

@bp.route("/get_covid19_data", methods=("POST", ))
def get_covid19_data():

    TF = True

    current_date = request.form.get("date")
    data_type = request.form.get("type")

    default_col_name = ["total_cases", "active_cases", "death_cases", "re_cases", "re_rate", "date"]
    col_name = []

    # 데이터베이스에서 받아온 데이터를 row_data에 입력한다.
    # 미완성 @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    row_data = get_data(current_date)

    if data_type == "gender":
        col_name = ["gender"] + default_col_name
    elif data_type == "age":
        col_name = ["age"] + default_col_name
    else:
        TF = False

    return {"TF":TF, "col_name": col_name, "row_data": row_data}