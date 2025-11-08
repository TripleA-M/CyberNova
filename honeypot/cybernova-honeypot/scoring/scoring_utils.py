def calculate_fingerprint_score(headers):
    score = 0
    if 'User-Agent' in headers:
        user_agent = headers['User-Agent']
        if 'Mozilla' in user_agent:
            score += 2
        if 'Chrome' in user_agent:
            score += 2
        if 'Safari' in user_agent:
            score += 1
    if 'Referer' in headers:
        score += 1
    if 'Accept-Language' in headers:
        score += 1
    if 'X-Forwarded-For' not in headers:
        score += 3
    return min(score, 10)