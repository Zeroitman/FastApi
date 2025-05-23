class KeyPattern:
    @staticmethod
    def refresh_token_key(profile_id):
        return f"REFRESH:{profile_id}"
