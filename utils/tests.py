from django.core.files.uploadedfile import SimpleUploadedFile
from faker import Faker

faker = Faker()


def generate_test_image():
    return SimpleUploadedFile("test_generated_image.jpg", faker.image(), content_type="image/jpg")