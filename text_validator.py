"""
Text Validation Utilities
Contains functions for validating and filtering text content.
"""

import re


# Common footer/navigation terms to filter out
FOOTER_TERMS = {
    "Meta", "Help", "Locations", "About", "Press", "API", "Jobs", "Privacy", 
    "Terms", "Contact", "Language", "Meta Verified", "Threads", "Follow", 
    "Following", "Like", "Reply", "View replies", "View all replies",
    "Log in", "Sign up", "More", "Liked", "Add a comment", "Post"
}


def is_valid_text(text, min_length=2):
    """
    Check if text is valid and meaningful
    
    Args:
        text (str): Text to validate
        min_length (int): Minimum length requirement
        
    Returns:
        bool: True if text is valid, False otherwise
    """
    if not text or len(text) < min_length:
        return False
    
    if text in FOOTER_TERMS:
        return False
    
    # Skip timestamp patterns
    if re.match(r'^\d+\s*(h|m|d|w|s|mo|y|ago|like|likes)$', text, re.IGNORECASE):
        return False
    
    # Skip action words
    if re.match(r'^(Reply|View|Follow|Following|Like|Unlike)$', text, re.IGNORECASE):
        return False
    
    return True


def is_valid_username(username):
    """
    Check if username is valid
    
    Args:
        username (str): Username to validate
        
    Returns:
        bool: True if username is valid, False otherwise
    """
    if not username:
        return False
    
    # Username validation
    if (len(username) > 30 or len(username) < 2 or 
        username.startswith('@') or username.endswith('Follow') or
        username in FOOTER_TERMS):
        return False
    
    return True


def is_valid_comment(comment, username=""):
    """
    Check if comment text is valid
    
    Args:
        comment (str): Comment text to validate
        username (str): Associated username for comparison
        
    Returns:
        bool: True if comment is valid, False otherwise
    """
    if not comment:
        return False
    
    # Comment validation
    if (
        (username and len(comment) <= len(username)) or
        (username and username == comment) or
        comment.startswith('Follow')):
        return False
    
    return True


def is_valid_username_comment_pair(username, comment):
    """
    Check if username and comment form a valid pair
    
    Args:
        username (str): Username to validate
        comment (str): Comment to validate
        
    Returns:
        bool: True if pair is valid, False otherwise
    """
    return (is_valid_username(username) and 
            is_valid_comment(comment, username) and 
            username != comment)


def clean_comment_text(comment):
    """
    Clean and normalize comment text
    
    Args:
        comment (str): Raw comment text
        
    Returns:
        str: Cleaned comment text
    """
    return comment.replace('\n', ' ').strip() if comment else ""


def create_comment_key(username, comment, max_length=50):
    """
    Create a unique key for comment deduplication
    
    Args:
        username (str): Username
        comment (str): Comment text
        max_length (int): Maximum length of comment portion in key
        
    Returns:
        str: Unique comment key
    """
    return f"{username}:{comment[:max_length]}"