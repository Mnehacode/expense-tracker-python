import matplotlib.pyplot as plt 
import streamlit as st
import pandas as pd
from datetime import date
import os

# ---------- Load or Create CSV ----------
FILE_NAME = "data.csv"

if os.path.exists(FILE_NAME):
    df = pd.read_csv(FILE_NAME)
else:
    df = pd.DataFrame(columns=["Date", "Description", "Category", "Amount"])

# ---------- App Title ----------
st.title("💰 Expense Tracker App")

# ---------- Input Form ----------
st.subheader("Add New Expense")

with st.form("expense_form"):
    expense_date = st.date_input("Select Date", value=date.today())
    description = st.text_input("Description")
    category = st.selectbox(
        "Category",
        ["Food", "Travel", "Shopping", "Bills", "Other"]
    )
    amount = st.number_input("Amount", min_value=0.0)

    submit = st.form_submit_button("Add Expense")

    if submit:
        new_data = {
            "Date": expense_date,
            "Description": description,
            "Category": category,
            "Amount": amount
        }

        df = pd.concat([df, pd.DataFrame([new_data])], ignore_index=True)
        df.to_csv(FILE_NAME, index=False)

        st.success("Expense Added Successfully!")

# ---------- Show All Expenses ----------
st.subheader("All Expenses")
st.dataframe(df)

# ---------- Summary Chart ----------
if not df.empty:
    st.subheader("Expenses by Category")

    summary = df.groupby("Category")["Amount"].sum()

    fig, ax = plt.subplots()
    ax.bar(summary.index, summary.values)

    ax.set_xlabel("Category")
    ax.set_ylabel("Total Amount")
    ax.set_title("Category-wise Expense Summary")

    for i, value in enumerate(summary.values):
        ax.text(i, value, str(value), ha='center', va='bottom')

    st.pyplot(fig)

