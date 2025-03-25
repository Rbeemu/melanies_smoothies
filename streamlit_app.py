import streamlit as st
from snowflake.snowpark import Session
from snowflake.snowpark.functions import col
import requests
import pandas as pd

helpful_links = [
    "https://docs.streamlit.io",
    "https://docs.snowflake.com/en/developer-guide/streamlit/about-streamlit",
    "https://github.com/Snowflake-Labs/snowflake-demo-streamlit",
    "https://docs.snowflake.com/en/release-notes/streamlit-in-snowflake"
]

# Write directly to the app
st.title("Customize your Smoothie :cup_with_straw:")
st.write("Choose the fruits you want in your custom smoothie:")

name_on_order = st.text_input("Name on Smoothie")
st.write("The name on your smoothie will be:", name_on_order)

# Correct Snowpark session initialization
connection_parameters = {
    "account": "XQDGXMV-BVB63220",
    "user": "LREDDY",
    "password": "Mammu240320252",
    "role": "SYSADMIN",
    "warehouse": "COMPUTE_WH",
    "database": "smoothies",
    "schema": "public"
}

session = Session.builder.configs(connection_parameters).create()

# Fetching data with Snowpark
my_dataframe = session.table('fruit_options').select(col('FRUIT_NAME'), col('SEARCH_ON')).collect()

# Convert to Pandas DataFrame
pd_df = pd.DataFrame(my_dataframe)

st.dataframe(pd_df)

ingredients_list = st.multiselect(
    "Choose up to 5 ingredients",
    pd_df['FRUIT_NAME'].tolist(),
    max_selections=5
)

if ingredients_list:
    ingredients_string = ''

    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '
        search_on = pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
        st.subheader(fruit_chosen + ' Nutrition Information')
        
        # Print the search_on value for debugging
        st.write(f"Fetching data for: {search_on}")
        
        fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + search_on)
        st.dataframe(fruityvice_response.json(), use_container_width=True)
    
    st.write(ingredients_string)
    
    my_insert_stmt = f"""
    INSERT INTO smoothies.public.orders (ingredients, name_on_order)
    VALUES ('{ingredients_string}', '{name_on_order}')
    """
    
    time_to_insert = st.button('Submit Order')
    
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")
