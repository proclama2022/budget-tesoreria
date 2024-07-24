import streamlit as st
import pandas as pd
import anthropic
from datetime import date, timedelta

def generate_treasury_budget(historical_data, assumptions, months):
    prompt = f"""
    Basandoti sui seguenti dati storici:
    {historical_data}
    
    E sulle seguenti assunzioni:
    {assumptions}
    
    Genera una proiezione del budget di tesoreria per i prossimi {months} mesi.
    Fornisci l'output in formato markdown con una tabella che visualizza il budget di tesoreria mensile.
    """
    
    client = anthropic.Anthropic(api_key=st.secrets["API_CLAUDE"])
    message = client.messages.create(
        model="claude-3-sonnet-20240229",
        max_tokens=4096,
        temperature=0,
        system="Sei un esperto finanziario specializzato nella creazione di budget di tesoreria.",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    
    return message.content

st.title("Generatore di Budget di Tesoreria")

st.header("Dati Storici")

months = 3
end_date = date.today().replace(day=1) - timedelta(days=1)

historical_data = {}

for i in range(months):
    current_date = (end_date - timedelta(days=30*i)).replace(day=1)
    current_date_str = current_date.strftime("%B %Y")
    st.subheader(f"Dati per {current_date_str}")
    
    historical_data[current_date_str] = {
        "Vendite": st.number_input(f"Vendite totali per {current_date_str}", min_value=0.0, format="%.2f", key=f"vendite_{i}"),
        "Costi fissi": st.number_input(f"Costi fissi per {current_date_str}", min_value=0.0, format="%.2f", key=f"costi_fissi_{i}"),
        "Costi variabili": st.number_input(f"Costi variabili per {current_date_str}", min_value=0.0, format="%.2f", key=f"costi_variabili_{i}"),
        "Investimenti": st.number_input(f"Investimenti per {current_date_str}", min_value=0.0, format="%.2f", key=f"investimenti_{i}"),
        "Debiti": st.number_input(f"Rimborso debiti per {current_date_str}", min_value=0.0, format="%.2f", key=f"debiti_{i}"),
    }

st.header("Assunzioni per le proiezioni future")
assumptions = st.text_area("Inserisci le assunzioni per le proiezioni future:")

projection_months = st.selectbox("Seleziona il periodo di proiezione", [6, 12])

if st.button("Genera Budget di Tesoreria"):
    if historical_data and assumptions:
        historical_data_str = "\n".join([f"{month}:\n" + "\n".join([f"  {k}: {v}" for k, v in data.items()]) for month, data in historical_data.items()])
        
        budget_output = generate_treasury_budget(historical_data_str, assumptions, projection_months)
        
        st.markdown(budget_output)
    else:
        st.warning("Per favore, inserisci sia i dati storici che le assunzioni.")