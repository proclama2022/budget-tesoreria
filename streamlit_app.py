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
    Fornisci l'output con una tabella in formato markdown che visualizza il budget di tesoreria mensile.
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
    
    return message.content[0].text

st.title("Generatore di Budget di Tesoreria")

st.header("Dati Storici")

# Lista di tutti i mesi
all_months = ["Gennaio", "Febbraio", "Marzo", "Aprile", "Maggio", "Giugno", 
              "Luglio", "Agosto", "Settembre", "Ottobre", "Novembre", "Dicembre"]

# Ottieni l'anno corrente
current_year = date.today().year

# Crea una lista di opzioni per i mesi, includendo l'anno corrente e quello precedente
month_options = [f"{month} {current_year}" for month in all_months] + [f"{month} {current_year-1}" for month in all_months]

# Permetti all'utente di selezionare i 3 mesi più recenti
selected_months = st.multiselect(
    "Seleziona i 3 mesi più recenti per i dati storici",
    options=month_options,
    default=month_options[:3],  # Seleziona i primi 3 mesi come default
    max_selections=3
)

historical_data = {}

for month in selected_months:
    st.subheader(f"Dati per {month}")
    
    historical_data[month] = {
        "Cassa all'inizio del periodo": st.number_input(f"Cassa iniziale di {month}", min_value=0.0, format="%.2f", key=f"cassa_{month}"),
        "Vendite": st.number_input(f"Vendite totali per {month}", min_value=0.0, format="%.2f", key=f"vendite_{month}"),
        "Costi fissi": st.number_input(f"Costi fissi per {month}", min_value=0.0, format="%.2f", key=f"costi_fissi_{month}"),
        "Costi variabili": st.number_input(f"Costi variabili per {month}", min_value=0.0, format="%.2f", key=f"costi_variabili_{month}"),
        "Investimenti": st.number_input(f"Investimenti per {month}", min_value=0.0, format="%.2f", key=f"investimenti_{month}"),
        "Debiti": st.number_input(f"Rimborso debiti per {month}", min_value=0.0, format="%.2f", key=f"debiti_{month}"),
    }

st.header("Assunzioni per le proiezioni future")
assumptions = st.text_area("Inserisci le assunzioni per le proiezioni future:")

projection_months = st.selectbox("Seleziona il periodo di proiezione", [6, 12])

if st.button("Genera Budget di Tesoreria"):
    if len(selected_months) == 3 and assumptions:
        historical_data_str = "\n".join([f"{month}:\n" + "\n".join([f"  {k}: {v}" for k, v in data.items()]) for month, data in historical_data.items()])
        
        budget_output = generate_treasury_budget(historical_data_str, assumptions, projection_months)
        
        st.markdown(budget_output)
    else:
        st.warning("Per favore, seleziona esattamente 3 mesi e inserisci le assunzioni.")