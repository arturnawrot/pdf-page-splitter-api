import os
import pytest
from pdf_splitter.app import app as flask_app
from multiprocessing import Process

def run_app():
    flask_app.run(host='127.0.0.1', port=8282)

class BaseTest:
    def setup_method(self):
        self.server = Process(target=run_app)
        self.server.start()

        self.ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../'))
        self.UPLOAD_FOLDER = os.path.join(self.ROOT_DIR, 'uploaded_files')
        self.FIXTURES_URL = f'http://127.0.0.1:8282/fixtures/'

    def teardown_method(self):
        self.server.terminate()
        self.server.join()

    @pytest.fixture
    def app(self):  # Corrected method signature
        yield flask_app

    @pytest.fixture
    def client(self, app):  # Added `self` and corrected signature
        return app.test_client()