from math import ceil

def add_to_date(date: list, days: int = 0, months: int = 0, years: int = 0) -> list:
    new_day = date[1] + days
    new_day = 1 if new_day % 31 == 0 else new_day % 31
    carried_months = (date[1] + days) // 31

    new_month = date[0] + months + carried_months
    new_month = 1 if new_month % 12 == 0 else new_month % 12
    carried_years = (date[0] + months + carried_months) // 12

    new_year = date[2] + years + carried_years

    return [new_month, new_day, new_year]

def subtract_from_date(date: list, days: int = 0, months: int = 0, years: int = 0) -> list:
    new_day = date[1] - days
    new_day = 1 if new_day % 31 == 0 else new_day % 31
    carried_months = ceil(abs(date[1] - days) / 31)
    
    new_month = date[0] - months - carried_months
    new_month = 1 if new_month % 12 == 0 else new_month % 12
    carried_years = ceil(abs(date[0] - months - carried_months) / 12)

    new_year = date[2] - years - carried_years

    return [new_month, new_day, new_year]

def find_team_in_event(event, team1) -> bool:
    return [team for team in event.teams if team.info.id == team1.info.id]