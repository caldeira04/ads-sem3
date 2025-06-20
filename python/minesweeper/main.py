import random


def game():
    gridX = int(input("Digite a quantidade de quadrados na horizontal: "))
    gridY = int(input("Digite a quantidade de quadrados na vertical: "))
    bombs = int(input("Digite a quantidade de bombas: "))
    if bombs >= (gridX * gridY):
        print("O número de minas é maior ou igual o número de quadrados na grade")
        return

    def grid():
        return [["[ ]" for _ in range(gridY)] for _ in range(gridX)]

    def place_bombs(grid, bombs):
        count = 0
        while count < bombs:
            x = random.randint(0, gridX - 1)
            y = random.randint(0, gridY - 1)
            if grid[x][y] != '[B]':
                grid[x][y] = '[B]'
                count += 1
        return grid

    def print_grid(grid):
        print("  " + " ".join(f"[{i:2}]" for i in range(len(grid[0]))))
        for idx, row in enumerate(grid):
            print(f"{idx:2} "+" ".join(str(cell) for cell in row))
    grid = grid()
    grid = place_bombs(grid, bombs)

    print("\nGrade do jogo:")
    print_grid(grid)
    print("\nInstruções: Digite as coordenadas no formato 'x y' para revelar um quadrado.")
    while True:
        try:
            x, y = map(int, input("Digite as coordenadas (x y): ").split())
            if grid[x][y] == '[B]':
                print("Você atingiu uma bomba! Fim de jogo.")
                break
            else:
                print("\nGrade atualizada:")
                print_grid(grid)
        except (ValueError, IndexError):
            print("Coordenadas inválidas. Tente novamente.")


game()
