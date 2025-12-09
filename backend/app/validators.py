"""Input validation functions for Recipe Repository"""
import re


def validate_username(username):
    """Validate username format and length"""
    if not username:
        return False, "Username is required"
    
    username = username.strip()
    
    if len(username) < 3:
        return False, "Username must be at least 3 characters"
    
    if len(username) > 80:
        return False, "Username must not exceed 80 characters"
    
    if not re.match(r'^[a-zA-Z0-9_-]+$', username):
        return False, "Username must contain only letters, numbers, hyphens, and underscores"
    
    return True, None


def validate_password(password):
    """Validate password strength"""
    if not password:
        return False, "Password is required"
    
    if len(password) < 8:
        return False, "Password must be at least 8 characters"
    
    if len(password) > 200:
        return False, "Password must not exceed 200 characters"
    
    return True, None


def validate_email(email):
    """Validate email format"""
    if not email:
        return False, "Email is required"
    
    email = email.strip().lower()
    
    # RFC 5322 simplified email validation
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    
    if not re.match(pattern, email):
        return False, "Invalid email format"
    
    if len(email) > 120:
        return False, "Email must not exceed 120 characters"
    
    return True, None


def validate_recipe_title(title):
    """Validate recipe title"""
    if not title:
        return False, "Recipe title is required"
    
    title = title.strip()
    
    if len(title) < 2:
        return False, "Recipe title must be at least 2 characters"
    
    if len(title) > 200:
        return False, "Recipe title must not exceed 200 characters"
    
    return True, None


def validate_page_number(page):
    """Validate pagination page number"""
    if page < 1:
        return False, "Page number must be at least 1"
    
    return True, None


def validate_per_page(per_page):
    """Validate per_page parameter"""
    if per_page < 1:
        return False, "Per page must be at least 1"
    
    if per_page > 100:
        return False, "Per page cannot exceed 100 items"
    
    return True, None


def validate_search_query(query):
    """Validate search query"""
    if not query:
        return False, "Search query is required"
    
    query = query.strip()
    
    if len(query) < 2:
        return False, "Search query must be at least 2 characters"
    
    if len(query) > 200:
        return False, "Search query must not exceed 200 characters"
    
    return True, None
