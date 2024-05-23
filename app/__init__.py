from flask import Flask, Blueprint
from sqlalchemy import inspect

from app.database import ENGINE, SESSION, BASE
from app.modules.positions import Positions


def create_app():
    app = Flask(__name__)

    # 어플리케이션 컨텍스트 내에서 DB 초기화
    with app.app_context():
        inspector = inspect(ENGINE)

        # 모델 호출
        from app.models.position import KoreaPosition

        # 모든 모델로부터 테이블명 추출
        tables_to_check = list(BASE.metadata.tables.keys())
        existing_tables = inspector.get_table_names()

        # 데이터베이스를 최초 1회만 만들기 위함.
        # 존재하지 않는 테이블만 생성
        table_create = [table for table in tables_to_check if table not in existing_tables]

        # 테이블을 만들어야 하는 경우?
        if table_create:

            # 사용할 클래스 호출
            positions = Positions()

            # 테이블 생성
            BASE.metadata.create_all(ENGINE)

            # 국내 좌표값 데이터 입력 처리
            korea_position_data = positions.get_dataset_positions('korea')
            positions.insert_table_korea_position(korea_position_data)

        from .views import covid19_view
        app.register_blueprint(covid19_view.bp)

    return app
