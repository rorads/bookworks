import pytest
from app import app
import os
import shutil
from bookworks.md_publish import UPLOAD_FOLDER
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

@pytest.fixture(autouse=True)
def setup_and_cleanup():
    """Setup test environment and cleanup after each test"""
    # Setup
    logger.debug(f"Creating upload folder at {UPLOAD_FOLDER}")
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    
    yield
    
    # Cleanup
    if os.path.exists(UPLOAD_FOLDER):
        logger.debug(f"Cleaning up upload folder at {UPLOAD_FOLDER}")
        shutil.rmtree(UPLOAD_FOLDER)
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)

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
    expected_file = os.path.join(UPLOAD_FOLDER, "Test-Heading.epub")
    
    # Make sure the file doesn't exist before the test
    if os.path.exists(expected_file):
        os.remove(expected_file)
    
    # Process the content
    response = client.post('/', data={
        'markdown_content': test_content,
        'author': 'Test Author'
    })
    
    # Verify response
    assert response.status_code == 200
    assert response.mimetype == 'application/epub+zip'  # EPUB file download response
    
    # The file should be cleaned up by the app after sending
    assert not os.path.exists(expected_file), "File should be cleaned up after sending"

def test_upload_folder_exists():
    """Test that the upload folder is created"""
    assert os.path.exists(UPLOAD_FOLDER)
    assert os.path.isdir(UPLOAD_FOLDER) 