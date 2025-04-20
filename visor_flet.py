import flet as ft
import pymysql
import pandas as pd

DB_CONFIG = {
    "host": "yamanote.proxy.rlwy.net",
    "port": 51558,
    "user": "root",
    "password": "UJuewnvyQAwjjEIjUeBJPJRGyVOqKbDE",
    "database": "railway"
}

cols = [
    "Recibo", "Fecha", "Concepto 1", "Importe", "Descuento", "Total", "Concepto 2", "Contribuyente",
    "Dirección", "Status", "Efectivo", "Tarjeta", "Transferencia", "Forma Pago", "Cheque"
]

def main(page: ft.Page):
    page.title = "ERP METEORITO - Visor Web"
    page.scroll = "always"

    filtro_txt = ft.TextField(label="Buscar por contribuyente", expand=True)
    desde_fecha = ft.TextField(label="Desde (aammdd)", width=150)
    hasta_fecha = ft.TextField(label="Hasta (aammdd)", width=150)
    tabla = ft.DataTable(columns=[ft.DataColumn(ft.Text(col)) for col in cols], rows=[])

    datos = []

    def cargar_datos(e=None):
        filtro = filtro_txt.value.lower()
        desde = desde_fecha.value
        hasta = hasta_fecha.value

        try:
            conexion = pymysql.connect(**DB_CONFIG)
            cursor = conexion.cursor()
            query = f"SELECT id_recibo, id_fecha, id_concepto1, id_importe, id_descuento, id_neto, id_concepto2, id_contribuyente, id_direccion, id_status, id_efectivo, id_tarjeta, id_transferencia, id_formapago, id_cheque FROM TEARMO01"
            cursor.execute(query)
            resultados = cursor.fetchall()

            tabla.rows.clear()
            datos.clear()

            for row in resultados:
                if filtro in str(row[7]).lower():
                    if desde and row[1] < desde:
                        continue
                    if hasta and row[1] > hasta:
                        continue

                    datos.append(row)
                    tabla.rows.append(
                        ft.DataRow(cells=[ft.DataCell(ft.Text(str(cell))) for cell in row])
                    )
            page.update()
        except Exception as err:
            page.snack_bar = ft.SnackBar(ft.Text(f"Error: {err}"), open=True)
            page.update()

    def exportar_excel(e):
        if not datos:
            page.snack_bar = ft.SnackBar(ft.Text("No hay datos para exportar."), open=True)
            page.update()
            return
        df = pd.DataFrame(datos, columns=cols)
        archivo = "exportado_recibos.xlsx"
        df.to_excel(archivo, index=False)
        page.snack_bar = ft.SnackBar(ft.Text(f"Exportado a {archivo}"), open=True)
        page.update()

    page.add(
        ft.Row([
            filtro_txt,
            desde_fecha,
            hasta_fecha,
            ft.ElevatedButton("Buscar", on_click=cargar_datos),
            ft.ElevatedButton("Exportar Excel", on_click=exportar_excel, bgcolor=ft.Colors.GREEN, color=ft.Colors.WHITE),
        ]),
        ft.Container(height=20),
        tabla
    )

ft.app(target=main)
