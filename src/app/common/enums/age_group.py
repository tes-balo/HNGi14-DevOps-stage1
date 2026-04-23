from enum import Enum


class AgeGroupEnum(str, Enum):
    CHILD = "child"
    TEENAGER = "teenager"
    ADULT = "adult"
    SENIOR = "senior"

    @staticmethod
    def classify_age_group(age: int):
        for max_age, group in AGE_GROUP_RANGES:
            if age <= max_age:
                return group

        return AgeGroupEnum.SENIOR


AGE_GROUP_RANGES = [
    (12, AgeGroupEnum.CHILD),
    (19, AgeGroupEnum.TEENAGER),
    (59, AgeGroupEnum.ADULT),
]
