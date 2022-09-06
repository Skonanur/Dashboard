import streamlit as st
from streamlit_option_menu import option_menu

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go


rz_colors = ['#0D94FB', '#012652']
rz_colors_2 = ['#012652', '#0D94FB']

# Change the Title in Web
st.set_page_config(page_title="Razorpay Dashboard",
                   layout="wide")

# Hide the Footer and Main Menu
hide_menu_style = """
                <style>
                #MainMenu {visibility: hidden; }
                footer {visibility: hidden;}
                </style>
                """
st.markdown(hide_menu_style, unsafe_allow_html=True)


class TreeMaps:
    def __init__(self, data):
        self.data = data

    # Returns a Credit DF for Table and another for the Treemap
    def credit_map(self):
        cards = self.data.drop(['upi_provider', 'upi_type'], axis=1)
        cards = cards[cards['payments_method'] == 'card']

        credit_df = cards[cards['cards_type'] == 'credit']
        credit_df = credit_df.dropna()

        credit_df['iins_iin'] = credit_df['iins_iin'].astype(int)
        credit_df['iins_iin'] = credit_df['iins_iin'].astype(str)

        credit_df = credit_df.groupby(
            ['error_code', 'internal_error_code', 'iins_iin', 'cards_issuer', 'cards_network', 'payments_gateway',
             'payments_auth_type']).size().reset_index().rename(columns={0: 'count'})

        top_credit = credit_df.copy()

        top_credit['bin_issuer_network'] = top_credit['iins_iin'] + ' + ' + top_credit['cards_issuer'] + ' + ' + \
                                           top_credit['cards_network']

        top_credit = top_credit.drop(['iins_iin', 'cards_issuer', 'cards_network'], axis=1)

        # Rearranging the Columns
        top_credit = top_credit[
            ['error_code', 'internal_error_code', 'bin_issuer_network', 'payments_gateway', 'payments_auth_type',
             'count']]

        top_credit = top_credit.sort_values(by=['count'], ascending=False).head(50)

        # Credit TreeMap
        credit_fig = px.treemap(credit_df,
                                path=['error_code', 'internal_error_code', 'cards_issuer', 'payments_gateway',
                                      'payments_auth_type'],
                                values='count')

        return top_credit, credit_fig

    # Returns a Debit DF for Table and another for the Treemap
    def debit_map(self):
        cards = self.data.drop(['upi_provider', 'upi_type'], axis=1)
        cards = cards[cards['payments_method'] == 'card']

        debit_df = cards[cards['cards_type'] == 'debit']
        debit_df = debit_df.dropna()

        debit_df['iins_iin'] = debit_df['iins_iin'].astype(int)
        debit_df['iins_iin'] = debit_df['iins_iin'].astype(str)

        debit_df = debit_df.groupby(
            ['error_code', 'internal_error_code', 'iins_iin', 'cards_issuer', 'cards_network', 'payments_gateway',
             'payments_auth_type']).size().reset_index().rename(columns={0: 'count'})

        top_debit = debit_df.copy()

        top_debit['bin_issuer_network'] = top_debit['iins_iin'] + ' + ' + top_debit['cards_issuer'] + ' + ' + top_debit[
            'cards_network']

        top_debit = top_debit.drop(['iins_iin', 'cards_issuer', 'cards_network'], axis=1)

        # Rearranging the Columns
        top_debit = top_debit[
            ['error_code', 'internal_error_code', 'bin_issuer_network', 'payments_gateway', 'payments_auth_type',
             'count']]

        top_debit = top_debit.sort_values(by=['count'], ascending=False).head(50)

        debit_fig = px.treemap(debit_df, path=['error_code', 'internal_error_code', 'cards_issuer', 'payments_gateway',
                                               'payments_auth_type'],
                               values='count')

        return top_debit, debit_fig

    # Returns a UPI DF for Table and another for the Treemap
    def upi_map(self):
        upi = self.data.drop(['iins_iin', 'cards_network', 'cards_issuer', 'cards_type', 'payments_auth_type'], axis=1)
        upi = upi[upi['payments_method'] == 'upi']
        upi = upi.drop('payments_method', axis=1)

        upi = upi.dropna()

        upi_df = upi.groupby(
            ['error_code', 'internal_error_code', 'upi_provider', 'payments_gateway']).size().reset_index().rename(
            columns={0: 'count'})

        top_upi = upi_df.sort_values(by=['count'], ascending=False).head(50)

        upi_fig = px.treemap(upi_df, path=['error_code', 'internal_error_code', 'upi_provider', 'payments_gateway'],
                             values='count')

        return top_upi, upi_fig


