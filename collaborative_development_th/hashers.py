from django.contrib.auth import hashers


class Argon2PasswordHasher(hashers.Argon2PasswordHasher):
    """Argon2id hasher with OWASP recommended configuration

    https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html#argon2id
    """

    memory_cost = 19456  # 19 MiB
    time_cost = 2
    parallelism = 1
