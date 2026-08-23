# notification.py

import os

import smtplib
import pandas as pd
from pathlib import Path
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

SENDER_EMAIL = os.getenv("SENDER_EMAIL", "serjao.dreis@gmail.com")
SENDER_PASS = os.getenv("SENDER_ID")
RECEIVERS = ["serjao.dreis@gmail.com", "nathaliaraks@gmail.com", "lenna-goncalves@hotmail.com"]


def send_email_alert(title, contents):
	'''
	Send an email alert.
	'''

	if not SENDER_PASS:
		print("  [ERROR] App password (SENDER_PASS) not set.")
		return

	msg = MIMEMultipart()
	msg["From"] = SENDER_EMAIL
	msg['To'] = ", ".join(RECEIVERS)
	msg['Subject'] = title

	msg.attach(MIMEText(contents, 'plain', 'utf-8'))

	try:
		with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
			server.login(SENDER_EMAIL, SENDER_PASS)
			server.sendmail(SENDER_EMAIL, RECEIVERS, msg.as_string())

		print(" [SUCESS] Email sent successfully.")

	except Exception as e:
		print(f" [ERRO] Unable to send email: {e}")

csv_name = "data/inventario_remedios.csv"
csv_path = Path(__file__).parent / csv_name

df_meds = pd.DataFrame()
if csv_path.is_file():
    df_meds = pd.read_csv(csv_path)

if not df_meds.empty:
	df_shortage = (
	    df_meds
	    .query("qtd_atual < qtd_semana")
	    .filter(items=["nome", "medicamento", "qtd_atual", "qtd_semana", "dosagem", "id"])
	)

	if not df_shortage.empty:
		lines_text = [
		    f"• {row['nome']}: {row['medicamento']} {row['dosagem']} (Estoque: {row['qtd_atual']})"
		    for _, row in df_shortage.iterrows()
		]

		text_alert = (
			"Atenção, os seguintes medicamentos estão com estoque baixo e precisam ser comprados:\n\n"
            + "\n".join(lines_text)
            + "\n\nFavor providenciar a reposição."
			)

		send_email_alert(title = "[Inventario Medicamentos] Alerta de Compra de Remédios",
			contents = text_alert
			)
	else:
		print("Estoque sucifiente de remédios, nada a fazer.")


