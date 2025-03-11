import pytest
from app import app
import os

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_index_get(client):
    """Test that the index page loads correctly"""
    response = client.get('/')
    assert response.status_code == 200
    assert b'form' in response.data

def test_post_without_content(client):
    """Test posting without any content returns an error"""
    response = client.post('/', data={})
    assert b'Please provide either markdown content or upload a file' in response.data

def test_post_with_markdown_content(client):
    """Test posting with markdown content"""
    test_content = "# Test Heading\nThis is a test."
    response = client.post('/', data={
        'markdown_content': test_content,
        'author': 'Test Author'
    })
    assert response.status_code == 200
    assert response.mimetype == 'application/epub+zip'  # EPUB file download response
    os.remove("Test Heading.epub")


def test_upload_folder_exists():
    """Test that the upload folder is created"""
    assert os.path.exists('uploads')
    assert os.path.isdir('uploads') 