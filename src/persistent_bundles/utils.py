def is_same_major_semver(s1: str, s2: str) -> bool:
    return s1.split(".")[0] == s2.split(".")[0]
