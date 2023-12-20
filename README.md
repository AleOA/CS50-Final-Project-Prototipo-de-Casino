# CS50 Final Project - Prototipo de casino
Un prototipo de casino que realicé para el proyecto final del CS50: Introduction to Computer Science en el año 2020.
# Link para acceder:
https://cs50finalproject.pythonanywhere.com/


![Pagina Principal](https://i.postimg.cc/13PtqKgS/Apostar.png)


# Sobre el proyecto
Es un prototipo de un casino online con sistema de resultados "fair game".

# Tecnologías:
   - Python
   - Flask
   - HTML
   - SQLite
   - JavaScript
   - CSS

![Login](https://i.postimg.cc/xqDwBtr1/Login.png)


# ¿Cómo jugar?
Seleccionar la cantidad que se quiera apostar y haga clic en "apostar". El multiplicador empezará a aumentar y se detendrá en un valor aleatorio. Si se retira la apuesta antes de que se detenga el multiplicador, se recupera la apuesta inical y también gana (el monto de la apuesta * multiplicador). De lo contrario, si no se llega a retirar la apuesta y el multiplicador se detiene, se pierde todo el monto de la apuesta.

![Pre Jugar](https://i.postimg.cc/65CqqPpz/Pre-Jugar.png)

![Juego Terminado](https://i.postimg.cc/dQbDqFwL/Juego-Terminado.png)

# ¿Por qué el juego es justo?
Para crear el casino, se creó una lista de 10000 hashes "sha256", que representa a cada juego. Cada hash es la cadena en minúsculas con hash del hash anterior. El último hash de la lista representa el primer juego jugado en el casino y el primer hash de la lista representa el último juego.
Para calcular cada multiplicador de juego, se utilizó la siguiente ecuación:

**h** = int(sha_signature[0:13], 16) ---> para obtener la variable "h", se convirtieron los primeros 13 caracteres del hash a hexadecimal.

**e** = math.pow(2, 52) ---> la variable "e" es el número 2^52.

**multiplicador = ((100 * e - h) / (e - h)) / 100 ---> Para calcular el multiplicador.**

**Si el hash comienza en 0, en lugar de usar la ecuación, el juego terminará en "0.00".**

Por eso se dice que es un "fair game", no se puede controlar el resultado de ningún juego, porque ya están definidos y pueden verificarse a través de esas ecuaciones.

![Preguntas](https://i.postimg.cc/BZLX9bWr/Secci-n-Preguntas.png)

![Ranking](https://i.postimg.cc/prFN036S/Ranking.png)
