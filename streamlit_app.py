import streamlit as st
from snowflake.snowpark.functions import col
import requests
import pandas

st.title(f"Customize Your Smoothie :cup_with_straw:")
st.write("Choose the fruits you want in your custom Smoothie!")

name_on_order = st.text_input('Name on Smoothie:')
st.write("The name on your Smoothie will be:", name_on_order)

conn = st.connection("snowflake")
session = conn.session()  

my_dataframe = session.table('smoothies.public.fruit_options').select(col('fruit_name'), col('search_on'))
pd_df=my_dataframe.to_pandas()


ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:'
    , my_dataframe
    , max_selections=6
)

if ingredients_list:
    ingredients_string = ', '.join(ingredients_list)
    
    for fruit_chosen in ingredients_list:
        search_on = pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
        st.write('The search value for ', fruit_chosen, ' is ', search_on, '.')
        st.subheader(fruit_chosen + ' Nutrition Information:')
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/" + search_on)
        sf_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)
    
    my_insert_stmt = f"""
    INSERT INTO smoothies.public.orders(name_on_order, ingredients)
    VALUES ('{name_on_order}', '{ingredients_string}')
    """
    
    time_to_insert = st.button('Submit Order', key='submit_order_button')
    
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success(f'Your Smoothie is ordered, {name_on_order}!', icon="✅")




