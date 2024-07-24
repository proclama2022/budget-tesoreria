import streamlit as st
import pandas as pd
import anthropic
import os
from datetime import date, timedelta

# Funzione per generare il budget di tesoreria utilizzando Claude
def generate_treasury_budget(historical_data, assumptions, months):
    prompt = f"""
    Basandoti sui seguenti dati storici:
    {historical_data}
    
    E sulle seguenti assunzioni:
    {assumptions}
    
    Genera una proiezione del budget di tesoreria per i prossimi {months} mesi.
    Fornisci l'output in formato markdown con una tabella che visualizza il budget di tesoreria mensile.
    """
    
    client = anthropic.Anthropic(api_key=st.secrets("API_CLAUDE"))
    message = client.messages.create(
        model="claude-3-5-sonnet-20240620",
        max_tokens=4096,
        temperature=0,
        system="Sei un esperto finanziario specializzato nella creazione di budget di tesoreria.",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    
    return message.content

# Interfaccia utente Streamlit
st.title("Generatore di Budget di Tesoreria")

# Input per i dati storici
st.header("Dati Storici")

# Chiediamo all'utente di inserire i dati per gli ultimi 3 mesi
months = 3
end_date = date.today().replace(day=1) - timedelta(days=1)
start_date = (end_date - timedelta(days=90)).replace(day=1)

historical_data = {}

for i in range(months):
    current_date = (start_date + timedelta(days=30*i)).strftime("%B %Y")
    st.subheader(f"Dati per {current_date}")
    
    historical_data[current_date] = {
        "Vendite": st.number_input(f"Vendite totali per {current_date}", min_value=0.0, format="%.2f", key=f"vendite_{i}"),
        "Costi fissi": st.number_input(f"Costi fissi per {current_date}", min_value=0.0, format="%.2f", key=f"costi_fissi_{i}"),
        "Costi variabili": st.number_input(f"Costi variabili per {current_date}", min_value=0.0, format="%.2f", key=f"costi_variabili_{i}"),
        "Investimenti": st.number_input(f"Investimenti per {current_date}", min_value=0.0, format="%.2f", key=f"investimenti_{i}"),
        "Debiti": st.number_input(f"Rimborso debiti per {current_date}", min_value=0.0, format="%.2f", key=f"debiti_{i}"),
    }

# Input per le assunzioni
st.header("Assunzioni per le proiezioni future")
assumptions = st.text_area("Inserisci le assunzioni per le proiezioni future:")

# Selezione del periodo di proiezione
projection_months = st.selectbox("Seleziona il periodo di proiezione", [6, 12])

if st.button("Genera Budget di Tesoreria"):
    if historical_data and assumptions:
        # Convertiamo i dati storici in una stringa formattata
        historical_data_str = "\n".join([f"{month}:\n" + "\n".join([f"  {k}: {v}" for k, v in data.items()]) for month, data in historical_data.items()])
        
        # Genera il budget di tesoreria
        budget_output = generate_treasury_budget(historical_data_str, assumptions, projection_months)
        
        # Visualizza l'output
        st.markdown(budget_output)
    else:
        st.warning("Per favore, inserisci sia i dati storici che le assunzioni.")