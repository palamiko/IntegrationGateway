from enum import Enum


class PriorityEnumZD(Enum):
    low = 'Низкий'
    normal = 'Нормальный'
    urgent = 'Срочный'
    extra = 'Экстренный'


class PriorityEnumJira(Enum):
    standard = 'Стандартный'
    medium = 'Средний'
    high = 'Высокий'
    crit = 'Критический'
