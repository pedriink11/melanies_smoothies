# Import python packages
import streamlit as st
# from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col
import requests
import pandas as pd

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

my_dataframe = session.table("smoothies.public.fruit_options").select(col('fruit_name'), col('search_on'))
# st.dataframe(data=my_dataframe, use_container_width=True)
# st.stop()

# Convert the snowpark dataframe to pandas
pd_df = my_dataframe.to_pandas()
# st.dataframe(pd_df)
# st.stop()

ingredients_list = st.multiselect(
    "Choose up to 5 ingredients:",
    my_dataframe,
    max_selections=5
)

if ingredients_list:

    ingredients_string = ''

    for each_fruit in ingredients_list:
        ingredients_string += each_fruit + ' '

        search_on=pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
        st.write('The search value for ', fruit_chosen,' is ', search_on, '.')
      
        st.subheader(each_fruit + ' Nutrition Information')
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/" + each_fruit)
        st.text(smoothiefroot_response.json())
        df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)

    st.write(ingredients_string)

    sql_query = """
    insert into smoothies.public.orders(name_on_order,ingredients)
    values ('""" + name_on_order + """','""" + ingredients_string + """')"""

    # st.write(sql_query)

    time_to_insert = st.button("Submit order")
    
    if time_to_insert:
        session.sql(sql_query).collect()
        st.success(name_on_order + ', your smoothie is ordered!' , icon="✅")


# smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")
# st.text(smoothiefroot_response.json())
# df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)
