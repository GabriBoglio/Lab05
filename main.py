import flet as ft
from alert import AlertManager
from deposito_strumenti import DepositoStrumenti

FILE_STRUMENTI = "strumenti.csv"


def main(page: ft.Page):
    page.title = "Lab05"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.theme_mode = ft.ThemeMode.DARK
    page.scroll = ft.ScrollMode.AUTO

    alert = AlertManager(page)

    deposito = DepositoStrumenti("Deposito Strumenti Musicali", "Alessandro Visconti")
    try:
        deposito.carica_file_strumenti(FILE_STRUMENTI)
    except FileNotFoundError as e:
        alert.show_alert(f"❌ Impossibile trovare il file {FILE_STRUMENTI}. Si partirà da un deposito vuoto.")

    txt_titolo = ft.Text(value=deposito.nome, size=38, weight=ft.FontWeight.BOLD)
    txt_responsabile = ft.Text(
        value=f"Responsabile: {deposito.get_responsabile()}",
        size=16,
        weight=ft.FontWeight.BOLD
    )

    input_responsabile = ft.TextField(value=deposito.get_responsabile(), label="Responsabile")

    input_tipo = ft.TextField(label="Tipo (es. Chitarra)")
    input_marca = ft.TextField(label="Marca (es. Fender)")
    input_anno = ft.TextField(label="Anno acquisto (es. 2021)")

    input_valore = ft.TextField(value="0", text_align=ft.TextAlign.RIGHT, width=100)

    lista_strumenti = ft.ListView(expand=True, spacing=5, padding=10, auto_scroll=True)

    def aggiorna_lista_strumenti():
        lista_strumenti.controls.clear()
        for strumento in deposito.strumenti_ordinati_per_marca():
            stato = "✅" if strumento.disponibile else "⛔"
            lista_strumenti.controls.append(ft.Text(f"{stato} {strumento}"))
        page.update()

    def cambia_tema(e):
        page.theme_mode = ft.ThemeMode.DARK if toggle_cambia_tema.value else ft.ThemeMode.LIGHT
        toggle_cambia_tema.label = "Tema scuro" if toggle_cambia_tema.value else "Tema chiaro"
        page.update()

    def conferma_responsabile(e):
        deposito.set_responsabile(input_responsabile.value)
        txt_responsabile.value = f"Responsabile: {deposito.get_responsabile()}"
        page.update()

    def decrementa_valore(e):
        try:
            valore_attuale = float(input_valore.value)
            input_valore.value = str(max(0.0, valore_attuale - 10.0))
            page.update()
        except ValueError:
            pass

    def incrementa_valore(e):
        try:
            valore_attuale = float(input_valore.value)
            input_valore.value = str(valore_attuale + 10.0)
            page.update()
        except ValueError:
            pass

    def aggiungi_nuovo_strumento(e):
        tipo = input_tipo.value.strip()
        marca = input_marca.value.strip()

        if not tipo or not marca or not input_anno.value or not input_valore.value:
            alert.show_alert("Errore: Compila tutti i campi prima di procedere.")
            return

        try:
            anno = int(input_anno.value)
            valore = float(input_valore.value)
        except ValueError:
            alert.show_alert("Errore di validazione: Anno e Valore devono essere campi numerici validi.")
            return

        deposito.aggiungi_strumento(tipo, marca, anno, valore)

        input_tipo.value = ""
        input_marca.value = ""
        input_anno.value = ""
        input_valore.value = "0"

        aggiorna_lista_strumenti()

    toggle_cambia_tema = ft.Switch(label="Tema scuro", value=True, on_change=cambia_tema)
    pulsante_conferma_responsabile = ft.Button("Conferma", on_click=conferma_responsabile)

    btn_meno = ft.IconButton(ft.icons.REMOVE, on_click=decrementa_valore)
    btn_piu = ft.IconButton(ft.icons.ADD, on_click=incrementa_valore)
    btn_aggiungi_strumento = ft.Button("Aggiungi strumento", on_click=aggiungi_nuovo_strumento)

    page.add(
        toggle_cambia_tema,
        txt_titolo,
        txt_responsabile,
        ft.Divider(),
        ft.Text("Modifica Informazioni", size=20, weight=ft.FontWeight.BOLD),
        ft.Row(spacing=20,
               controls=[input_responsabile, pulsante_conferma_responsabile],
               alignment=ft.MainAxisAlignment.CENTER),
        ft.Divider(),
        ft.Text("Aggiungi Nuovo Strumento", size=20, weight=ft.FontWeight.BOLD),
        ft.Row(controls=[input_tipo, input_marca, input_anno], alignment=ft.MainAxisAlignment.CENTER),
        ft.Row(
            controls=[
                ft.Text("Valore (€):"),
                btn_meno,
                input_valore,
                btn_piu
            ],
            alignment=ft.MainAxisAlignment.CENTER
        ),
        btn_aggiungi_strumento,
        ft.Divider(),
        ft.Text("Lista degli Strumenti", size=20, weight=ft.FontWeight.BOLD),
        lista_strumenti,
    )
    aggiorna_lista_strumenti()


ft.run(main)