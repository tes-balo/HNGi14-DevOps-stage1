from enum import Enum


class AgeGroup(str, Enum):
    CHILD = "CHILD"
    TEENAGER = "TEENAGER"
    ADULT = "ADULT"
    SENIOR = "SENIOR"

    @staticmethod
    def classify_age_group(age: int):
        for max_age, group in AGE_GROUP_RANGES:
            if age <= max_age:
                return group

        return AgeGroup.SENIOR


AGE_GROUP_RANGES = [
    (12, AgeGroup.CHILD),
    (19, AgeGroup.TEENAGER),
    (59, AgeGroup.ADULT),
]
