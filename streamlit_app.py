import streamlit as st
from snowflake.snowpark.functions import col

st.title(f"Customize Your Smoothie :cup_with_straw:")
st.write("Choose the fruits you want in your custom Smoothie!")

name_on_order = st.text_input('Name on Smoothie:')
st.write("The name on your Smoothie will be:", name_on_order)

# Get Snowpark session by calling .session()
conn = st.connection("snowflake")
session = conn.session()  # <-- note the parentheses!

# Access the table via Snowpark session
my_dataframe = session.table('smoothies.public.fruit_options').select(col('fruit_name'))

ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:'
    , my_dataframe
    , max_selections=5
)

if ingredients_list:
    ingredients_string = ''
    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ', '
        my_insert_stmt = """
        insert into smoothies.public.orders(name_on_order, ingredients)
        values ('""" + name_on_order + """', '""" + ingredients_string + """')"""

    time_to_insert = st.button('Submit Order')
    
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered, ' + name_on_order + '!', icon="✅")

