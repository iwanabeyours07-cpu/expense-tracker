import streamlit as st
import pandas as pd
import os
from datetime import date

FILE_NAME = "expenses.csv"

st.set_page_config(page_title="Expense Tracker", page_icon="💰")

def load_data():
    if os.path.exists(FILE_NAME):
        return pd.read_csv(FILE_NAME)
    return pd.DataFrame(columns=["Date", "Category", "Amount", "Note"])

def save_data(df):
    df.to_csv(FILE_NAME, index=False)

df = load_data()

st.title("💰 Expense Tracker")

with st.form("expense_form"):
    expense_date = st.date_input("Date", value=date.today())
    category = st.selectbox(
        "Category",
        ["Food", "Travel", "Shopping", "Bills", "Other"]
    )
    amount = st.number_input("Amount", min_value=0.0)
    note = st.text_input("Note")

    submit = st.form_submit_button("Add Expense")

    if submit:
        new_data = pd.DataFrame([{
            "Date": expense_date,
            "Category": category,
            "Amount": amount,
            "Note": note
        }])

        df = pd.concat([df, new_data], ignore_index=True)
        save_data(df)
        st.success("Expense Added!")

if not df.empty:
    st.subheader("Expense History")
    st.dataframe(df)

    st.subheader("Total Spent")
    st.write(f"₹ {df['Amount'].sum()}")

    st.subheader("Category-wise Spending")
    st.bar_chart(df.groupby("Category")["Amount"].sum())