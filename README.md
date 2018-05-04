# Pokemon-Python
Este es un programa escrito en Python para simular una batalla Pokémon doble. Por ahora es capaz de crear una batalla jugable contra enemigos cuyas acciones son aleatorias. Por otro lado, las acciones del aliado pueden ser aleatorias, o ser controladas por una inteligencia artificial.

La inteligencia artificial utiliza técnicas de aprendizaje por refuerzo y redes neuronales profundas.

![Demo](/Demo/2vs2battle_v3.png)

## Tabla de contenido
  * [Librerías](#librerías)
  * [Introducción](#introduccion)
  * [Instalación](#instalacion)
  * [Ejecución](#ejecucion)

## Librerías
Actualmente se están usando las siguientes librerías:
  * pygame: https://github.com/pygame/pygame
  * keras: https://github.com/keras-team/keras

## Introducción
Este proyecto está dedicado a crear una IA que sea capaz de aprender de un humano y que desarrolle estrategias cooperativas con él.

## Instalación
El código incluye un fichero para poder instalar las librerías necesarias para poder ejecutar el programa. Dentro del directorio raíz se debe ejecutar la siguiente instrucción:
```
pip install -r requirements.txt
```
o bien si se desea instalar el paquete:
```
python setup.py install
```

## Ejecución
Para ejecutar el programa se puede llamar a la siguiente instrucción para obtener más detalles del funcionamiento de este:
```
python run.py -h
```
