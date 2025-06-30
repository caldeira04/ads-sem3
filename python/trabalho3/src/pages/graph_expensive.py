import flet as ft
import requests
import json

API_URL = "http://localhost:3000/products"

def graph_expensive_page(page: ft.Page):
    list_container = ft.Container(
        content=ft.Text("Carregando dados...", text_align=ft.TextAlign.CENTER),
        width=800,
        height=400,
        border=ft.border.all(1, ft.Colors.OUTLINE),
        border_radius=8,
        padding=20
    )
    
    def format_price(price_in_cents):
        return f"R$ {price_in_cents / 100:.2f}".replace('.', ',')
    
    def load_expensive_products():
        try:
            response = requests.get(API_URL)
            
            if response.status_code == 200:
                products = response.json()
                
                if not products:
                    list_container.content = ft.Container(
                        content=ft.Column(
                            [
                                ft.Icon(ft.Icons.INVENTORY_2, size=64, color=ft.Colors.GREY),
                                ft.Text(
                                    "Nenhum produto encontrado",
                                    size=16,
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
                    sorted_products = sorted(
                        products, 
                        key=lambda x: x.get("price", 0), 
                        reverse=True
                    )
                    
                    top_products = sorted_products[:10]
                    
                    colors = [
                        ft.Colors.YELLOW,
                        ft.Colors.GREY_400,
                        ft.Colors.ORANGE,
                        ft.Colors.PURPLE,
                        ft.Colors.RED,
                        ft.Colors.TEAL,
                        ft.Colors.PINK,
                        ft.Colors.INDIGO,
                        ft.Colors.LIME,
                        ft.Colors.AMBER
                    ]
                    
                    chart_rows = []
                    max_price = max(product.get("price", 0) for product in top_products) if top_products else 1
                    
                    for i, product in enumerate(top_products):
                        price = product.get("price", 0)
                        bar_width = (price / max_price) * 400
                        color = colors[i % len(colors)]
                        
                        rank_icon = "🥇" if i == 0 else "🥈" if i == 1 else "🥉" if i == 2 else f"#{i+1}"
                        
                        chart_rows.append(
                            ft.Container(
                                content=ft.Row(
                                    [
                                        ft.Container(
                                            content=ft.Text(
                                                rank_icon,
                                                size=16,
                                                weight=ft.FontWeight.BOLD,
                                                color=ft.Colors.BLACK
                                            ),
                                            width=50,
                                            alignment=ft.alignment.center
                                        ),
                                        
                                        ft.Container(
                                            content=ft.Column(
                                                [
                                                    ft.Text(
                                                        product.get("name", "N/A"),
                                                        size=12,
                                                        weight=ft.FontWeight.BOLD,
                                                        color=ft.Colors.BLACK,
                                                        overflow=ft.TextOverflow.ELLIPSIS
                                                    ),
                                                    ft.Text(
                                                        f"{product.get('brand', 'N/A')} • {product.get('category', 'N/A')}",
                                                        size=10,
                                                        color=ft.Colors.GREY_700,
                                                        overflow=ft.TextOverflow.ELLIPSIS
                                                    )
                                                ],
                                                spacing=2
                                            ),
                                            width=150,
                                            alignment=ft.alignment.center_left
                                        ),
                                        
                                        ft.Container(
                                            content=ft.Row(
                                                [
                                                    ft.Container(
                                                        width=bar_width,
                                                        height=30,
                                                        bgcolor=color,
                                                        border_radius=15,
                                                        content=ft.Container(
                                                            content=ft.Text(
                                                                format_price(price),
                                                                size=10,
                                                                weight=ft.FontWeight.BOLD,
                                                                color=ft.Colors.WHITE
                                                            ),
                                                            alignment=ft.alignment.center
                                                        ) if bar_width > 80 else None
                                                    )
                                                ],
                                                spacing=0
                                            ),
                                            width=420,
                                            alignment=ft.alignment.center_left
                                        ),
                                        
                                        ft.Container(
                                            content=ft.Text(
                                                format_price(price),
                                                size=12,
                                                weight=ft.FontWeight.BOLD,
                                                color=ft.Colors.GREEN_700
                                            ),
                                            width=100,
                                            alignment=ft.alignment.center_left
                                        )
                                    ],
                                    spacing=10,
                                    vertical_alignment=ft.CrossAxisAlignment.CENTER
                                ),
                                padding=ft.padding.symmetric(vertical=5, horizontal=10),
                                margin=ft.margin.symmetric(vertical=2),
                                bgcolor=ft.Colors.WHITE,
                                border_radius=8,
                                border=ft.border.all(1, ft.Colors.GREY_200)
                            )
                        )
                    
                    list_container.content = ft.Column(
                        [
                            ft.Text(
                                "💰 Top 10 Produtos Mais Caros",
                                size=18,
                                weight=ft.FontWeight.BOLD,
                                color=ft.Colors.BLUE
                            ),
                            ft.Container(height=15),
                            
                            ft.Container(
                                content=ft.Column(
                                    chart_rows,
                                    spacing=0,
                                    scroll=ft.ScrollMode.AUTO
                                ),
                                height=250,
                                width=720
                            ),
                            
                            ft.Container(height=15),
                            ft.Row(
                                [
                                    ft.Text(
                                        f"Exibindo top {len(top_products)} de {len(products)} produtos",
                                        size=12,
                                        color=ft.Colors.GREY_700,
                                        weight=ft.FontWeight.BOLD
                                    )
                                ],
                                spacing=20,
                                alignment=ft.MainAxisAlignment.CENTER
                            )
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER
                    )
            else:
                list_container.content = ft.Container(
                    content=ft.Column(
                        [
                            ft.Icon(ft.Icons.ERROR, size=64, color=ft.Colors.RED),
                            ft.Text(
                                "Erro ao carregar dados",
                                size=16,
                                color=ft.Colors.RED,
                                text_align=ft.TextAlign.CENTER
                            )
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=10
                    ),
                    alignment=ft.alignment.center,
                    expand=True
                )
                
        except requests.exceptions.ConnectionError:
            list_container.content = ft.Container(
                content=ft.Column(
                    [
                        ft.Icon(ft.Icons.WIFI_OFF, size=64, color=ft.Colors.ORANGE),
                        ft.Text(
                            "Erro de conexão",
                            size=16,
                            color=ft.Colors.ORANGE,
                            text_align=ft.TextAlign.CENTER
                        ),
                        ft.Text(
                            "Verifique se o json-server está rodando",
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
            list_container.content = ft.Container(
                content=ft.Column(
                    [
                        ft.Icon(ft.Icons.BUG_REPORT, size=64, color=ft.Colors.RED),
                        ft.Text(
                            "Erro inesperado",
                            size=16,
                            color=ft.Colors.RED,
                            text_align=ft.TextAlign.CENTER
                        ),
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
    
    main_container = ft.Container(
        content=ft.Column(
            [
                ft.Text(
                    "Produtos Mais Caros",
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
                                ft.Row(
                                    [
                                        ft.ElevatedButton(
                                            text="Atualizar Lista",
                                            icon=ft.Icons.REFRESH,
                                            on_click=lambda e: load_expensive_products(),
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
                                list_container
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
    
    return main_container, load_expensive_products
