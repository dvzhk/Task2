import pandas as pd

def task_two(default_csv):
    traffic_accident_partip = pd.read_csv(default_csv, index_col=0, encoding="cp1251", sep=";", usecols=[0,1,2])

    preview = traffic_accident_partip.head()

    #Находим участников с числом ДТП > 1
    #для этого составляем общий список участников из одной колонки
    #
    traffic_accident_partip_one = traffic_accident_partip.iloc[:, 0]
    print(traffic_accident_partip_one)

    traffic_accident_partip_two = traffic_accident_partip.iloc[:, 1]
    print(traffic_accident_partip_two)
    #итоговый список:
    part_list = traffic_accident_partip_one.append(traffic_accident_partip_two).reset_index()

    more_than_one_time = part_list[part_list.iloc[:, 1].duplicated(keep=False)].sort_values(0)
    print(more_than_one_time)

    #Ищем тех, из данного списка, кто участвовал в ДТП дважды и более между собой
    podozrevaemie = more_than_one_time[more_than_one_time.iloc[:, 0].duplicated(keep=False)]

    #Искомый список
    spisok_podozrev = sorted(podozrevaemie[0].drop_duplicates().values)

    #Список сомнительных ДТП
    questionably_accs = traffic_accident_partip.loc[podozrevaemie.iloc[:, 0]].drop_duplicates().sort_index()

    return {'preview': preview,
            'preview_part_list': part_list.head(20),
            'more_than_one_time': more_than_one_time,
            'podozrevaemie': podozrevaemie,
            'spisok_podozrev': spisok_podozrev,
            'questionably_accs': questionably_accs
            }


