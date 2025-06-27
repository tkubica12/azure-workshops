import reflex as rx

def index():
    return rx.text("Hello World")

app = rx.App()
app.add_page(index)
