# Tank-Duel

# Краткая характеристика
* Наименование программы: **Танковая дуэль** - 2D аркада для двух игроков.
* Назначение программы: игровая программа для **развлечения**.
* Конечные пользователи: любители **ретро-игр** на платформе PC.

# Техническое задание
Разработать игровое приложение на языке Python с использованием возможностей библиотеки [**PyGame**](https://www.pygame.org/news). 

![pygame](./pic/logo-pygame.png)

# Сборка и запуск
Разработка и тестирование программы осуществлено в операционной системе **Windows 10**.

## Файловая структура проекта
```text
[Tank-Duel]            # Директория приложения
├── [pic]              # Изображения
├── [sound]            # Звуки
├── [sprite]           # Спрайты
├── params.py          # Python-файл с параметрами игры
├── README.md          # Документация к игре
├── requirements.txt   # Список внешних зависимостей
└── tank-duel.py       # main-файл
```

Для успешного запуска и нормальной работы в операционной системе должны быть установлены следующие **компоненты**:

+ язык **Python 3.9.8**
+ библиотека **pygame 2.1.1**
+ библиотека **numpy 1.22.0**

# Функциональные возможности
Два игрока управляют своими танками (у каждого игрока по одному танку). Их задача -- **уничтожать друг друга и собирать очки**. Конечная цель -- **победить игрока-противника** (сделать так, чтобы количество жизней противника было равно нулю).

## Игроки

![player_1](./pic/player_1.png 'Игрок 1') ![player_2](./pic/player_2.png 'Игрок 2')

Первый и второй игрок **управляют** жёлтым и зелёным танком соответственно. Игроки могут **производить выстрелы**.
Попадая в танк, пуля **отнимает жизнь и уничтожает танк**.
При исчерпании количества жизней, игра переходит на новый уровень или завершается.

## Блоки (тайлы)

### Кирпичи

![bricks](./pic/bricks.png 'Кирпичи')

Если пуля попадёт по кирпичам, то она их **уничтожит**.
Танк **не может проехать**, пока на его пути кирпичи.

### Вода

![water](./pic/water.png 'Вода')

Пуля **пролетает над водой**.
Танк **не может проехать**, когда на его пути вода.
**Неразрушаема**.

## Бонусы

В игре имеется 2 вида **бонусов** — предметов, которые случайно появляются на карте.

|              Жизнь              |                Бустер                |
|:-------------------------------:|:------------------------------------:|
| ![life](./pic/life.png 'Жизнь') | ![buster](./pic/buster.png 'Бустер') |

### Жизнь
Бонус **добавляет** игроку одну жизнь и 100 очков. Максимальное **количество** жизней, которые игрок может иметь в запасе: **3**.

### Бустер
Бонус **умножает** очки, полученные за уничтожение противника или подбор бонуса. За бустер **начисляется** 100 очков. После взятия, бустер используется **3** раза.

# Игровой интерфейс

## Стартовое окно
![screen-01](./pic/screen-01.png 'Стартовое окно')

## Игровое поле
![screen-02](./pic/screen-02.png 'Игровое поле')

## Game Over
![screen-03](./pic/screen-03.png 'Game Over')
