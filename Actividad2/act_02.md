# Actividad 2

Peso - 30% del PortFolio

- Primera Convocatoria 03/06/2022
- Segunda Convocatoria 08/07/2022

Desarrollar el algoritmo de A Star. En clase se ha explicado el funcionamiento del algoritmo A* para encontrar el camino más corto entre dos puntos. En la carpeta *act_02* hay un fichero *a_star.py* que contiene código fuente de apoyo y un maze.bmp que contiene el diseño de un laberinto de prueba.

En el código adjunto se incluye el prototipo de una función *calc_path*, que debe implementar el algoritmo A*. Este algoritmo debe usar la clase *Node* (para cada nodo que se recorre) definida en el mismo fichero como apoyo, y al final del algoritmo estos nodos tendrán cada uno el padre desde el que fueron alcanzados. De esta manera, la función ya implementada *return_path* será capaz de determinar el camino, una vez se cumpla la condición de salida (haber llegado al final). También se proveen tres funciones para distintas heurísticas, se puede usar libremente cualquiera de ellas.

Se provee también de toda la infraestructura para cargar el fichero del laberinto, y construirlo como una lista bidimensional (que se deberá usar para conocer el entorno, por filas, columnas), donde el primer nivel son las filas y luego las columnas. En cada punto del laberinto se tiene un 0 si esa baldosa es transitable, o un 1 si es una pared. Al clickar sobre el mapa una vez, se determina el punto de salida, y otro click determina el punto de finalización, y en ese momento se llama a la función para calcular el camino más corto.

Se deben adjuntar todos los ficheros que formen parte de la solución.