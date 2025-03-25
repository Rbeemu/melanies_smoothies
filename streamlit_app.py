import streamlit as st
import snowflake.connector 
from snowflake.snowpark.functions import col
import requests

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

# Correct Snowflake connection
conn = snowflake.connector.connect(
    user='LREDDY',
    password='Mammu240320252',
    account='XQDGXMV-BVB63220'
)
session = conn.cursor()

session.execute("USE DATABASE smoothies")
session.execute("USE SCHEMA public")
session.execute("SELECT FRUIT_NAME FROM fruit_options")
my_dataframe = session.fetchall()

ingredients_list = st.multiselect(
    "Choose up to 5 ingredients",
    [row[0] for row in my_dataframe],
    max_selections=5
)

if ingredients_list:
    ingredients_string = ''

    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '
        search_on = pd_df.loc [pd_df ['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'], iloc[0]
        st.subheader(fruit_chosen + ' Nutrition Information')
        fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + search_on)
        #smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/" + fruit_chosen)
        #st.dataframe(smoothiefroot_response.json(), use_container_width=True)
        fv_df = st.dataframe(data= fruityvice_response.json(), use_container_width=True)
        
        st.write(ingredients_string)
    
    my_insert_stmt = f"""
    INSERT INTO smoothies.public.orders (ingredients, name_on_order)
    VALUES ('{ingredients_string}', '{name_on_order}')
    """
    
    time_to_insert = st.button('Submit Order')
    
    if time_to_insert:
        session.execute(my_insert_stmt)
        st.success('Your Smoothie is ordered!', icon="✅")
