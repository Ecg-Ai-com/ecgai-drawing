from enum import IntEnum


class Artifact(IntEnum):
    ARTIFACT_UNSPECIFIED = 0
    SALT = 1
    PEPPER = 2
    SALT_AND_PEPPER = 3
    POISSON = 4
    SPECKLE = 5
    NONE = 6
