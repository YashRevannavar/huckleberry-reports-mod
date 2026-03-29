from enum import Enum, auto

class ActivityType(str, Enum):
    FEED = "Feed"
    DIAPER = "Diaper"
    SLEEP = "Sleep"
    TEMP = "Temp"
    GROWTH = "Growth"
    TUMMY_TIME = "Tummy time"
    BATH = "Bath"
    PUMP = "Pump"
    UNKNOWN = "Unknown"

    @classmethod
    def from_string(cls, value: str):
        for member in cls:
            if member.value == value:
                return member
        return cls.UNKNOWN

class FeedType(str, Enum):
    BREAST_MILK = "Breast Milk"
    FORMULA = "Formula"
    BOTH = "Both"
    UNKNOWN = "Unknown"

    @classmethod
    def from_string(cls, value: str):
        if not value or not isinstance(value, str):
            return cls.UNKNOWN
        for member in cls:
            if member.value == value:
                return member
        return cls.UNKNOWN

class DiaperCondition(str, Enum):
    PEE = "Pee"
    POO = "Poo"
    BOTH = "Both"
    UNKNOWN = "Unknown"

    @classmethod
    def from_string(cls, value: str):
        if not value or not isinstance(value, str):
            return cls.UNKNOWN
        value_lower = value.lower()
        if "both" in value_lower:
            return cls.BOTH
        elif "poo" in value_lower and "pee" not in value_lower:
            return cls.POO
        elif "pee" in value_lower and "poo" not in value_lower:
            return cls.PEE
        return cls.UNKNOWN
