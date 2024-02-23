import os
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")


def send_prompt_to_gpt(prompt):
  client = openai.OpenAI()

  # Aquí se construye el mensaje completo para el prompt de GPT, ajusta según tus necesidades.
  full_prompt = f"Clasifica los siguientes roles en el departamento y jerarquía correctos, considerando errores comunes previos. Roles como 'Sales executive', 'asesor comercial', 'Sales Representative', 'Especialista em comunicação', 'Account Manager', 'Ejecutivo de ventas', 'Ejecutivo de mercado', 'Brand Strategist', 'Especialista en CRM', 'Marketing Specialist', 'Desarrollo de negocios - Acuicultura', 'Sales Associate', 'Especialista en tecnología', 'UX/UI Designer', 'Full-stack Developer', 'Content Marketer & StorySeller en StorySelling', 'Email Marketer' deben clasificarse como 'Analista' en el departamento correspondiente, no como 'Gerente/Manager'. Por otro lado, 'Digital Marketing Leader', 'Jefe de Marketing y Alianzas Comerciales', 'Product Owner' deben ser clasificados como 'Gerente/Manager', no 'C-Suite/Founder'. Usa esta información para informar tus respuestas y responde en formato JSON sin dejar espacios vacíos o 'none'. Considera las siguientes opciones para cada categoría: '{{\"Departamento\": [\"Marketing\", \"Sales\", \"Support\", \"Onboarding\", \"Customer Success\", \"Product\", \"Operations\", \"Tech\", \"Growth\", \"Other\", \"Founder or Investor\"], \"Jerarquía\": [\"C-Suite/Founder\", \"Gerente/Manager\", \"Analista\"], \"Idioma\": [\"ES\", \"EN\", \"PT\", \"FR\", \"DE\", \"IT\", \"OTHER\"]}}'"

  response = client.chat.completions.create(
      model="gpt-3.5-turbo",
      messages=[{
          "role":
          "system",
          "content":
          "Este es un sistema que categoriza información de contactos."
      }, {
          "role": "user",
          "content": full_prompt
      }],
      temperature=0.1)

  if response.choices:
    return response.choices[0].message.content.strip()
  else:
    return None
