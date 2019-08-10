import hashlib
from django.core.files.base import ContentFile, File
from django.test import TestCase
from faker import Faker

from alerts.models import hash_file, AlertVideo

fake = Faker()


class HashFile(TestCase):

    def setUp(self):
        File.DEFAULT_CHUNK_SIZE = 64 * 2
        self.small_file_content: str = fake.text(max_nb_chars=50)
        self.small_file = ContentFile(self.small_file_content, 'file')
        self.big_file_content: str = fake.text(max_nb_chars=2000)
        self.big_file = ContentFile(self.big_file_content, 'file')

    def test_hash_file_with_one_chunk(self):
        hasher = hashlib.sha256()
        hasher.update(self.small_file_content.encode())

        expected_hash = hasher.hexdigest()
        actual_hash = hash_file(self.small_file)
        self.assertEquals(actual_hash, expected_hash)

    def test_hash_file_with_multiple_chunks(self):
        hasher = hashlib.sha256()
        hasher.update(self.big_file_content.encode())

        expected_hash = hasher.hexdigest()
        actual_hash = hash_file(self.big_file)
        self.assertEquals(actual_hash, expected_hash)


class TestAlertVideo(TestCase):

    def setUp(self):
        File.DEFAULT_CHUNK_SIZE = 64 * 2
        self.small_file_content: str = fake.text(max_nb_chars=50)
        self.small_file = ContentFile(self.small_file_content, 'small_file')
        self.valid_alert_video = AlertVideo(video=self.small_file)

    def test_save_valid_video__stores_name(self):
        self.valid_alert_video.save()
        self.assertEquals(self.valid_alert_video.name, self.small_file.name)

    def test_save_valid_video__stores_hash(self):
        self.valid_alert_video.save()
        self.assertIsNotNone(self.valid_alert_video.hash)
        self.assertNotEquals(self.valid_alert_video.hash, '')
        self.assertGreater(len(self.valid_alert_video.hash), 10)
