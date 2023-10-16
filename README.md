# morphological
Репозиторий для склонения фраз, исправления опечаток.


### Как установить
Клонируем репозиторий
```git clone https://github.com/kerplunk1/morphological.git```

Переходим в клонированный репозиторий
```cd morphological```

Запускаем в докер
```sudo docker compose up -d```

_По умолчанию работает на 8000 порту, можно поменять отредактировав файл_ ```docker-compose.yml```.


### Как отправлять запросы
Есть три метода:
1. /case_declensions - склоняет фразу под нужный падеж.
   
   Принимает JSON файл, который должен содержать два параметра с ключами "phrase" и "form".
   Во "phrase" передаем фразу, в "form" - падеж.

   Список падежей ***('nomn', 'gent', 'datv', 'accs', 'ablt', 'loct', 'voct', 'gen2', 'acc2', 'loc2', 'sing', 'plur')***

   Например, ```{"phrase": "Внутренние сети", "form": "datv"}```

2. /correct_mistake - исправляет опечатки.
   
   Принимает JSON файл, который должен содержать один параметр "phrase".

   Например, ```{"phrase": "Манометр техничский показывающий"}```

3. /all - исправляет ошибки и склонят.

   Принимает JSON файл, который должен содержать два параметра с ключами "phrase" и "form".
   Во "phrase" передаем фразу, в "form" - падеж.


### Возвращаемые данные
Возвращает JSON c ключом "result" и обработанной фразой.

Например, ```{'result': 'внутренним сетям'}```, ```{'result': 'манометру техническому показывающему}```
   

## Пример отправки запроса на python
```python

from requests import Session

url = 'http://192.168.101.252:8000/case_declensions'

data = ["Внутренние сети",
 "Противапожарный водопровод В2",
 "Насосы пожаротушения: Система В2",
 "Всасывающий трубопровод D300мм",
 "Напорный трубопровод D250мм",
 "Задвижка с невыдвижным шпинделем фланцевая чугунная, с обрезиненным клином под электропривод D250 vм PN16",
 "Электропривод к задвижке  JAFAR2911   (в комплекте с задвижкой)",
 "Задвижка ручная чугунная с обрезиненным клином с ответными фланцами",
 "Абратный клапан чугунный D250",
 "Клапан обратный осевой с сеткой фланцевый   DN 300 PN 0,25 МПа корпус чугун",
 "Отвод 90-2-273х8",
 "Манометр техничский показывающий 0-100ruc",
 "Кран трехходовой для манометра D15",
 "Тройник 325х8"
]

for i in data:
   response = session.post(url, json={'phrase': i, 'form': 'datv'})
   result = response.json()
   print(result)

```
