import pandas as pd
import os

def make_edges(traffic_accident_partip):
    """Создание ребер для построения графа"""
    pairs = []
    for row in traffic_accident_partip.itertuples():
        node = (row[1], row[2])
        pairs.append(node)
    return pairs


def preprocessing(default_csv):
    """Загрузка и предобработка файла" с данными"""
    traffic_accident_partip = pd.read_csv(default_csv, index_col=0, encoding="cp1251", sep=";", usecols=[0, 1, 2])
    return traffic_accident_partip


def graph_process(traffic_accident_partip):
    """Решение с использованием графов"""
    preview = traffic_accident_partip.head()
    pairs = make_edges(traffic_accident_partip)

    try:

        import networkx
        import matplotlib.pyplot as plt

        #Создаем ненаправленный граф
        graph = networkx.Graph()
        #Добавляем в граф ребра
        graph.add_edges_from(pairs)
        #Находим компоненты, которые содержат более двух вершин
        components = [x for x in networkx.connected_components(graph) if len(x) > 2]
        # Находим субграфы из компонент
        subgraphs = []
        for i in components:
            subgraphs.append(graph.subgraph(i))

        #Подготовка графики и сохранение
        abspath = os.path.abspath(os.path.dirname(__file__))
        graph = 'static'
        plots_array = []
        for j, i in enumerate(subgraphs):
            fig = plt.figure(figsize=(6, 4), dpi=75)
            #Замена текстовых подписей на цифровые
            labels = {x: y for x,y in zip(components[j], range(len(components[j])))}
            networkx.draw_spring(i, with_labels=True, font_size=12, labels=labels, font_color='white')
            #plt.show()

            img_name = f"Graph{j}.svg"
            img_path = os.path.join(abspath, graph, img_name)
            fig.savefig(img_path, format="svg", transparent=False)
            plots_array.append((img_name, labels))
        import_error = 0

    except ImportError:
        #Блок выполняется в отсутствие установленных модулей
        import_error = 1
        components = {}
        plots_array = [('Graph0.svg',
                        {'Галкина Елена Тарасовна': 0, 'Дорофеева Гулия Николаевна': 1,
                         'Миронов Пётр Александрович': 2, 'Пахомов Анатолий Васильевич': 3,
                         'Елисеева Сати Вячеславовна': 4, 'Шубин Всеволод Валерьевич': 5}),
                       ('Graph1.svg', {'Котова Виктория Архиповна': 0, 'Цветков Валерий Ростиславович': 1,
                                       'Петухова Медина Максимовна': 2, 'Королева Радмила Олеговна': 3}),
                       ('Graph2.svg', {'Мухамадеев Александр Валерьевич': 0, 'Сенчукова Екатерина Семеновна': 1,
                                       'Коробов Вадим Александрович': 2, 'Рогачев Антон Владимирович': 3}),
                       ('Graph3.svg', {'Воробьев Иван Александрович': 0, 'Павлова Мария Геннадиевна': 1,
                                       'Комин Сергей Николаевич': 2}),
                       ('Graph4.svg', {'Стрелков Евгений Егорович': 0, 'Александрова Лариса Евгеньевна': 1,
                                       'Силина Радмила Викторовна': 2}),
                       ('Graph5.svg', {'Архипова Анна Игоревна': 0, 'Суворов Илья Макарович': 1,
                                       'Федотов Ростислав Богуславович': 2, 'Мамонтов Мстислав Георгиевич': 3})]

    return {'import_error': import_error,
            'preview': preview,
            'pairs': pairs[:10],
            'components': components,
            'plots_array': plots_array}


def task_two(traffic_accident_partip):
    """Решение без использования графов"""
    #traffic_accident_partip = preprocessing(default_csv)
    preview = traffic_accident_partip.head()

    #Находим участников с числом ДТП > 1
    #для этого составляем общий список участников из одной колонки
    traffic_accident_partip_one = traffic_accident_partip.iloc[:, 0]
    traffic_accident_partip_two = traffic_accident_partip.iloc[:, 1]

    #итоговый список:
    part_list = traffic_accident_partip_one.append(traffic_accident_partip_two).reset_index()
    more_than_one_time = part_list[part_list.iloc[:, 1].duplicated(keep=False)].sort_values(0)

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


