import streamlit as st
import pandas as pd
import numpy as np
import math

commodity_kilo_price = pd.read_csv('commodities_price_kilogram.csv', index_col = 0).squeeze("columns")

st.title('Are you worth your weight in gold?')

weight = st.number_input('Insert your body weight in kg',
                         step = 1,
                        value = 0,
                        help = 'For non-metric users: a stone is about 6.35 kg')

wealth = st.number_input('Insert your net worth/wealth in US Dollars',
                         step = 1000,
                        value = 0,
                        help = "Depending on how seriously you're taking this, you can calculate your net worth based on your savings and assets, but a random number is fine as well")

if wealth < 0:
    st.warning("You're not worth any commodity if your net worth is negative")
else:
    if weight <= 0:
        st.warning("Your body weight cannot be zero or negative")
    else:

        commodity_price_body_weight = commodity_kilo_price * weight
        if wealth < commodity_price_body_weight.min():
            st.error("You're either too poor, too heavy, or both, to be worth your weight in any commodity")
        else:
            counter = 0
            while wealth >= commodity_price_body_weight.min():
                counter += 1
                possible_commodities = commodity_price_body_weight[commodity_price_body_weight <= wealth]
                com_ind =  np.argmax(possible_commodities)
                selected_commodity = possible_commodities.index[com_ind]
                if selected_commodity == 'Gold':
                    st.success('Yes, you are! You are worth a total sum of:')
                    st.balloons()
                elif counter == 1:
                    st.error("Sadly, you aren't worth your weight in gold. You are however, worth your weight in other commodities for a total sum of:")
                selected_cost = possible_commodities[com_ind]
                nr_times_weight = math.floor(wealth /selected_cost)
                wealth -= selected_cost * nr_times_weight
                if nr_times_weight > 1:
                    times_sing_plur = 'times'
                else:
                    times_sing_plur = 'time'
                st.write('{} {} your weight in {}'.format(nr_times_weight,times_sing_plur, selected_commodity))
                
st.info('The price per kg of gold and other commodities is based on the monthly [World Bank report](https://www.worldbank.org/en/research/commodity-markets)')
