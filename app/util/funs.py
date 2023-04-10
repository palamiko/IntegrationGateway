from app.dto.priority_enum import PriorityEnumZD, PriorityEnumJira


def mapping_priority(priority: PriorityEnumZD):
    match priority:
        case PriorityEnumZD.low:
            return PriorityEnumJira.standard

        case PriorityEnumZD.normal:
            return PriorityEnumJira.medium

        case PriorityEnumZD.urgent:
            return PriorityEnumJira.high

        case PriorityEnumZD.extra:
            return PriorityEnumJira.crit

