import streamlit as st
import math

# Bitcoin Valuation App (Web Version)
def bitcoin_scarcity_valuation(gold_market_cap_trillions, btc_share_pct, circulating_supply=19_700_000):
    btc_market_cap = (gold_market_cap_trillions * 1_000_000_000_000) * (btc_share_pct / 100)
    price_per_btc = btc_market_cap / circulating_supply
    return round(price_per_btc, 2)

def metcalfe_valuation(user_count):
    base_value = 1_000_000_000_000  # $1 Trillion base value
    base_users = 100_000_000
    relative_value = base_value * (user_count / base_users)**2
    return round(relative_value, 2)

def price_from_network_value(network_value, circulating_supply=19_700_000):
    return round(network_value / circulating_supply, 2)

def stock_to_flow(circulating_supply, annual_new_supply):
    if annual_new_supply == 0:
        return float('inf')
    return circulating_supply / annual_new_supply

def s2f_model_price(s2f_value, a=-0.38, b=3.36):
    # PlanB's original constants from regression
    log_price = a + b * math.log10(s2f_value)
    return round(10 ** log_price, 2)

# Streamlit App
st.title("📈 Bitcoin Valuation Calculator")
st.markdown("Estimate Bitcoin price using scarcity, S2F, and network adoption models")

st.header("1️⃣ Scarcity-Based Valuation")
gold_market_cap = st.slider("Global Gold Market Cap (in Trillion USD)", 5, 20, 13)
btc_share = st.slider("Bitcoin's Share of Gold Market (%)", 1, 50, 15)
scarcity_price = bitcoin_scarcity_valuation(gold_market_cap, btc_share)
st.success(f"Estimated BTC Price (Scarcity Model): ${scarcity_price}")

st.header("2️⃣ Network Adoption Valuation (Metcalfe's Law)")
user_count = st.number_input("Estimated Active Bitcoin Users", min_value=10_000_000, max_value=1_000_000_000, value=300_000_000, step=10_000_000)
network_value = metcalfe_valuation(user_count)
btc_price_metcalfe = price_from_network_value(network_value)

st.info(f"Network Value: ${network_value:,}")
st.success(f"Implied BTC Price (Metcalfe's Law): ${btc_price_metcalfe}")

st.header("3️⃣ Stock-to-Flow Model")
circulating_supply = st.number_input("Current Circulating BTC", min_value=10000000, max_value=21000000, value=19_700_000, step=100000)
annual_new_supply = st.number_input("Annual New BTC Supply", min_value=10000, max_value=1000000, value=165_000, step=10000)
s2f = stock_to_flow(circulating_supply, annual_new_supply)
s2f_price = s2f_model_price(s2f)

st.info(f"S2F Ratio: {s2f:.2f}")
st.success(f"Estimated BTC Price (S2F Model): ${s2f_price}")

st.markdown("---")
st.caption("Created by Abhi, using GPT – Crypto Valuation Module 🧠")
