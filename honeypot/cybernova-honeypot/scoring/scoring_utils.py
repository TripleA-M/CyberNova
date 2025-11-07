def calculate_fingerprint_score(headers):
    score = 0

    # Check for common headers that indicate a legitimate request
    if 'User-Agent' in headers:
        user_agent = headers['User-Agent']
        # Example scoring based on User-Agent
        if 'Mozilla' in user_agent:
            score += 2
        if 'Chrome' in user_agent:
            score += 2
        if 'Safari' in user_agent:
            score += 1

    # Check for the presence of other headers
    if 'Referer' in headers:
        score += 1
    if 'Accept-Language' in headers:
        score += 1

    # Score based on the absence of certain headers
    if 'X-Forwarded-For' not in headers:
        score += 3

    # Cap the score at 10
    return min(score, 10)