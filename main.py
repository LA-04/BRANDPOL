import pandas as pd

def control_sites(df):
    sites = ["acmespb.ru", "apteka.ru", "aptekamos.ru", "aptekiplus.ru", "maksavit.ru", "ozerki.ru",
             "planetazdorovo.ru", "po-aptekam.ru", "rigla.ru", "stolichki.ru"]
    check_sites = set(df['Сайт'])
    not_scrin = [i for i in sites if i not in check_sites]
    return check_sites, not_scrin

def control_regions(df):
    regions = ["Казань", "Уфа", "Белгород", "Тула", "Санкт-Петербург", "Владимир", "Екатеринбург", "Воронеж",
               "Астрахань"]
    r = df.groupby(["Сайт"])["Регион"]
    u = {i[0]:set(i[1]) for i in r}
    not_control = {}
    for key, value in u.items():
        a = []
        for i in regions:
            if i not in value:
                a.append(i)
        not_control[key] = a
    return u, not_control

def control_SKU(df):
    r = df.groupby(["Сайт"])["Товар (офф. Наименование)"]
    u = {i[0]: len(set(i[1])) for i in r}
    return u

def print_info(df):
    work_sites, not_work_sites = control_sites(df)
    work_regions, not_work_region = control_regions(df)
    unic_position = control_SKU(df)

    print("--- " * 5)
    print(f"В соответвтвии с договором не отслеживаются сайты: {', '.join(not_work_sites)}")
    print(f"Отслеживаются сайты: {', '.join(work_sites)}")
    print("--- "*5)
    print("Информация по отслеживаемым сайтам:\n")

    for i in work_sites:
        print(f"Сайт {i}:")
        if len(not_work_region[i]) == 0:
            print("Отслеживается во всех регионах")
        else:
            print(f"Отслеживается в таких регионах как: {', '.join(work_regions[i])}")
            print(f"Не отслеживается в таких регионах как: {', '.join(not_work_region[i])}")
        if unic_position[i] > 1000:
            print(f"SKU в норме: {unic_position[i]}\n")
        else:
            print(f"SKU ниже нормы: {unic_position[i]}\n")

def main():
    df = pd.read_csv('test_an.csv')
    print_info(df)


if __name__ == "__main__":
    main()