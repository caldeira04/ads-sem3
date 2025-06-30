import flet as ft
import requests
import json

API_URL = "http://localhost:3000/products"

def add_product_page(page: ft.Page):
    name_field = ft.TextField(
        label="Nome do Produto",
        hint_text="Ex: iPhone 14",
        border=ft.InputBorder.OUTLINE,
        width=400,
        prefix_icon=ft.Icons.SHOPPING_BAG
    )
    
    brand_field = ft.TextField(
        label="Marca",
        hint_text="Ex: Apple",
        border=ft.InputBorder.OUTLINE,
        width=400,
        prefix_icon=ft.Icons.BUSINESS
    )
    
    category_field = ft.Dropdown(
        label="Categoria",
        hint_text="Selecione uma categoria",
        border=ft.InputBorder.OUTLINE,
        width=400,
        options=[
            ft.dropdown.Option("Smartphone"),
            ft.dropdown.Option("Headphones"),
            ft.dropdown.Option("Tablet"),
            ft.dropdown.Option("Laptop"),
            ft.dropdown.Option("Smartwatch"),
            ft.dropdown.Option("Acessórios"),
            ft.dropdown.Option("Outros")
        ]
    )
    
    price_field = ft.TextField(
        label="Preço (R$)",
        hint_text="Ex: 999.99",
        border=ft.InputBorder.OUTLINE,
        width=400,
        prefix_icon=ft.Icons.ATTACH_MONEY,
        keyboard_type=ft.KeyboardType.NUMBER
    )
    
    status_text = ft.Text(
        "",
        size=14,
        weight=ft.FontWeight.BOLD
    )
    
    def get_next_id():
        try:
            response = requests.get(API_URL)
            if response.status_code == 200:
                products = response.json()
                if products:
                    return max(product["id"] for product in products) + 1
                else:
                    return 1
            else:
                return 1
        except Exception:
            return 1
    
    def validate_fields():
        errors = []
        
        if not name_field.value or name_field.value.strip() == "":
            errors.append("Nome do produto é obrigatório")
        
        if not brand_field.value or brand_field.value.strip() == "":
            errors.append("Marca é obrigatória")
        
        if not category_field.value:
            errors.append("Categoria é obrigatória")
        
        if not price_field.value or price_field.value.strip() == "":
            errors.append("Preço é obrigatório")
        else:
            try:
                price = float(price_field.value.replace(",", "."))
                if price <= 0:
                    errors.append("Preço deve ser maior que zero")
            except ValueError:
                errors.append("Preço deve ser um número válido")
        
        return errors
    
    def clear_fields():
        name_field.value = ""
        brand_field.value = ""
        category_field.value = None
        price_field.value = ""
        status_text.value = ""
        page.update()
    
    def show_snackbar(message, color=ft.Colors.GREEN):
        page.snack_bar.content.value = message
        page.snack_bar.bgcolor = color
        page.snack_bar.open = True
        page.update()
    
    def add_product(e):
        errors = validate_fields()
        if errors:
            status_text.value = "Erros encontrados:\n• " + "\n• ".join(errors)
            status_text.color = ft.Colors.RED
            page.update()
            return
        
        try:
            price = float(price_field.value.replace(",", "."))
            
            new_product = {
                "id": get_next_id(),
                "name": name_field.value.strip(),
                "brand": brand_field.value.strip(),
                "category": category_field.value,
                "price": int(price * 100)
            }
            
            response = requests.post(
                API_URL,
                headers={"Content-Type": "application/json"},
                data=json.dumps(new_product)
            )
            
            if response.status_code == 201:
                status_text.value = f"Produto '{new_product['name']}' adicionado com sucesso!"
                status_text.color = ft.Colors.GREEN
                show_snackbar(f"Produto '{new_product['name']}' adicionado com sucesso!")
                clear_fields()
            else:
                status_text.value = f"Erro ao adicionar produto. Código: {response.status_code}"
                status_text.color = ft.Colors.RED
                
        except Exception as ex:
            status_text.value = f"Erro inesperado: {str(ex)}"
            status_text.color = ft.Colors.RED
        
        page.update()
    
    add_button = ft.ElevatedButton(
        text="Adicionar Produto",
        icon=ft.Icons.ADD,
        on_click=add_product,
        style=ft.ButtonStyle(
            color=ft.Colors.WHITE,
            bgcolor=ft.Colors.BLUE,
            padding=ft.padding.symmetric(horizontal=20, vertical=10)
        )
    )
    
    clear_button = ft.OutlinedButton(
        text="Limpar Campos",
        icon=ft.Icons.CLEAR,
        on_click=lambda e: clear_fields(),
        style=ft.ButtonStyle(
            color=ft.Colors.BLUE,
            padding=ft.padding.symmetric(horizontal=20, vertical=10)
        )
    )
    
    products_table_container = ft.Container(
        content=ft.Text("Carregando produtos...", text_align=ft.TextAlign.CENTER),
        width=780,
        height=350,  
        border=ft.border.all(1, ft.Colors.OUTLINE),
        border_radius=8,
        padding=10
    )
    
    main_container = ft.Container(
        content=ft.Column(
            [
                ft.Text(
                    "Adicionar Novo Produto",
                    size=28,
                    weight=ft.FontWeight.BOLD,
                    color=ft.Colors.BLUE
                ),
                ft.Divider(),
                ft.Container(height=10),
                ft.Card(
                    content=ft.Container(
                        content=ft.Column(
                            [
                                name_field,
                                ft.Container(height=10),
                                brand_field,
                                ft.Container(height=10),
                                category_field,
                                ft.Container(height=10),
                                price_field,
                                ft.Container(height=20),

                                ft.Row(
                                    [add_button, clear_button],
                                    alignment=ft.MainAxisAlignment.CENTER,
                                    spacing=20
                                ),
                                
                                ft.Container(height=10),
                                status_text
                            ],
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            spacing=0
                        ),
                        padding=30
                    ),
                    elevation=5
                ),
                
                ft.Container(height=20),
                
                ft.Card(
                    content=ft.Container(
                        content=ft.Column(
                            [
                                ft.Text(
                                    "📦 Produtos Existentes",
                                    size=20,
                                    weight=ft.FontWeight.BOLD,
                                    color=ft.Colors.BLUE
                                ),
                                ft.Divider(),
                                ft.Container(height=10),
                                
                                ft.Row(
                                    [
                                        ft.ElevatedButton(
                                            text="Atualizar Lista",
                                            icon=ft.Icons.REFRESH,
                                            on_click=lambda e: load_products_table(),
                                            style=ft.ButtonStyle(
                                                color=ft.Colors.WHITE,
                                                bgcolor=ft.Colors.GREEN,
                                                padding=ft.padding.symmetric(horizontal=15, vertical=8)
                                            )
                                        )
                                    ],
                                    alignment=ft.MainAxisAlignment.CENTER
                                ),
                                
                                ft.Container(height=15),
                                products_table_container
                            ],
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER
                        ),
                        padding=20
                    ),
                    elevation=3
                ),
                ft.Container(height=50)
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=10,
            scroll=ft.ScrollMode.ALWAYS,  
            expand=True
        ),
        padding=20,
        expand=True
    )
    
    def format_price(db_price):
        """Formata o preço de centavos para reais"""
        return f"R$ {db_price / 100:.2f}".replace('.', ',')
    
    def load_products_table():
        try:
            response = requests.get(API_URL)
            if response.status_code == 200:
                products = response.json()
                if not products:
                    products_table_container.content = ft.Container(
                        content=ft.Column(
                            [
                                ft.Icon(ft.Icons.INVENTORY_2, size=64, color=ft.Colors.GREY),
                                ft.Text(
                                    "Nenhum produto encontrado",
                                    size=16,
                                    color=ft.Colors.GREY,
                                    text_align=ft.TextAlign.CENTER
                                ),
                                ft.Text(
                                    "Adicione seu primeiro produto usando o formulário acima",
                                    size=12,
                                    color=ft.Colors.GREY,
                                    text_align=ft.TextAlign.CENTER
                                )
                            ],
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            spacing=10
                        ),
                        alignment=ft.alignment.center,
                        expand=True
                    )
                else:
                    products.sort(key=lambda x: x.get("id", 0))
                    header = ft.Row(
                        [
                            ft.Container(
                                content=ft.Text("ID", weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                                bgcolor=ft.Colors.BLUE,
                                padding=ft.padding.all(10),
                                width=60,
                                alignment=ft.alignment.center
                            ),
                            ft.Container(
                                content=ft.Text("Nome", weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                                bgcolor=ft.Colors.BLUE,
                                padding=ft.padding.all(10),
                                width=200,
                                alignment=ft.alignment.center_left
                            ),
                            ft.Container(
                                content=ft.Text("Marca", weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                                bgcolor=ft.Colors.BLUE,
                                padding=ft.padding.all(10),
                                width=150,
                                alignment=ft.alignment.center_left
                            ),
                            ft.Container(
                                content=ft.Text("Categoria", weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                                bgcolor=ft.Colors.BLUE,
                                padding=ft.padding.all(10),
                                width=150,
                                alignment=ft.alignment.center_left
                            ),
                            ft.Container(
                                content=ft.Text("Preço", weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                                bgcolor=ft.Colors.BLUE,
                                padding=ft.padding.all(10),
                                width=120,
                                alignment=ft.alignment.center_right
                            ),
                            ft.Container(
                                content=ft.Text("Ações", weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                                bgcolor=ft.Colors.BLUE,
                                padding=ft.padding.all(10),
                                width=80,
                                alignment=ft.alignment.center
                            )
                        ],
                        spacing=1
                    )

                    rows = []
                    for i, product in enumerate(products):
                        row_color = ft.Colors.WHITE if i % 2 == 0 else ft.Colors.GREY_100
                        row = ft.Row(
                            [
                                ft.Container(
                                    content=ft.Text(str(product.get("id", "N/A")), color=ft.Colors.BLACK),
                                    bgcolor=row_color,
                                    padding=ft.padding.all(10),
                                    width=60,
                                    alignment=ft.alignment.center,
                                ),
                                ft.Container(
                                    content=ft.Text(
                                        product.get("name", "N/A"),
                                        overflow=ft.TextOverflow.ELLIPSIS,
                                        color=ft.Colors.BLACK
                                    ),
                                    bgcolor=row_color,
                                    padding=ft.padding.all(10),
                                    width=200,
                                    alignment=ft.alignment.center_left
                                ),
                                ft.Container(
                                    content=ft.Text(
                                        product.get("brand", "N/A"),
                                        overflow=ft.TextOverflow.ELLIPSIS,
                                        color=ft.Colors.BLACK
                                    ),
                                    bgcolor=row_color,
                                    padding=ft.padding.all(10),
                                    width=150,
                                    alignment=ft.alignment.center_left
                                ),
                                ft.Container(
                                    content=ft.Text(
                                        product.get("category", "N/A"),
                                        overflow=ft.TextOverflow.ELLIPSIS,
                                        color=ft.Colors.BLACK
                                    ),
                                    bgcolor=row_color,
                                    padding=ft.padding.all(10),
                                    width=150,
                                    alignment=ft.alignment.center_left
                                ),
                                ft.Container(
                                    content=ft.Text(
                                        format_price(product.get("price", 0)),
                                        weight=ft.FontWeight.BOLD,
                                        color=ft.Colors.GREEN_700
                                    ),
                                    bgcolor=row_color,
                                    padding=ft.padding.all(10),
                                    width=120,
                                    alignment=ft.alignment.center_right
                                ),
                                ft.Container(
                                    bgcolor=row_color,
                                    width=80,
                                    content=ft.IconButton(
                                        icon=ft.Icons.DELETE,
                                        tooltip="Excluir",
                                        on_click=lambda e, p=product: delete_product(p)
                                    )
                                )
                            ],
                            spacing=1
                        )
                        rows.append(row)
                    
                    products_table_container.content = ft.Column(
                        [
                            header,
                            ft.Container(height=1),
                            ft.Container(
                                content=ft.Column(
                                    rows,
                                    spacing=1,
                                    scroll=ft.ScrollMode.AUTO
                                ),
                                height=250,
                                border=ft.border.all(1, ft.Colors.GREY_300)
                            ),
                            ft.Container(height=10),
                            ft.Text(
                                f"Total de produtos: {len(products)}",
                                size=12,
                                color=ft.Colors.GREY_700,
                                weight=ft.FontWeight.BOLD
                            )
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER
                    )
                
            else:
                products_table_container.content = ft.Container(
                    content=ft.Column(
                        [
                            ft.Icon(ft.Icons.ERROR, size=64, color=ft.Colors.RED),
                            ft.Text(
                                f"Erro ao carregar produtos",
                                size=16,
                                color=ft.Colors.RED,
                                text_align=ft.TextAlign.CENTER
                            ),
                            ft.Text(
                                f"Código do erro: {response.status_code}",
                                size=12,
                                color=ft.Colors.GREY,
                                text_align=ft.TextAlign.CENTER
                            )
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=10
                    ),
                    alignment=ft.alignment.center,
                    expand=True
                )
                            
        except Exception as ex:
            products_table_container.content = ft.Container(
                content=ft.Column(
                    [
                        ft.Text(
                            str(ex),
                            size=12,
                            color=ft.Colors.GREY,
                            text_align=ft.TextAlign.CENTER
                        )
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=10
                ),
                alignment=ft.alignment.center,
                expand=True
            )
        
        page.update()
    
    def add_product(e):
        """Adiciona um novo produto e atualiza a tabela"""
        errors = validate_fields()
        if errors:
            status_text.value = "Erros encontrados:\n• " + "\n• ".join(errors)
            status_text.color = ft.Colors.RED
            page.update()
            return
        
        try:
            price = float(price_field.value.replace(",", "."))
            
            new_product = {
                "id": get_next_id(),
                "name": name_field.value.strip(),
                "brand": brand_field.value.strip(),
                "category": category_field.value,
                "price": int(price * 100)
            }
            
            response = requests.post(
                API_URL,
                headers={"Content-Type": "application/json"},
                data=json.dumps(new_product)
            )
            
            if response.status_code == 201:
                status_text.value = f"Produto '{new_product['name']}' adicionado com sucesso!"
                status_text.color = ft.Colors.GREEN
                show_snackbar(f"Produto '{new_product['name']}' adicionado com sucesso!")
                clear_fields()
                load_products_table()
            else:
                status_text.value = f"Erro ao adicionar produto. Código: {response.status_code}"
                status_text.color = ft.Colors.RED
                
        except requests.exceptions.ConnectionError:
            status_text.value = "Erro: Não foi possível conectar ao servidor. Verifique se o json-server está rodando."
            status_text.color = ft.Colors.RED
        except Exception as ex:
            status_text.value = f"Erro inesperado: {str(ex)}"
            status_text.color = ft.Colors.RED
        

    add_button.on_click = add_product

    def delete_product(e):
        print(f"Excluindo produto: {e['name']} (ID: {e['id']})")
        try:
            response = requests.delete(f"{API_URL}/{e['id']}")
            
            if response.status_code == 200:
                show_snackbar(f"Produto '{e['name']}' excluído com sucesso!")
                load_products_table()
            else:
                show_snackbar(f"Erro ao excluir produto. Código: {response.status_code}", color=ft.Colors.RED)
        
        except Exception as ex:
            show_snackbar(f"Erro inesperado: {str(ex)}", color=ft.Colors.RED)

    # Retornar o container para uso na navegação
    return main_container, load_products_table