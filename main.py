from sheets_api import authenticate_sheets, append_to_sheet, read_sheet
from openai_api import send_prompt_to_gpt

SPREADSHEET_ID = '12_Dhf5ElWWlWwNlJ04gK-KNZderJNzNR6fTWILFNtNQ'
RANGE_NAME = 'A2:P4911'


def main():
  service = authenticate_sheets()
  sheet_data = read_sheet(service, SPREADSHEET_ID, RANGE_NAME)

  for index, row in enumerate(sheet_data):
    if len(row) < 16 or row[15].lower() != 'FALSO':
      continue

    valor_G = row[6]  # Asume que G está en el índice 6
    valor_M = row[12]  # Asume que M está en el índice 12

    gpt_response = send_prompt_to_gpt(valor_G, valor_M)

    if gpt_response:
      try:
        response_data = json.loads(gpt_response)
        # Asume que los índices para H, I, y N son 7, 8 y 13 respectivamente
        update_values = [[
            response_data.get('Department', ''),
            response_data.get('RoleLevel', ''),
            response_data.get('Language', '')
        ]]
        append_to_sheet(service, SPREADSHEET_ID, f'H{index+2}:N{index+2}',
                        update_values)  # Ajusta según tu rango de celdas
        append_to_sheet(service, SPREADSHEET_ID, f'P{index+2}',
                        [['VERDADERO']])  # Actualiza P a 'VERDADERO'
      except json.JSONDecodeError:
        print(
            f"Error al decodificar la respuesta de GPT para la fila {index+2}")


if __name__ == '__main__':
  main()
