
import flet as ft
from pages.add_product import add_product_page
from pages.graph_brands import graph_brands_page
from pages.graph_expensive import graph_expensive_page

def main(page: ft.Page):
    page.title = "Gerenciador de Produtos"
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.theme_mode = ft.ThemeMode.DARK

    snack = ft.SnackBar(content=ft.Text(""), open=False)
    page.snack_bar = snack
    page.overlay.append(snack)

    current_page = "add_product"
    content_container = ft.Container(expand=True)
    pages = {
        "add_product": {
            "title": "Adicionar Produtos",
            "icon": ft.Icons.ADD_SHOPPING_CART,
            "page_func": add_product_page
        },
        "graph_brands": {
            "title": "Gráfico de Marcas", 
            "icon": ft.Icons.BAR_CHART,
            "page_func": graph_brands_page
        },
        "graph_expensive": {
            "title": "Produtos Caros",
            "icon": ft.Icons.TRENDING_UP,
            "page_func": graph_expensive_page
        }
    }
    
    def navigate_to(page_key):
        """Navega para uma página específica"""
        nonlocal current_page
        current_page = page_key
        
        for btn_key, button in nav_buttons.items():
            if btn_key == page_key:
                button.style = ft.ButtonStyle(
                    color=ft.Colors.WHITE,
                    bgcolor=ft.Colors.BLUE,
                    padding=ft.padding.symmetric(horizontal=20, vertical=12)
                )
            else:
                button.style = ft.ButtonStyle(
                    color=ft.Colors.BLUE,
                    bgcolor=ft.Colors.TRANSPARENT,
                    padding=ft.padding.symmetric(horizontal=20, vertical=12)
                )
        
        page_container, load_function = pages[page_key]["page_func"](page)
        content_container.content = page_container
        
        if load_function:
            load_function()
        
        page.update()
    
    nav_buttons = {}
    nav_button_list = []
    
    for page_key, page_info in pages.items():
        button = ft.TextButton(
            text=page_info["title"],
            icon=page_info["icon"],
            on_click=lambda e, pk=page_key: navigate_to(pk),
            style=ft.ButtonStyle(
                color=ft.Colors.BLUE,
                bgcolor=ft.Colors.TRANSPARENT,
                padding=ft.padding.symmetric(horizontal=20, vertical=12)
            )
        )
        nav_buttons[page_key] = button
        nav_button_list.append(button)
    
    nav_bar = ft.Container(
        content=ft.Row(
            [
                ft.Icon(ft.Icons.INVENTORY, color=ft.Colors.BLUE, size=30),
                ft.Text(
                    "Gerenciador de Produtos",
                    size=20,
                    weight=ft.FontWeight.BOLD,
                    color=ft.Colors.BLUE
                ),
                ft.Container(expand=True),  
                *nav_button_list
            ],
            spacing=10,
            vertical_alignment=ft.CrossAxisAlignment.CENTER
        ),
        bgcolor=ft.Colors.WHITE,
        padding=ft.padding.symmetric(horizontal=20, vertical=10),
        border=ft.border.only(bottom=ft.BorderSide(2, ft.Colors.GREY_300)),
        shadow=ft.BoxShadow(
            spread_radius=1,
            blur_radius=3,
            color=ft.Colors.with_opacity(0.1, ft.Colors.BLACK),
            offset=ft.Offset(0, 2)
        )
    )
    
    main_layout = ft.Column(
        [
            nav_bar,
            content_container
        ],
        spacing=0,
        expand=True
    )
    
    page.add(main_layout)
    navigate_to("add_product")

ft.app(target=main)