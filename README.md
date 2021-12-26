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
├── tank-duel.py       # main-файл
```

Для успешного запуска и нормальной работы в операционной системе должны быть установлены следующие **компоненты**:

+ язык **Python 3.9.8**
+ библиотека **pygame 2.1.1**

# Функциональные возможности
Два игрока управляют своими двумя танками. Их задача -- **побеждать друг друга и собирать очки, тем самым накапливать очки**. Конечная цель -- **набрать определённое количество очков (режим "Аркада") ИЛИ уничтожить игрока-противника (режим "Одна жизнь")**.