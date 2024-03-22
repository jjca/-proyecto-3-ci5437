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
$(\forall e_i,e_j \in E | e_i \neq e_j : (\exists d \in D, h \in H | x(e_i,e_j,d,h)))$ 

- Dos juegos no pueden ocurrir al mismo tiempo. $(\forall x_1(e_i1,e_j1,d_1,h_1), x_2(e_i2,e_j2,d_2,h_2) | : h_1 != h_2 \land d_1 = d_2)$
- Un participante puede jugar a lo sumo una vez por día. $(\forall e \in E| \sum_{i=1,j=1}^{n,m} x(e_i,e_k,d_j,h) <= 1)$
* Un participante no puede jugar de "visitante" en dos días consecutivos, ni de "local" dos días seguidos.
* Todos los juegos deben empezar en horas "en punto" (por ejemplo, las 13:00:00 es una hora válida pero las 13:30:00 no).
* Todos los juegos deben ocurrir entre una fecha inicial y una fecha final especificadas. Pueden ocurrir juegos en dichas fechas.
* Todos los juegos deben ocurrir entre un rango de horas especificado, el cuál será fijo para todos los días del torneo.
* A efectos prácticos, todos los juegos tienen una duración de dos horas.


# Referencias

Béjar, R. y Manyà, F.: Solving the Round Robin Problem Using Propositional Logic. https://cdn.aaai.org/AAAI/2000/AAAI00-040.pdf. 2000.
Lynce, I. y Ouaknine, J.: Sudoku as a SAT Problem. https://sat.inesc-id.pt/~ines/publications/aimath06.pdf