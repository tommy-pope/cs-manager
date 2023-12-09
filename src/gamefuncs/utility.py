from math import ceil


def find_closest_square(number: int) -> int:
    power = 1
    diff = 999

    while True:
        squared = pow(2, power)
        new_diff = abs(squared - number)

        if new_diff >= diff:
            if pow(2, power - 1) > number:
                return pow(2, power - 2)
            return pow(2, power - 1)

        diff = new_diff

        power += 1


def add_to_date(date: list, days: int = 0, months: int = 0, years: int = 0) -> list:
    new_day = date[1] + days
    new_day = 1 if new_day % 31 == 0 else new_day % 31
    carried_months = (date[1] + days) // 31

    new_month = date[0] + months + carried_months
    new_month = 1 if new_month % 12 == 0 else new_month % 12
    carried_years = (date[0] + months + carried_months) // 12

    new_year = date[2] + years + carried_years

    return [new_month, new_day, new_year]


def subtract_from_date(
    date: list, days: int = 0, months: int = 0, years: int = 0
) -> list:
    new_day = date[1] - days
    new_day = 1 if new_day % 31 == 0 else new_day % 31
    carried_months = ceil(abs(date[1] - days) / 31)

    new_month = date[0] - months - carried_months
    new_month = 1 if new_month % 12 == 0 else new_month % 12

    carried_years = abs(date[0] - months - carried_months) // 12
    new_year = date[2] - years - carried_years

    return [new_month, new_day, new_year]


def check_date_equality(date_one: list, date_two: list) -> bool:
    return (
        date_one[0] == date_two[0]
        and date_one[1] == date_two[1]
        and date_one[2] == date_two[2]
    )


def find_team_in_event(event, team1) -> bool:
    return [team for team in event.teams if team.info.id == team1.info.id]
