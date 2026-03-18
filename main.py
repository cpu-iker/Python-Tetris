from tetris.game import Game


# Función que inicia el juego
def main():
    game = Game() # Crea una instancia/objeto de la clase Game
    game.run() # Ejecuta el juego llamando al método run de la clase


# Este bloque asegura que el archivo se ejecute solo si es el principal
if __name__ == "__main__":
    main()
