# tp1-SIA

Para correr el motor de busqueda se debe correr

``python3 src/simulation.py``

El config.json del directorio contiene los siguientes pares clave, valor:


- level: Path al archivo con representacion ASCII del nivel.
- algorithm:[ "bfs" | "dfs" | "a*" | "greedy" ]
- limit: Numero entero (Obligatorio solo para DFS)