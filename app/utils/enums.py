import enum


class FlightStatus(str, enum.Enum):
    OnTime = "OnTime"
    Late = "Late"
    Boarding = "Boarding"
    TakenOff = "TakenOff"

    @classmethod
    def has_value(cls, value):
        return any(value == item.value for item in cls)


class TicketStatus(str, enum.Enum):
    Reserved = "Reserved"
    PaidFor = "Booked"

    @classmethod
    def has_value(cls, value):
        return any(value == item.value for item in cls)
