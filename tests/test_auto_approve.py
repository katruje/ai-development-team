from datetime import datetime

def test_auto_approval(include_timestamp=False):
    """Test function to verify auto-approval is working.
    
    Args:
        include_timestamp: If True, includes a timestamp in the return value.
        
    Returns:
        str: A test message, optionally with a timestamp.
    """
    message = "Auto-approval test successful!"
    if include_timestamp:
        message += f" Tested at {datetime.now().isoformat()}"
    return message
