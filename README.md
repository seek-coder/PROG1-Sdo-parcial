# SEGUNDO PARCIAL LABORATORIO 1 - BRAIAN CATRIEL GATTO
![image](https://github.com/seek-coder/PROG1-Sdo-parcial/assets/130781541/67f92319-3cbb-48fa-b369-9090df565f7e)

## I. FUNDAMENTACIÓN: 
El presente proyecto integra los contenidos vistos en las materias de _Programación I_ y _Laboratorio I_ de **Tecnicatura en Programación** de la **UTN**. Al parcial anterior, se añade el concepto de **CLASES** y el uso de *Base de datos SQLITE*:

1) **Sintaxis**: código bien organizado y eficiente.
2) **Variables y tipos de datos**: como enteros, cadenas, listas, tuplas, diccionarios, conjuntos, etc.
3) **Estructuras de control**: incluye condicionales (if, else, elif) y bucles (for, while) para controlar el flujo de un programa.
4) **Funciones**: que permiten organizar y reutilizar el código. Esto significa aplicar definiciones y llamadas.
4) **Objetos y clases**: ya que Python es un lenguaje de programación orientado a objetos.
5) **Uso de bibliotecas**: que pueden simplificar muchas tareas.
6) **Manejo de excepciones**: que sirven para lograr manejar errores y excepciones.
7) **Entrada y salida de dato**s: eso es,  leer y escribir archivos, interactuar con el sistema y procesar la entrada del usuario.
8) **Módulos y paquetes**: para organizar y reutilizar el código a través de módulos y paquetes.
9) **Pruebas y depuración**: para escribir código confiable.
10) **Seguridad**: aplicar mejores prácticas de seguridad para evitar vulnerabilidades.
11) **Comunidades y recursos**: es decir, conectar con la comunidad de Python, explorar documentación y recursos en línea.
12) **Uso de PYGAME**: como una biblioteca de código abierto en Python que se utiliza para desarrollar juegos y aplicaciones multimedia.
13) **Uso de CLASES**: una plantilla para la creación de objetos. Define un conjunto de atributos y métodos comunes a todos los objetos que se crean a partir de ella. Los objetos son instancias de una clase y heredan las características definidas en la clase.
14) **SQLite**: uso de base de datos para guardar rankings
    
## II. DESCRIPCIÓN GENERAL DEL PROYECTO:
Se trata este de un videojuego tipo arcade que cumple con las siguientes condiciones:
Objetos del juego:

1) Jugador: Controlado por el usuario, acumula puntos destruyendo enemigos y recolectando objetos especiales. Puede moverse, saltar y disparar proyectiles.
2) Enemigos: Antagonistas que se mueven aleatoriamente, dañan al jugador y pueden ser destruidos por proyectiles.
3) Boss: Jefe final del juego con una lógica de ataque única.
4) Terreno y Plataformas: Elementos estáticos que definen zonas transitables.
5) Proyectil: Disparado por el jugador y enemigos para atacar. Se destruye al alcanzar un objetivo o los límites de la escena.
6) Vidas: El jugador inicia con tres vidas y las pierde por colisiones. Puede recuperar salud mediante objetos especiales.
7) Puntuación: Se incrementa por destrucción de enemigos y recolección de objetos. Al final del nivel, se multiplica el tiempo restante por 100 y se suma al puntaje.
8) Cronómetro: Controla el tiempo disponible para cada nivel. El juego termina cuando llega a cero.
9) Ítems y Items Especiales: Objetos recolectables que otorgan beneficios al jugador.
10) Trampas: Obstáculos que restan vidas al jugador al entrar en contacto.
11) Generador de enemigos: Suelta aleatoriamente enemigos desde la parte superior de la pantalla.
12) Niveles: Agrupa elementos del juego, soportados por un archivo JSON para guardar/recuperar partidas.
13) Reglas de Movimiento:

El jugador se mueve horizontalmente y salta, limitado por la condición de contacto con el suelo o plataformas.
Los enemigos tienen movimientos autónomos y cambian de dirección al alcanzar límites horizontales.
Audio:

14) Efectos de sonido acompañan acciones del jugador y enemigo.
15) Música ambiental durante el gameplay.
16) Pantallas del juego:

Selección de nivel: Visualiza tres niveles, accede al siguiente si el anterior es superado con al menos una estrella.
Configuraciones: Prender o apagar música o sonido
Pausa: Posibilidad de pausar el juego con una pantalla representativa.

17) Pantalla de ranking:

Puntuación almacenada en base de datos de SQLite

## III. CONSIDERACIONES FINALES
El videojuego es de mi autoría, pero la aplicación de conceptos se da en base a las clases de las materias anteriormente mencionadas gracias a los profesores de las materias de Programación I y Laboratorio I. Tanto el código, como los sprites (hechos con [Aseprite](https://www.aseprite.org/)) y los sonidos del juego (hechos con [FL Studio](https://www.image-line.com/)) son de producción propia. 
El proyecto me tomó alrededor de cuarenta y ocho horas de trabajo comprendidos en un periódo de casi dos semanas.

Se requiere de la instalación de [pygame](https://www.pygame.org/news) para probar el código.

[Video del juego](https://youtu.be/eKbwOfpsbYk)
