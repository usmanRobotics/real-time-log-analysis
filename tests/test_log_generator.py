import re
from log_generator import generate_log

def test_generate_log():
    log_entry = generate_log()
    
    # Check if log_entry matches the expected format
    pattern = re.compile(r'\d+\.\d+\.\d+\.\d+ - - \[\d{2}/\w+/\d{4}:\d{2}:\d{2}:\d{2} \+\d{4}\] "\w+ /[a-zA-Z]* HTTP/1.1" \d{3} - "-" ".*"')
    assert pattern.match(log_entry), "Log entry does not match the expected format."
