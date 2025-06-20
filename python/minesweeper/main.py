import random


def game():
    gridX = int(input("Digite a quantidade de quadrados na horizontal: "))
    gridY = int(input("Digite a quantidade de quadrados na vertical: "))
    bombs = int(input("Digite a quantidade de bombas: "))
    if bombs >= (gridX * gridY):
        print("O número de minas é maior ou igual ao número de quadrados na grade")
        return

    def create_grid():
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
        print("   " + " ".join(f"[{i}]" for i in range(len(grid[0]))))
        for idx, row in enumerate(grid):
            print(f"{idx:2} " + " ".join(str(cell) for cell in row))

    def count_bombs_around(grid, x, y):
        count = 0
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < gridX and 0 <= ny < gridY and grid[nx][ny] == '[B]':
                    count += 1
        return count

    def flood_fill(x, y, visited):
        if (x, y) in visited or not (0 <= x < gridX and 0 <= y < gridY):
            return
        visited.add((x, y))
        if real_grid[x][y] == '[B]':
            return
        bombs_around = count_bombs_around(real_grid, x, y)
        visible_grid[x][y] = f"[{bombs_around}]"
        if bombs_around == 0:
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    if dx != 0 or dy != 0:
                        flood_fill(x + dx, y + dy, visited)

    def check_victory():
        for x in range(gridX):
            for y in range(gridY):
                if real_grid[x][y] != '[B]' and visible_grid[x][y] == '[ ]':
                    return False
        return True

    real_grid = create_grid()
    visible_grid = create_grid()
    real_grid = place_bombs(real_grid, bombs)

    print("Grade do jogo:")
    print_grid(visible_grid)
    print("Instruções:")
    print("Digite as coordenadas (x y) para revelar um quadrado.")
    print("Para colocar/remover uma bandeira, digite 'f x y'.")

    while True:
        try:
            input_coordinates = input("Digite as coordenadas (x y): ").split()

            if input_coordinates[0].lower() == 'f' and len(input_coordinates) == 3:
                y, x = int(input_coordinates[1]), int(input_coordinates[2])
                if not (0 <= x < gridX and 0 <= y < gridY):
                    print("Coordenadas fora dos limites. Tente novamente.")
                    continue
                if visible_grid[x][y] == '[ ]':
                    visible_grid[x][y] = '[F]'
                elif visible_grid[x][y] == '[F]':
                    visible_grid[x][y] = '[ ]'
                else:
                    print("Você não pode colocar uma bandeira aqui.")
                print("\nGrade atualizada:")
                print_grid(visible_grid)
                continue

            elif len(input_coordinates) == 2:
                y, x = int(input_coordinates[0]), int(input_coordinates[1])
                if not (0 <= x < gridX and 0 <= y < gridY):
                    print("Coordenadas fora dos limites. Tente novamente.")
                    continue
                if visible_grid[x][y] == '[F]':
                    print("Casa com bandeira. Remova a bandeira antes de revelar.")
                    continue

                if real_grid[x][y] == '[B]':
                    print("Voce atingiu uma bomba! Fim de jogo.")
                    for i in range(gridX):
                        for j in range(gridY):
                            if real_grid[i][j] == '[B]':
                                visible_grid[i][j] = '[B]'
                    print_grid(visible_grid)
                    break
                else:
                    visited = set()
                    flood_fill(x, y, visited)
                    print("\nGrade atualizada:")
                    print_grid(visible_grid)

                    if check_victory():
                        print("Parabéns! Você venceu!")
                        break

            else:
                print("Entrada inválida. Tente novamente.")
                continue
        except (ValueError, IndexError):
            print("Entrada inválida. Tente novamente.")


game()
