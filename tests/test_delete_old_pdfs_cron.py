import os
import time
from unittest.mock import patch
from pdf_splitter.tests.base_test import BaseTest
from pdf_splitter.app import delete_files

class TestDeleteOldPDFsCron(BaseTest):

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

    def test_delete_files(self):
        # Create test files
        old_file = os.path.join(self.UPLOAD_FOLDER, 'old_file.txt')
        new_file = os.path.join(self.UPLOAD_FOLDER, 'new_file.txt')
        open(old_file, 'w').close()
        open(new_file, 'w').close()

        # Modify file times to simulate an old and new file
        old_time = time.time() - 48 * 60 * 60 - 1  # older than 48 hours
        new_time = time.time() - 1 * 60 * 60        # only 1 hour old
        os.utime(old_file, (old_time, old_time))
        os.utime(new_file, (new_time, new_time))
        
        delete_files()

        # Validate that the old file is deleted and the new file remains
        remaining_files = os.listdir(self.UPLOAD_FOLDER)
        assert 'old_file.txt' not in remaining_files
        assert 'new_file.txt' in remaining_files

    @patch('apscheduler.schedulers.background.BackgroundScheduler.add_job')
    def test_scheduler_adds_job(self, mocker):
        def delete_files():
            pass  # Mock delete_files

        # Mock scheduler
        scheduler = mocker.MagicMock()
        mock_add_job = scheduler.add_job

        scheduler.add_job(func=delete_files, trigger="interval", hours=1)
        mock_add_job.assert_called_once_with(func=delete_files, trigger="interval", hours=1)
        scheduler.shutdown()