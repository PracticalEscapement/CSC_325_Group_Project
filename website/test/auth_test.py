import pytest
from flask import session
from werkzeug.security import generate_password_hash
from ..auth import auth
from ..models import User
from .. import create_app
from .. import db
from .. import db

@pytest.fixture
def app():
    # Import app factory function
    app = create_app()
    
    # Configure app for testing
    app.config.update({
        'TESTING': True,
        'WTF_CSRF_ENABLED': False,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:'
    })
    
    # Create test database and context
    with app.app_context():
        db.create_all()
        
        # Create a test user
        test_user = User(
            email='test@example.com',
            username='Test User',
            password=generate_password_hash('password123')
        )
        db.session.add(test_user)
        db.session.commit()
        
        yield app
        
        # Clean up
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def runner(app):
    return app.test_cli_runner()

# Login Tests
def test_login_page_loads(client):
    """Test that login page loads correctly."""
    response = client.get('/login')
    assert response.status_code == 200
    assert b'Login' in response.data

def test_successful_login(client):
    """Test successful login with correct credentials."""
    response = client.post('/login', data={
        'email': 'test@example.com',
        'password': 'password123'
    }, follow_redirects=True)
    
    assert response.status_code == 200
    assert b'Logged in successfully' in response.data
    
    with client.session_transaction() as sess:
        assert sess['user'] == 'test@example.com'

def test_login_with_incorrect_password(client):
    """Test login failure with incorrect password."""
    response = client.post('/login', data={
        'email': 'test@example.com',
        'password': 'wrongpassword'
    }, follow_redirects=True)
    
    assert response.status_code == 200
    assert b'Incorrect password' in response.data

def test_login_with_nonexistent_email(client):
    """Test login failure with non-existent email."""
    response = client.post('/login', data={
        'email': 'nonexistent@example.com',
        'password': 'password123'
    }, follow_redirects=True)
    
    assert response.status_code == 200
    assert b'Email doesnt exists' in response.data

# Sign-up Tests
def test_signup_page_loads(client):
    """Test that signup page loads correctly."""
    response = client.get('/sign-up')
    assert response.status_code == 200
    assert b'Sign Up' in response.data

def test_successful_signup(client):
    """Test successful user registration."""
    response = client.post('/sign-up', data={
        'email': 'newuser@example.com',
        'firstName': 'New',
        'lastName': 'User',
        'password1': 'password123',
        'password2': 'password123'
    }, follow_redirects=True)
    
    assert response.status_code == 200
    assert b'User created successfully' in response.data
    
    # Verify user was added to database
    user = User.query.filter_by(email='newuser@example.com').first()
    assert user is not None
    assert user.username == 'New User'

def test_signup_with_invalid_email(client):
    """Test signup failure with invalid email format."""
    response = client.post('/sign-up', data={
        'email': 'invalid-email',
        'firstName': 'New',
        'lastName': 'User',
        'password1': 'password123',
        'password2': 'password123'
    }, follow_redirects=True)
    
    assert response.status_code == 200
    assert b'Invalid email address' in response.data

def test_signup_with_existing_email(client):
    """Test signup failure when email already exists."""
    response = client.post('/sign-up', data={
        'email': 'test@example.com',  # Already exists
        'firstName': 'Another',
        'lastName': 'User',
        'password1': 'password123',
        'password2': 'password123'
    }, follow_redirects=True)
    
    assert response.status_code == 200
    assert b'Email already exists' in response.data

def test_signup_with_mismatched_passwords(client):
    """Test signup failure when passwords don't match."""
    response = client.post('/sign-up', data={
        'email': 'another@example.com',
        'firstName': 'Another',
        'lastName': 'User',
        'password1': 'password123',
        'password2': 'differentpassword'
    }, follow_redirects=True)
    
    assert response.status_code == 200
    assert b"Passwords don't match" in response.data

# Logout Tests
def test_logout(client):
    """Test successful logout."""
    # First login
    client.post('/login', data={
        'email': 'test@example.com',
        'password': 'password123'
    })
    
    # Then logout
    response = client.get('/logout', follow_redirects=True)
    
    assert response.status_code == 200
    assert b'You have been logged out' in response.data
    
    with client.session_transaction() as sess:
        assert 'user' not in sess