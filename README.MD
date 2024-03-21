<h1 align="center">✨ TEST RADIUM ✨</h1>

<p align="center">  
<img src="https://img.shields.io/badge/python-3.12 -blueviolet.svg">

</p>


## ***Навигация***
- [Описание](#описание)
- [Технологии](#Технологии)
- [How to install](#how_to_install)
- [Ответы на вопросы](#questions)

<a name="описание"></a> 
## ***Описание***

Тестовое задание для компании RADIUM

Напишите скрипт, асинхронно, в 3 одновременных задачи, скачивающий содержимое HEAD репозитория https://gitea.radium.group/radium/project-configuration во временную папку.
После выполнения всех асинхронных задач скрипт должен посчитать sha256 хэши от каждого файла.
Код должен проходить без замечаний проверку линтером wemake-python-styleguide. Конфигурация nitpick - https://gitea.radium.group/radium/project-configuration
Обязательно 100% покрытие тестами

<a name="computer_vision_and_machine_learning"></a> 
### Технологии

- [FastApi](https://fastapi.tiangolo.com/)
- [Docker](https://www.docker.com/)

<a name="how_to_install"></a> 
## ***How to install***


- Клонировать репозиторий
- Запустить файл main.py

<a name="questions"></a> 
## ***Ответы на вопросы***

- Как вы реализовали асинхронное выполнение задач в вашем скрипте?
- Какие библиотеки использовались для скачивания содержимого репозитория и для каких целей?
- Какие проблемы асинхронности вы сталкивались при выполнении задания и как их решали?
- Как вы организовали скачивание файлов во временную папку?
- Какие основные требования wemake-python-styleguide вы находите наиболее важными для поддержания качества кода?
- Как вы настраивали свой проект для соответствия конфигурации nitpick, указанной в задании? Были ли трудности при - настройке?
- Какие инструменты использовали для измерения 100% покрытия тестами?
- Какие типы тестов вы написали для проверки функциональности вашего скрипта? (Например, модульные тесты, - интеграционные тесты)
- Как вы тестировали асинхронный код? Использовали ли вы моки (mocks) или стабы (stubs) для тестирования асинхронных - операций?