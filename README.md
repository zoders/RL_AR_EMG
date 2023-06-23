# Обучение с подкреплением + ЭМГ + AR
## Описание
**Использование обучения с подкреплением (англ. Reinforcement Learning — RL) для распознавания сигналов ЭМГ и управления AR-средой.**

## Структура проекта 
- EmgPlatform — esp-idf и прошивка для устройства захвата ЭМГ (прошивка работает с этой версией esp-idf, но не с последней)
- TestSceneView — приложение для Android с AR, созданное с помощью библиотеки [SceneView](https://github.com/SceneView/sceneview-android)
- RLearningOnline — реализация RL. client.py — клиент в котором RL-агент взаимодействует со средой; клиент подключается к ЭМГ-устройству и AR-устройству. play.py — симуляция движений заранее собранными жестами в папке moves ("0" — сжимание кулака, "1" — сгибание запястья) для взаимодействия RL-агента и среды.

## ЭМГ-устройство
Разработчик платформы: [Мельников Алексей Олегович](http://rf-lab.org/), к.т.н., доцент РТУ МИРЭА. melnikov.aleksey@gmail.com
<p align="center">
<img src="/media/device_esp32.png" />
</p>

## Скриншоты AR-приложения
<p align="center">
<img src="/media/screen1.jpeg" width="32%"/>
<img src="/media/screen2.png" width="32%"/>
</p>

## Схема обучения с подкреплением
<p align="center">
<img src="/media/rl.png" />
</p>

## Схема программно-аппаратного комплекса
<p align="center">
<img src="/media/schema.png" />
</p>

## Видео с примером работы
https://github.com/zoders/RL_AR_EMG/blob/main/media/demonstration.mp4


