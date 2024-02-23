# main.py

import json
import time
from sheets_api import authenticate_sheets, read_sheet

from openai_api import send_prompt_to_gpt

SPREADSHEET_ID = '12_Dhf5ElWWlWwNlJ04gK-KNZderJNzNR6fTWILFNtNQ'
RANGE_NAME = 'A2:P4911'  # Ajusta este rango según sea necesario

def process_gpt_response(gpt_response):
    try:
        response_dict = json.loads(gpt_response)
        values = list(response_dict.values())
        return values[:3]  # Retorna solo los primeros tres valores
    except json.JSONDecodeError:
        print("Error al decodificar la respuesta de GPT.")
        return None, None, None

def update_cell(service, spreadsheet_id, cell_range, value):
    body = {'values': [[value]]}
    service.spreadsheets().values().update(
        spreadsheetId=spreadsheet_id,
        range=cell_range,
        valueInputOption='USER_ENTERED',
        body=body
    ).execute()
    print(f"Actualizado: {cell_range} con '{value}'.")

def main():
    print("Autenticando y obteniendo acceso a la hoja de cálculo...")
    service = authenticate_sheets()

    print(f"Obteniendo datos de la hoja de cálculo desde el rango: {RANGE_NAME}")
    sheet_data = read_sheet(service, SPREADSHEET_ID, RANGE_NAME)

    if not sheet_data:
        print("No se encontraron datos en la hoja de cálculo.")
        return

    print(f"Se encontraron {len(sheet_data)} filas para procesar.")
    for index, row in enumerate(sheet_data, start=2):  # Ajusta el índice de inicio según tus necesidades
        valor_G = row[6] if len(row) > 6 else ""  # Suponiendo que 'G' está en el índice 6
        valor_M = row[12] if len(row) > 12 else ""  # Suponiendo que 'M' está en el índice 12

        if valor_G or valor_M:  # Si hay información en G o M
            prompt = f"{valor_G}, {valor_M}".strip(', ')
            print(f"Fila {index}: Procesando con el prompt: '{prompt}'")

            gpt_response = send_prompt_to_gpt(prompt)

            if gpt_response:
                print(f"Fila {index}: Respuesta de GPT recibida.")
                values = process_gpt_response(gpt_response)
                if values:
                    for i, column in enumerate(['H', 'I', 'N'], start=0):
                        update_cell(service, SPREADSHEET_ID, f'{column}{index}', values[i])
                else:
                    print(f"Fila {index}: Error al procesar la respuesta de GPT.")
            else:
                print(f"Fila {index}: No se recibió respuesta de GPT.")
        else:
            print(f"Fila {index}: Faltan datos en G y M, marcando P como FALSO.")
            update_cell(service, SPREADSHEET_ID, f'P{index}', 'FALSO')

        # Marca la columna P como VERDADERO después de procesar la fila
        update_cell(service, SPREADSHEET_ID, f'P{index}', 'VERDADERO')

        # Inserta una pausa después de procesar cada 15 filas
        if (index - 1) % 15 == 0 and index > 2:  # No pausar en la primera fila procesada
            print("Pausando para evitar superar la cuota de solicitudes de escritura...")
            time.sleep(60)  # Pausa de 60 segundos

if __name__ == '__main__':
    main()