class Plots:
    def __init__(self, data):
        self.data = data

    def credit_plot(self):
        cards = self.data.drop(['upi_provider', 'upi_type'], axis=1)
        cards = cards[cards['payments_method'] == 'card']

        credit_df = cards[cards['cards_type'] == 'credit']
        credit_df = credit_df.dropna()

        credit_errors = credit_df.groupby(['error_code', 'internal_error_code']).size().reset_index().rename(
            columns={0: 'count'})
        # credit_errors = credit_errors[credit_errors['count'] > 200]

        return credit_errors

    def debit_plot(self):
        cards = self.data.drop(['upi_provider', 'upi_type'], axis=1)
        cards = cards[cards['payments_method'] == 'card']

        debit_df = cards[cards['cards_type'] == 'debit']
        debit_df = debit_df.dropna()

        debit_errors = debit_df.groupby(['error_code', 'internal_error_code']).size().reset_index().rename(
            columns={0: 'count'})
        # debit_errors = debit_errors[debit_errors['count'] > 200]

        return debit_errors

    def upi_plot(self):
        upi = self.data.drop(['iins_iin', 'cards_network', 'cards_issuer', 'cards_type', 'payments_auth_type'], axis=1)
        upi = upi[upi['payments_method'] == 'upi']
        upi = upi.drop('payments_method', axis=1)

        upi = upi.dropna()

        upi_df = upi.groupby(
            ['error_code', 'internal_error_code']).size().reset_index().rename(
            columns={0: 'count'})

        # upi_df = upi_df[upi_df['count'] > 200]

        return upi_df


code_text = """SELECT id, error_code, internal_error_code, iins_iin, payments_gateway, payments_auth_type, 
cards_network, cards_issuer,cards_type, is_success, payments_created_date, payments_method, upi_provider, upi_type
FROM realtime_hudi_api.payments
INNER JOIN warehouse.payments ON payments_id = id
WHERE payments_merchant_id = ''
AND payments_created_date BETWEEN 'YYYY-MM-DD' and 'YYYY-MM-DD';"""

st.code(code_text, language='sql')

# File Uploader
uploaded_file = st.file_uploader(label="Upload CSV File")

if uploaded_file:
    # Main Menu
    menu = option_menu(
        menu_title="Select:",
        options=["Credit", "Debit", "UPI"],
        orientation="horizontal"
    )
    # Read the Uploaded File
    full_data = pd.read_csv(uploaded_file)

    # full_data['payments_created_date'] = pd.to_datetime(full_data['payments_created_date'])
    full_data = full_data.sort_values(by=['payments_created_date'])

    col1, col2 = st.columns([1, 1])

    unique_dates = full_data['payments_created_date'].unique()

    with col1:
        start_date = st.selectbox("Start Date", unique_dates, index=0)

    with col2:
        end_date = st.selectbox("End Date", unique_dates, index=len(unique_dates) - 1)

    date_range = list(pd.date_range(start_date, end_date, freq='d').strftime("%Y-%m-%d"))

    df = full_data[full_data['payments_created_date'].isin(date_range)]

    # credit_date_df = credit_date_df[credit_date_df['internal_error_code'].isin(list_1)]

    # Object Instantiation
    treeMaps = TreeMaps(df)
    plots = Plots(df)

    if menu == "Credit":
        worst_credit = treeMaps.credit_map()[0].reset_index(drop=True)
        credit_map = treeMaps.credit_map()[1]

        credit_map.update_layout(
            margin=dict(l=40, r=40, t=90, b=60),
            # autosize=False,
            # hovermode=False,
            width=1000,
            height=600)

        # Worst Credit Combinations DataFrame
        st.header("Worst Credit Combinations")
        st.dataframe(worst_credit)

        # Plot Credit TreeMap
        st.header("Credit Errors Map:")
        st.write(credit_map)

        # Initialise from Class
        credit_plot = plots.credit_plot()

        credit_plot_donut = go.Figure(
            data=[go.Pie(labels=credit_plot['internal_error_code'], values=credit_plot['count'], hole=.4)])

        # Create Credit Donut Plot
        credit_plot_donut.update_layout(
            width=1000,
            height=1000)

        # Plot Credit Donut Plot
        st.write(credit_plot_donut)

    elif menu == "Debit":
        worst_debit = treeMaps.debit_map()[0].reset_index(drop=True)
        debit_map = treeMaps.debit_map()[1]

        debit_map.update_layout(
            margin=dict(l=40, r=40, t=90, b=60),
            # autosize=False,
            # hovermode=False,
            width=1000,
            height=600)

        # Worst Debit Combinations DataFrame
        st.header("Worst Debit Combinations")
        st.dataframe(worst_debit)

        # Plot Debit TreeMap
        st.header("Debit Errors Map:")
        st.write(debit_map)

        # Initialise from Class
        debit_plot = plots.debit_plot()

        # Create Debit Donut Plot
        debit_plot_donut = go.Figure(
            data=[go.Pie(labels=debit_plot['internal_error_code'], values=debit_plot['count'], hole=.4)])

        debit_plot_donut.update_layout(
            width=1000,
            height=1000)

        # Plot Debit Donut Plot
        st.write(debit_plot_donut)

    if menu == "UPI":
        worst_upi = treeMaps.upi_map()[0].reset_index(drop=True)
        upi_map = treeMaps.upi_map()[1]

        upi_map.update_layout(
            margin=dict(l=40, r=40, t=90, b=60),
            # autosize=False,
            # hovermode=False,
            width=1000,
            height=600)

        # Worst UPI Combinations DataFrame
        st.header("Worst UPI Combinations")
        st.dataframe(worst_upi)

        # Plot UPI TreeMap
        st.header("UPI Errors Map:")
        st.write(upi_map)

        # Initialise
        upi_plot = plots.upi_plot()

        # Create UPI Donut Plot
        upi_plot_donut = go.Figure(
            data=[go.Pie(labels=upi_plot['internal_error_code'], values=upi_plot['count'], hole=.4)])

        upi_plot_donut.update_layout(
            width=1000,
            height=1000)

        # Plot UPI Donut Plot
        st.write(upi_plot_donut)
