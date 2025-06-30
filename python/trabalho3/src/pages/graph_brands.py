import flet as ft
import requests
import json
from collections import Counter

API_URL = "http://localhost:3000/products"

def graph_brands_page(page: ft.Page):
    chart_container = ft.Container(
        content=ft.Text("Carregando dados...", text_align=ft.TextAlign.CENTER),
        width=800,
        height=400,
        border=ft.border.all(1, ft.Colors.OUTLINE),
        border_radius=8,
        padding=20
    )
    
    def load_brands_chart():
        try:
            response = requests.get(API_URL)
            
            if response.status_code == 200:
                products = response.json()
                
                if not products:
                    chart_container.content = ft.Container(
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
                    brands_count = Counter(product.get("brand", "Sem marca") for product in products)
                    sorted_brands = sorted(
                        brands_count.items(), 
                        key=lambda x: (-x[1], x[0])
                    )
                    
                    colors = [
                        ft.Colors.BLUE,
                        ft.Colors.GREEN, 
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
                    max_count = max(brands_count.values()) if brands_count else 1
                    
                    for i, (brand, count) in enumerate(sorted_brands):
                        bar_width = (count / max_count) * 400
                        color = colors[i % len(colors)]
                        
                        chart_rows.append(
                            ft.Container(
                                content=ft.Row(
                                    [
                                        ft.Container(
                                            content=ft.Text(
                                                brand,
                                                size=14,
                                                weight=ft.FontWeight.BOLD,
                                                color=ft.Colors.BLACK
                                            ),
                                            width=120,
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
                                                                str(count),
                                                                size=12,
                                                                weight=ft.FontWeight.BOLD,
                                                                color=ft.Colors.WHITE
                                                            ),
                                                            alignment=ft.alignment.center
                                                        ) if bar_width > 40 else None
                                                    )
                                                ],
                                                spacing=0
                                            ),
                                            width=420,  
                                            alignment=ft.alignment.center_left
                                        ),
                                        
                                        ft.Container(
                                            content=ft.Text(
                                                f"{count} produto{'s' if count != 1 else ''}",
                                                size=12,
                                                color=ft.Colors.GREY_700
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
                    
                    chart_container.content = ft.Column(
                        [
                            ft.Text(
                                "📊 Produtos por Marca",
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
                                width=650
                            ),
                            
                            ft.Container(height=15),
                            ft.Row(
                                [
                                    ft.Text(
                                        f"Total de marcas: {len(brands_count)}",
                                        size=12,
                                        color=ft.Colors.GREY_700,
                                        weight=ft.FontWeight.BOLD
                                    ),
                                    ft.Text(
                                        f"Total de produtos: {sum(brands_count.values())}",
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
                chart_container.content = ft.Container(
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

        except Exception as ex:
            chart_container.content = ft.Container(
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
                    "Gráfico de Marcas",
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
                                            text="Atualizar Gráfico",
                                            icon=ft.Icons.REFRESH,
                                            on_click=lambda e: load_brands_chart(),
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
                                chart_container
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
    
    return main_container, load_brands_chart