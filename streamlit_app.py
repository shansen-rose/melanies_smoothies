import streamlit as st
# from snowflake.snowpark.context import get_active_session
# from snowflake.snowpark.functions import col

st.title(f"Customize Your Smoothie :cup_with_straw:")
st.write(
  "Choose the fruits you want in your custom Smoothie!"
)

name_on_order = st.text_input('Name on Smoothie:')
st.write("The name on your Smoothie will be:", name_on_order)

cnx = st.connection("snowflake")
session = cnx.session()
# session = get_active_session()
# my_dataframe = session.table('smoothies.public.fruit_options').select(col('fruit_name'))

# ingredients_list = st.multiselect(
#     'Choose up to 5 ingredients:'
#     , my_dataframe
#     , max_selections=5
# )

# if ingredients_list:
#     ingredients_string = ''
#     for fruit_chosen in ingredients_list:
#         ingredients_string += fruit_chosen + ', '
#         my_insert_stmt = """
#         insert into smoothies.public.orders(name_on_order, ingredients)
#         values ('""" + name_on_order + """', '""" + ingredients_string + """')"""

#     time_to_insert = st.button('Submit Order')
    
#     if time_to_insert:
#         session.sql(my_insert_stmt).collect()
#         st.success('Your Smoothie is ordered, ' + name_on_order + '!', icon="✅")

#     # st.write(my_insert_stmt)
#     # st.stop()

# --- CHANGED ---
# Fetch the fruit options as a list of strings instead of using Snowpark 'col'
my_dataframe = session.table('smoothies.public.fruit_options')
fruit_list = [row['FRUIT_NAME'] for row in my_dataframe.collect()]  # <-- NEW

ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:',
    fruit_list,   # <-- CHANGED: use the Python list instead of Snowpark DF
    max_selections=5
)

if ingredients_list:
    # --- CHANGED ---
    # Use join instead of manually looping
    ingredients_string = ', '.join(ingredients_list)  # <-- NEW

    # --- CHANGED ---
    # f-string for cleaner SQL
    my_insert_stmt = f"""
    insert into smoothies.public.orders(name_on_order, ingredients)
    values ('{name_on_order}', '{ingredients_string}')
    """  # <-- CHANGED

    time_to_insert = st.button('Submit Order')
    
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success(f'Your Smoothie is ordered, {name_on_order}!', icon="✅")  # <-- CHANGED
