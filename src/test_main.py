from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_read_images():
    request_code = 'a00f155c-e97a-4435-8181-f247eae08862'
    response = client.get(f"/frames/{request_code}")
    assert response.status_code == 200
    assert response.json() == [
        {
            "request_code": "a00f155c-e97a-4435-8181-f247eae08862",
            "file_name": "73f3f7ca-b528-47a7-9f09-97dbb9abebb7.jpeg",
            "reg_date": "2022-06-17T19:25:05"
        },
        {
            "request_code": "a00f155c-e97a-4435-8181-f247eae08862",
            "file_name": "0e6c41e8-3421-43e0-8dc5-7849f61b4b5f.jpeg",
            "reg_date": "2022-06-17T19:25:05"
        }
    ]


def test_read_images_invalid_code():
    request_code = 'code'
    response = client.get(f"/frames/{request_code}")
    assert response.status_code == 404
    assert response.json() == {"detail": "No files with such request code"}


def test_upload_images():
    filename = '9ce3cfa5-6033-4d09-91e6-e2c423a76e19.jpeg'
    response = client.post(
        "/frames/",
        files={'files': open(filename, "rb")},
    )
    assert response.status_code == 200


def test_delete_images():
    request_code = '6b85241f-0854-46a8-9137-7b68621ca793'
    response = client.delete(f"/frames/{request_code}")
    assert response.status_code == 200
    assert response.json() == {"message": "1 file(s) were successfully deleted"}


def test_delete_images_invalid_code():
    request_code = 'code'
    response = client.get(f"/frames/{request_code}")
    assert response.status_code == 404
    assert response.json() == {"detail": "No files with such request code"}
