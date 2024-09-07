def valid_minecraft_nick(nickname: str) -> bool:
    return 3 <= len(nickname) <= 16 and nickname.replace('_', '').isalnum()