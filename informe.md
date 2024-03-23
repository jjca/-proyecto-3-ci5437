# Informe - Proyecto 3
Elaborado por:
- Yerimar Manzo 14-10611
- Jorge Correia 14-10254

## Representación del problema en CNF

El problema a resolver es una variante del problema de Round Robin para SAT, el cual, consiste en ubicar un horario válido para los juegos con el conjunto de restricciones dado.

De acuerdo a Lynce y Ouaknine, un problema SAT se representa con $n$ variables proposicionales, las cuales pueden tener valores $0$ (false) o $1$ (true). Una fórmula $\varphi$ SAT tiene:
- Un literal $l$ el cual es una variable $x_i$ (positiva) o su complemento, $x_j$ (negativa). 
- Una cláusula $\omega$ es una disyunción de literales

Una fórmula $\varphi$ en CNF es una conjunción de cláusulas $\omega$. Se quiere que la fórmula $\varphi$ sea satisfecha, para ello cada  una de las cláusulas de la fórmula debe satisfecha, es decir, valuar a true. Para que una cláusula $\omega$ con literal $l$, sea sastifecha, se necesita que algún $l_j$ en $\omega$ sea verdadero.

Para representar este problema en CNF, primero es necesario definir las variables, los dominios de dichas variables, así como las restricciones. 

### Variables

Para representar las variables, se tomaron las ideas usadas en el paper de Béjar y Manyà. De esta forma, una variable se define como una terna $x(e_i,e_j,d,h)$, donde:
- $e_i$ es el ID del equipo que jugará local
- $e_j$ es el ID del equipo que jugará como visitante
- $d$ es el ID del día del juego
- $h$ es el ID de la hora del juego

Para esta variable, cuando su valor es $1$ (True), significa que el equipo $e_i$ jugará como local contra el equipo $e_j$, en el día $d$ a la hora $h$.

Dominios:

- El dominio para los equipos $E$: son los números naturales desde el 1 hasta $k$, donde $k$ es la cantidad de equipos a jugar.
- El dominio para los días $D$ son los números naturales desde el 1 hasta $j$, donde $j$ es el número de días a jugar. 
- El dominio para las horas $H$ son igualmente los números naturales desde 1 hasta $m$, donde $m$ es el número de horas diarias para jugar.

Así, una variable se define como $x(e_i,e_j,d,h)$, donde $e_i,e_j \in E \land e_i \neq e_j$, $d \in D$ y $h \in H$.

### Restricciones

- Todos los participantes deben jugar dos veces con cada uno de los otros participantes, una como "visitantes" y la otra como "locales". Esto significa que, si hay 10 equipos, cada equipo jugará 18 veces.
- Dos juegos no pueden ocurrir al mismo tiempo.
- Un participante puede jugar a lo sumo una vez por día.
- Un participante no puede jugar de "visitante" en dos días consecutivos, ni de "local" dos días seguidos.
- Todos los juegos deben empezar en horas "en punto" (por ejemplo, las 13:00:00 es una hora válida pero las 13:30:00 no).
- Todos los juegos deben ocurrir entre una fecha inicial y una fecha final especificadas. Pueden ocurrir juegos en dichas fechas.
- Todos los juegos deben ocurrir entre un rango de horas especificado, el cuál será fijo para todos los días del torneo.
- A efectos prácticos, todos los juegos tienen una duración de dos horas.

Las restricciones mapeadas fueron las 1, 2, 3, 4. Las otras restricciones se encuentran implícitas en la definición del problema y por cómo se hizo el código. La mayoría de las restricciones contiene dos literales negativos, de forma que sólo uno de ellos sea verdadero.
# Ejecución

Para ejecutar el programa, se debe usar:

```bash
python3 main.py nombre_JSON.json
```

## Casos de prueba

Se crearon varios casos de prueba con 3 a 10 equipos, e intervalos de tiempo entre 1 semana a 1 mes. Los casos de prueba se almacenaron en el directorio `jsons` siguiendo además el formato indicado en el enunciado del problema.

Los casos de prueba se ejecutaron en equipos con el siguiente hardware:

- Windows Subsystem for Linux con Debian 12, Intel Core i7-9750H @ 2.60GHz x 6 core, 3GB de RAM
- Windows Subsystem for Linux con Ubuntu 22.04, Intel Core i5-11400F @ 2.60GHz, 16GB de RAM

### Ejecución de los casos

La ejecución de cada caso implicó:

- Crear los juegos posibles
- Crear el CNF correspondiente `output.cnf`
- Ejecutar el solver SAT Glucose sobre `output.cnf` y registrar su salida en `salida_glucose.txt`.
- Crear el archivo `calendario.ics`.

Se ejecutó cada caso una sola vez y se registró el tiempo de ejecución del mismo, registrándose en la siguiente tabla:

#### Fáciles

| |F1|F2|F3|F4|
|:---:|:---:|:---:|:---:|:---:|
Nº de variables|384|180|1320|4200|4200|
Nº de cláusulas|25740|8256|187100|1006770|1006770|
Tiempo de ejecución|0.036s|0.097s|7.34s|1min 57s|2 min|

Para los casos fáciles, F3 y F4, el archivo de las cláusulas CNF `output.cnf` llegó a pesar 13 MB.

#### Intermedio
| |I1|I2|I3|
|:---:|:---:|:---:|:---:|
Nº de variables|10304|9504|10350|
Nº de cláusulas|3985912|3290184|3576240|
Tiempo de ejecución|19 min 30s|15 min|14 min|

Para los casos I1, I2 e I3, el tamaño del archivo `output.cnf` fue de 53MB, 44MB y 48MB, respectivamente.

#### Conclusión

Debido a la gran cantidad de ciclos anidados que se presentan para generar el archivo CNF, el tiempo de ejecución del programa se ve acotado por la creación de las cláusulas del CNF y luego crear el archivo. Una vez generado, Glucose realiza el cálculo rápidamente y el mapeo inverso es rápido también, por lo que la creación del ics termina segundos después.

El tiempo de ejecución es posible que pueda ser acortado si se procesa de una forma diferente el cálculo del archivo CNF. 

A medida que se aumenta la cantidad de equipos y se tiene más tiempo, el número de casos posible aumenta muchísimo. Lo ideal es que se tenga un escenario ajustado, para obtener buenos resultados. Por el contrario, mientras menos días se tenga que calcular y menos equipos se tenga, más rápido será la creación del CNF.

El número aproximado de casos posibles viene dado por: cantidad_de_equipos $\times$ cantidad_de_equipos-1 $\times$ cantidad_días $\times$ cantidad_horas_disponibles

Luego, cada ciclo debe ejecutarse al menos en tiempo $\Omega$(cantidad_de_equipos $\times$ cantidad_de_equipos-1 $\times$ cantidad_días $\times$ cantidad_horas_disponibles).

El uso de memoria viene dado por la cantidad de cláusulas, y el archivo de `output.cnf`.

# Referencias

Béjar, R. y Manyà, F.: Solving the Round Robin Problem Using Propositional Logic. https://cdn.aaai.org/AAAI/2000/AAAI00-040.pdf. 2000.
Lynce, I. y Ouaknine, J.: Sudoku as a SAT Problem. https://sat.inesc-id.pt/~ines/publications/aimath06.pdf