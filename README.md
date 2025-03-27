# tp1-SIA

Para ejecutar el motor de busqueda se debe correr desde la raiz del directorio:

``python3 src/simulation.py config.json``

El archivo `config.json` del directorio contiene los siguientes pares clave-valor:


- level: Path al archivo con representacion ASCII del nivel.
- algorithm: [ "bfs" | "dfs" | "a*" | "greedy" ]
- limit: Numero entero (Obligatorio solo para DFS)


La representacion ASCII del nivel se da de la siguiente forma:
- Pared='#'
- Caja='$'
- Objetivo='.'
- Caja sobre objetivo='*'
- Espacio en blanco=' '
- Jugador='@'
- Jugador sobre objetivo='+'
