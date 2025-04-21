# Instrucciones para ejecutar


Para ejecutar el juego es necesario tener la dependencia pygame:  
`pip install pygame`

Comando de ejecución del juego:  
`python juego_ajedrez_dado.py`


# Reglas del juego

Este juego es una versión modificada del ajedrez tradicional, diseñada para introducir un elemento de aleatoriedad y dinamismo usando un dado virtual. A continuación se explican las reglas e instrucciones para jugar:

## Objetivo del Juego
Capturar al rey enemigo. El primer jugador que logre capturar al rey del oponente gana la partida.

---

## Reglas Generales

1. Antes de mover una pieza (excepto el rey), el jugador debe lanzar el dado haciendo clic en el botón “Lanzar”.

2. El resultado del dado determinará el tipo de movimiento que las piezas pueden hacer durante ese turno. Las caras del dado representan los siguientes movimientos:
   - Peón (2 caras)
   - Torre (1 cara)
   - Alfil (1 cara)
   - Caballo (1 cara)
   - Reina (1 cara)

3. Una vez lanzado el dado, el jugador puede seleccionar cualquier soldado (pieza no rey) para moverlo según el tipo de movimiento obtenido.  
   Ejemplo: Si el dado da como resultado “Caballo”, el jugador puede mover uno de sus soldados como si fuera un caballo.

4. El rey puede moverse en cualquier momento y no depende del dado. Su movimiento es igual al del ajedrez tradicional (una casilla en cualquier dirección).

5. Para mover una pieza, haz clic sobre ella y luego sobre la casilla destino. Las casillas válidas se resaltarán:
   - Amarillo: movimiento válido.
   - Rojo: pieza enemiga que puede ser capturada.

6. Capturar al rey enemigo termina inmediatamente el juego.

7. Puedes reiniciar el juego en cualquier momento haciendo clic en el botón “Reiniciar”.

---

## Información Adicional

- Las piezas iniciales son todas soldados, excepto el rey.
- No hay jaque ni jaque mate; la partida termina con la captura directa del rey.
- Las reglas estándar del ajedrez como enroque, promoción o jaque no aplican en este mod.
