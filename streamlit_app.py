# Import python packages
import streamlit as st
# from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col

cnx = st.connection("snowflake")
session = cnx.session()

# Write directly to the app
st.title(":cup_with_straw: Customize your smoothie: :cup_with_straw:")
st.write(
  """
  Choose the fruits you want in your customized smoothie!
  """
)

name_on_order = st.text_input("Name on smoothie:")
st.write("Thanks: ", name_on_order)

my_dataframe = session.table("smoothies.public.fruit_options").select(col('fruit_name'))
# st.dataframe(data=my_dataframe, use_container_width=True)

ingredients_list = st.multiselect(
    "Choose up to 5 ingredients:",
    my_dataframe,
    max_selections=5
)

if ingredients_list:

    ingredients_string = ''

    for each_fruit in ingredients_list:
        ingredients_string += each_fruit + ' '

    st.write(ingredients_string)

    sql_query = """
    insert into smoothies.public.orders(name_on_order,ingredients)
    values ('""" + name_on_order + """','""" + ingredients_string + """')"""

    # st.write(sql_query)

    time_to_insert = st.button("Submit order")
    
    if time_to_insert:
        session.sql(sql_query).collect()
        st.success(name_on_order + ', your smoothie is ordered!' , icon="✅")

import requests
smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")
st.text(smoothiefroot_response)
