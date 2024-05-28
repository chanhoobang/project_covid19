from flask import Flask
from sqlalchemy import inspect

from app.database import ENGINE, SESSION, BASE
from app.models.detail import GlobalData
from app.modules.common import Common
from app.modules.korea import KoreaModule
from app.modules.world import WorldModule


# 플라스크 어플리케이션 생성
def create_app():

    # 플라스크 어플리케이션 초기화
    app = Flask(__name__)

    # 블루프린트 불러옴
    from app.views.home import home_bp
    from app.views.information import information_bp
    from app.views.visualization import visualization_bp

    # 블루프린트 등록
    app.register_blueprint(home_bp)
    app.register_blueprint(information_bp)
    app.register_blueprint(visualization_bp)

    # 어플리케이션 컨텍스트 내에서 DB 초기화
    with app.app_context():
        inspector = inspect(ENGINE)

        # 모델 호출
        from app.models.position import KoreaPosition
        from app.models.position import GlobalPosition
        from app.models.detail import AgeData
        from app.models.detail import GenderData
        from app.models.detail import GlobalData
        from app.models.detail import KoreaData

        # 모든 모델로부터 테이블명 추출
        tables_to_check = list(BASE.metadata.tables.keys())
        existing_tables = inspector.get_table_names()

        # 데이터베이스를 최초 1회만 만들기 위함.
        # 존재하지 않는 테이블만 생성
        table_create = [table for table in tables_to_check if table not in existing_tables]

        # 테이블을 만들어야 하는 경우?
        if table_create:

            # 테이블 생성
            BASE.metadata.create_all(ENGINE)

        # 국내 데이터 입력 처리
        # 단, 데이터의 갯수가 0일 때에만.
        if Common.table_row_count(KoreaPosition) == 0:
            KoreaModule.insert_korea_position()

        if Common.table_row_count(AgeData) == 0:
            KoreaModule.insert_korea_ages_data()

        if Common.table_row_count(GenderData) == 0:
            KoreaModule.insert_korea_gender_data()

        if Common.table_row_count(KoreaData) == 0:
            KoreaModule.insert_korea_data()

        # 해외 데이터 입력처리 (국내 데이터와 동일)
        if Common.table_row_count(GlobalData) == 0:
            WorldModule.insert_global_date_data()

        if Common.table_row_count(GlobalPosition) == 0:
            WorldModule.insert_global_position()

    return app
