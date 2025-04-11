no# Estrategia y otros detalles del agente

La idea fundamental del funcionamiento del agente es calcular la mejor jugada posible para su turno en el juego, dado el estado del tablero.

Como punto de partida se tomó la búsqueda de dicha jugada en árbol de decisiones que generan los posibles movimientos. Para ello inicialmente se consideró el algoritmo _Minimax_ con la optimización de *$\alpha \beta$-prune* o _Poda alfa-beta_.

Dada la imposibilidad computacional que representa explorar el árbol de decisiones en su totalidad, se ha tomado un enfoque eurístico para atacar el problema: se determina que a una cierta profundidad se evalua el estado resultante de aplicar una serie de jugadas $s$ con una funcion $h(s)$ que califica cuan favorable (o desfavorable) es el estado del tablero.

A partir de este momento el mayor desafío reside en encontrar la eurística que mejor juegue, que más haga ganar al agente. 

- Inicialmente se implementó `max_island_size_heuristic` que intenta maximizar el tamaño de la isla más grande del jugador y minimizar la isla más grande del agente, entendiéndose por isla un grupo conectado (o conexo, para hacer uso de términos más rimbombantes) de fichas de un mismo jugador. 
- También se implementó `big_island_size_heuristic` que intenta maximizar el tamaño total de las islas no triviales (de más de una ficha) del jugador y minimizar el mismo criterio para el oponente. Ambas fueron implementadas haciendo uso de disjoint sets para poder ser computadas eficientemente.

- Posteriormente se pensó en `moves_needed_heuristic`, una heurística más popular, cuyo objetivo es minimizar la cantidad de movimientos necesarios para ganar y maximizar los movimientos del oponente. Para que el agente tuviera una estrategía ligeramente más agresiva y ambiciosa se le dió un mayor peso al valor de la eurística para el jugador. Dicha funcion usa un BFS con una deque para cada jugador, ya que el problema se modeló como un grafo donde los vertices tienen solo valores $w \in \{0, 1, + \infty \}$

- Finalmente se implementó `bridges_heuristic`, una heurística que favorece jugadas que generen la creación de puentes (y la no generacion de puentes del oponente). Un puente o conexión virtual, son un par de fichas no conectadas, que pueden ser unidas en un turno cualquiera sea la jugada del oponente. Dicho de otra forma, un par de fichas que tienen dos caminos disjuntos de una ficha de longitud.

Teniendo esas cuatro funciones para evaluar un estado, se halló una funcion de evaluación general, dada por la combinación lineal de las mismas con unos coeficientes de ponderación.

Luego de un largo proceso de prueba y error las dos primeras heurísticas llegaron a tener un peso tan bajo que fueron descartadas para ahorrar computo, y se decidió darle un poco más de peso a `moves_needed_heuristic`, ya que de esa forma, el jugador se mantiene a la ofensiva sin sacrificar la estrategia, de lo contrario intenta llenar el tablero de puentes dejando de un lado la victoria xD.

Finalmente, una parámetro que fue clave en la velocidad y eficacia del agente. Es efectuar el `Minimax` a profundidad $1$ (pudiera uno preguntarse si este cambio revoca su condición de `Minimax` y lo convierte en simplemente un `Max`, pero este .md no es el de un proyecto de filosofía). Esto hace que el jugador se comporte muy agresivo y menos planificador, lo cual vence a otros jugadores que usan una profundidad más alta. Para tener una idea de como esto ultimo cambia el desempeño del agente, de 50 partidas simuladas, entre el versiones del jugador que usaban profundidad 1 y 2 respectivamente, el jugador cuya profundidad 1 ganó el 100% de las veces.
