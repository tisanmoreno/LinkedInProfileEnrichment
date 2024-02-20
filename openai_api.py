import os
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")

def send_prompt_to_gpt(valor_G, valor_M):
    client = openai.OpenAI()

    prompt = f"Por favor, analiza los siguientes datos: {valor_G}, {valor_M}. Basándote en esta información respóndeme las siguientes preguntas de acuerdo a las opciones que te otorgo. Pregunta 1: ¿Cuál es el departamento del que hace parte este contacto? Opciones 1: { 'Department': ["Marketing", "Sales", "Support", "Onboarding", "Customer Success", "Product", "Operations", "Tech", "Growth", "Other", "Founder or Investor"] } Pregunta 2:¿Cuál es su jerarquía dentro de la empresa? Opciones 2: { 'RoleLevel': ["C-Suite/Founder", "Gerente/Manager", "Analista"] } Pregunta 3. ¿Qué idioma habla? Opciones 3: { 'Language': ["ES", "EN", "PT", "FR", "DE", "IT", "OTHER"] }. Sólo se recibirá una opción por criterio y no se acepta que uses alguna palabra por fuera de las opciones otorgadas (salvo que no tengas otra opción). El formato de respuesta solicitado es JSON y por ningún motivo dejes un espacio vacio o none. Por ejemplo: { 'Department': 'Sales', 'RoleLevel': 'Gerente/Manager', 'Languague': 'ES' }"

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Este es un sistema que categoriza información de contactos."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3
    )

    if response.choices:
        return response.choices[0].message.content.strip()
    else:
        return None