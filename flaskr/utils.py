def is_leap_year(year):
    """Verifica se um ano é bissexto."""

    return (year % 4 == 0 and (year % 100 != 0 or year % 400 == 0))

def get_days_in_month(month, year):
    """Retorna o número de dias de um mês, considerando ano bissexto para 
    fevereiro.
    """

    days_in_month = {
        1: 31,
        2: 28 if not is_leap_year(year) else 29,
        3: 31,
        4: 30,
        5: 31,
        6: 30,
        7: 31,
        8: 31,
        9: 30,
        10: 31,
        11: 30,
        12: 31,
    }
    
    return days_in_month.get(month, 31)