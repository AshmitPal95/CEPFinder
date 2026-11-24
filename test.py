import flet as ft
import inspect

def main(page: ft.Page):

    print("SnackBar signature:")
    print(inspect.signature(ft.SnackBar))

    def show_old(e):
        print("Button clicked")

        page.snack_bar = ft.SnackBar(
            content=ft.Text("Hello from snack_bar")
        )

        page.snack_bar.open = True
        page.update()

    def show_add(e):
        print("Add snackbar clicked")

        sb = ft.SnackBar(
            content=ft.Text("Hello via add()")
        )

        page.add(sb)

        sb.open = True
        page.update()

    page.add(
        ft.Text("SnackBar Test"),
        ft.OutlinedButton(
            "Test snack_bar property",
            on_click=show_old
        ),
        ft.OutlinedButton(
            "Test add() method",
            on_click=show_add
        )
    )

ft.run(main)