# CS50 Final Project - Prototipo de casino
Un prototipo de casino que realicé para el proyecto final del CS50: Introduction to Computer Science.
# Link para acceder:
https://cs50finalproject.pythonanywhere.com/

# Sobre el proyecto
Es un prototipo de un casino online con sistema de resultados "fair game".

# Tecnologías:
   - Python
   - Flask
   - HTML
   - SQLite
   - JavaScript
   - CSS

# ¿Cómo jugar?
Seleccionar la cantidad que se quiera apostar y haga clic en "apostar". El multiplicador empezará a aumentar y se detendrá en un valor aleatorio. Si se retira la apuesta antes de que se detenga el multiplicador, se recupera la apuesta inical y también gana (el monto de la apuesta * multiplicador). De lo contrario, si no se llega a retirar la apuesta y el multiplicador se detiene, se pierde todo el monto de la apuesta.

# ¿Por qué el juego es justo?
Para crear el casino, se creó una lista de 10000 hashes "sha256", que representa a cada juego. Cada hash es la cadena en minúsculas con hash del hash anterior. El último hash de la lista representa el primer juego jugado en el casino y el primer hash de la lista representa el último juego.
Para calcular cada multiplicador de juego, se utilizó la siguiente ecuación:

**h** = int(sha_signature[0:13], 16) ---> para obtener la variable "h", se convirtieron los primeros 13 caracteres del hash a hexadecimal.

**e** = math.pow(2, 52) ---> la variable "e" es el número 2^52.

**multiplicador = ((100 * e - h) / (e - h)) / 100 ---> Para calcular el multiplicador.**

**Si el hash comienza en 0, en lugar de usar la ecuación, el juego terminará en "0.00".**

Por eso se dice que es un "fair game", no puede controlar el resultado de ningún juego, porque ya están definidos y pueden verificarse a través de esas ecuaciones.
