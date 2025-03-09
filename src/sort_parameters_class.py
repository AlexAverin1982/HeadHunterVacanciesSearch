class SortParameter:
    SALARY_MIN = 1
    SALARY_MAX = 2
    SALARY_AVG = 3
    NAME = 4
    EMPLOYER = 5

    def __init__(self, sort_aspect: int, ascending_order: bool = True):
        self.aspect: int = sort_aspect
        self.ascending_order: bool = ascending_order
