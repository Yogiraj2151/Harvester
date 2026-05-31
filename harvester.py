from pathlib import Path

import pandas as pd
import streamlit as st


DATA_FILE = Path("land_information.csv")
COLUMNS = ["Date", "Name", "Gunthe", "Price", "Online", "Cash", "Total Paid", "Balance"]


def load_data() -> pd.DataFrame:
    if DATA_FILE.exists():
        data = pd.read_csv(DATA_FILE)
        for column in COLUMNS:
            if column not in data.columns:
                data[column] = ""
        return data[COLUMNS]
    return pd.DataFrame(columns=COLUMNS)


def save_record(record: dict) -> None:
    data = load_data()
    data = pd.concat([data, pd.DataFrame([record])], ignore_index=True)
    data.to_csv(DATA_FILE, index=False)


st.set_page_config(page_title="Information Saver", page_icon=":moneybag:", layout="wide")

st.title("Information Saver")

with st.form("information_form", clear_on_submit=True):
    col1, col2 = st.columns(2)

    with col1:
        entry_date = st.date_input("Date")
        name = st.text_input("Name")
        gunthe = st.number_input("Gunthe", min_value=0.0, step=0.5)
        price = st.number_input("Price", min_value=0.0, step=1000.0)

    with col2:
        online = st.number_input("Online Payment", min_value=0.0, step=1000.0)
        cash = st.number_input("Cash Payment", min_value=0.0, step=1000.0)

    submitted = st.form_submit_button("Save Information")

if submitted:
    total_paid = online + cash
    balance = price - total_paid

    if not name.strip():
        st.error("Please enter name.")
    elif price <= 0:
        st.error("Please enter price.")
    else:
        save_record(
            {
                "Date": entry_date.isoformat(),
                "Name": name.strip(),
                "Gunthe": gunthe,
                "Price": price,
                "Online": online,
                "Cash": cash,
                "Total Paid": total_paid,
                "Balance": balance,
            }
        )
        st.success("Information saved successfully.")

data = load_data()

st.subheader("Saved Information")

if data.empty:
    st.info("No information saved yet.")
else:
    total_price = data["Price"].sum()
    total_online = data["Online"].sum()
    total_cash = data["Cash"].sum()
    total_balance = data["Balance"].sum()

    metric1, metric2, metric3, metric4 = st.columns(4)
    metric1.metric("Total Price", f"{total_price:,.2f}")
    metric2.metric("Online", f"{total_online:,.2f}")
    metric3.metric("Cash", f"{total_cash:,.2f}")
    metric4.metric("Balance", f"{total_balance:,.2f}")

    st.dataframe(data, use_container_width=True)

    csv_data = data.to_csv(index=False).encode("utf-8")
    st.download_button(
        "Download CSV",
        data=csv_data,
        file_name="land_information.csv",
        mime="text/csv",
    )
