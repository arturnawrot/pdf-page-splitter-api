from pdf_splitter.tests.base_test import BaseTest
import os

class TestPDFSplitter(BaseTest):
    def setup_method(self):        
        super().setup_method()  # Ensure the parent class's setup is called
        if not os.path.exists(self.UPLOAD_FOLDER):
            os.makedirs(self.UPLOAD_FOLDER)
        self.initial_files = set(os.listdir(self.UPLOAD_FOLDER))

    def teardown_method(self):
        super().teardown_method()  # Ensure the parent class's teardown is called
        current_files = set(os.listdir(self.UPLOAD_FOLDER))
        new_files = current_files - self.initial_files
        for file in new_files:
            os.remove(os.path.join(self.UPLOAD_FOLDER, file))

    def test_valid_pdf_splitting(self, client):
        test_url = self.FIXTURES_URL + 'valid_pdf.pdf'
        response = client.post('/split-pdf', json={'url': test_url})
        assert response.status_code == 200
        data = response.get_json()
        assert isinstance(data, list) and len(data) == 4

    def test_invalid_file_type(self, client):
        test_url = self.FIXTURES_URL + 'invalid_format.jpg'
        response = client.post('/split-pdf', json={'url': test_url})
        assert response.status_code == 400

    def test_url_not_found(self, client):
        test_url = self.FIXTURES_URL + 'this_file_does_not_exist.pdf'
        response = client.post('/split-pdf', json={'url': test_url})
        assert response.status_code == 404

    def test_no_url_provided(self, client):
        response = client.post('/split-pdf', json={})
        assert response.status_code == 400
        assert "No URL provided" in response.get_data(as_text=True)

    def test_unexpected_error(self, client):
        test_url = self.FIXTURES_URL + 'corrupted_pdf.pdf'
        response = client.post('/split-pdf', json={'url': test_url})
        assert response.status_code == 500
        assert "Failed to process PDF" in response.get_data(as_text=True)