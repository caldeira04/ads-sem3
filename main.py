import csv
import locale
locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')

students = []

with open('Students Social Media Addiction.csv', mode="r") as file:
    csv_reader = csv.DictReader(file)
    for row in csv_reader:
        students.append(row)


def title(text):
    print()
    print(text)
    print("=" * 40)


def most_used_platform():
    title("Redes Mais Utilizadas")
    platforms = {}
    for student in students:
        platform = student['Most_Used_Platform']
        platforms[platform] = platforms.get(platform, 0) + 1

    print("As plataformas que reunem mais usuários na pesquisa são: ")
    groups = dict(sorted(platforms.items(),
                  key=lambda item: item[1], reverse=True))

    for num, (platform, count) in enumerate(groups.items(), start=1):
        print(f"{num}. {platform} - {count} usuários")


def compare_countries():
    title("Comparação entre Países: Redes Mais Utilizadas")
    country1 = input("País 1: ")
    country2 = input("País 2: ")

    platforms = {}
    for student in students:
        if student['Country'] == country1 or student['Country'] == country2:
            platform = student['Most_Used_Platform']
            if platform not in platforms:
                platforms[platform] = {country1: 0, country2: 0}
            platforms[platform][student['Country']] += 1

    print(f"Comparação entre {country1} e {country2}:")
    for platform, counts in platforms.items():
        print(f"{platform}: {
              country1} - {counts[country1]}, {country2} - {counts[country2]}")


def average_platform_ages():
    title("Média de Idades por Plataforma")
    platform = input("Plataforma: ")

    ages = []
    for student in students:
        if student['Most_Used_Platform'] == platform:
            try:
                age = int(student['Age'])
                ages.append(age)
            except ValueError:
                continue

    if ages:
        average_age = sum(ages) / len(ages)
        print(f"Média de idade dos usuários do {
              platform}: {average_age:.2f} anos")
    else:
        print(f"Nenhum usuário encontrado para a plataforma {platform}.")


def most_addicted_country():
    title("País com Maior Vício em Redes Sociais")
    countries = {}
    for student in students:
        country = student['Country']
        addiction_level = int(student['Addicted_Score'])
        if country not in countries:
            countries[country] = 0
        countries[country] = countries.get(country, 0) + addiction_level

    print("Top 10 Países com maior vício em redes sociais:")
    most_addicted = dict(sorted(countries.items(),
                                key=lambda item: item[1], reverse=True))
    for num, (country, score) in enumerate(most_addicted.items(), start=1):
        print(f"{num}. {country} - Pontos de Vício: {score}")
        if num == 10:
            break


def most_addicted_level():
    title("Média de vício por grupo acadêmico")
    academic_group = ["Undergraduate", "Graduate", "High School"]
    num1 = sum1 = 0
    print("Grupos acadêmicos disponíveis:")
    for i, group in enumerate(academic_group, start=1):
        print(f"{i}. {group}")
    choice = input("Selecione um grupo acadêmico: ")
    if choice == "1":
        group = academic_group[0]
        num1 = 0
        sum1 = 0
        for student in students:
            if student['Academic_Level'] == group:
                try:
                    addiction_score = int(student['Addicted_Score'])
                    num1 += 1
                    sum1 += addiction_score
                    average_addiction = sum1 / num1
                except ZeroDivisionError:
                    print(
                        "Nenhum usuário encontrado no grupo")
        print(f"Média de vício em redes sociais para {
            group}: {average_addiction:.2f}")
    elif choice == "2":
        group = academic_group[1]
        num1 = 0
        sum1 = 0
        for student in students:
            if student['Academic_Level'] == group:
                try:
                    addiction_score = int(student['Addicted_Score'])
                    num1 += 1
                    sum1 += addiction_score
                    average_addiction = sum1 / num1
                except ZeroDivisionError:
                    print(
                        "Nenhum usuário encontrado no grupo")
        print(f"Média de vício em redes sociais para {
            group}: {average_addiction:.2f}")
    elif choice == "3":
        group = academic_group[2]
        num1 = 0
        sum1 = 0
        for student in students:
            if student['Academic_Level'] == group:
                try:
                    addiction_score = int(student['Addicted_Score'])
                    num1 += 1
                    sum1 += addiction_score
                    average_addiction = sum1 / num1
                except ZeroDivisionError:
                    print(
                        "Nenhum usuário encontrado no grupo")
        print(f"Média de vício em redes sociais para {
            group}: {average_addiction:.2f}")

    else:
        print("Opção inválida.")


def most_used_by_country():
    title("Rede Social Mais Utilizada por País")
    country = input("Digite o nome do país: ")
    platforms = {}
    for student in students:
        if student['Country'] == country:
            platform = student['Most_Used_Platform']
            platforms[platform] = platforms.get(platform, 0) + 1
    if platforms:
        most_used = max(platforms.items(), key=lambda item: item[1])
        print(f"A rede social mais utilizada em {country} é: {
              most_used[0]} com {most_used[1]} usuários.")


def common_items_between_countries():
    title("Itens em Comum entre Países")
    country1 = input("País 1: ")
    country2 = input("País 2: ")

    items_country1 = set()
    items_country2 = set()

    for student in students:
        if student['Country'] == country1:
            items_country1.add(student['Most_Used_Platform'])
        elif student['Country'] == country2:
            items_country2.add(student['Most_Used_Platform'])

    common_items = items_country1.intersection(items_country2)

    if common_items:
        print(f"Itens em comum entre {country1} e {country2}:")
        for item in common_items:
            print(f"- {item}")
    else:
        print(f"Nenhum item em comum encontrado entre {
              country1} e {country2}.")


while True:
    title("Análise de Vício em Redes Sociais")
    print("1. Rede Social Mais Utilizada")
    print("2. Comparar Países")
    print("3. Média de Idades por Plataforma")
    print("4. Top 10 Países com Maior Vício em Redes Sociais")
    print("5. Grupo Acadêmico com Maior Vício em Redes Sociais")
    print("6. Rede Social Mais Utilizada por País")
    print("7. Itens em comum entre os países")
    print("0. Sair")
    try:
        choice = int(input("Escolha uma opção: "))
    except ValueError:
        print("Por favor, insira um número válido.")
        continue

    if choice == 1:
        most_used_platform()
    elif choice == 2:
        compare_countries()
    elif choice == 3:
        average_platform_ages()
    elif choice == 4:
        most_addicted_country()
    elif choice == 5:
        most_addicted_level()
    elif choice == 6:
        most_used_by_country()
    elif choice == 7:
        common_items_between_countries()
    elif choice == 0:
        print("Saindo...")
        break
    else:
        print("Opção inválida. Tente novamente.")
