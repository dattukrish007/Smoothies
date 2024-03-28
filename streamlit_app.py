# Import python packages
import streamlit as st
import requests

from snowflake.snowpark.functions import col

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie!:cup_with_straw:")
st.write("Choose the fruits you want in your smoothie!")



# option = st.selectbox(
#    "What is your favorite fruite?",
#    ("Banana", "Strawberries", "Peaches"),
   
# )

# st.write('You selected:', option)


name_on_order = st.text_input('Name on Smoothie')
st.write('The name on your Smoothie will be', name_on_order)

cnx = st.connection('snowflake')
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'),col('SEARCH_ON'))

# st.dataframe(data=my_dataframe, use_container_width=True)
# st.stop()

# Convert the Snowpark Dataframe to a Pandas Dataframe so we can use the LOC function
pd_df=my_dataframe.to_pandas()
st.dataframe(pd_df)
st.stop()


ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:', my_dataframe,
    max_selections = 5
)

if ingredients_list:
    # st.write(ingredients_list)
    # st.text(ingredients_list)

    ingredients_string = ''
    
    for x in ingredients_list:
        ingredients_string += x + ' '
        st.subheader(x + 'Nutrition Information')
        fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+x)
        fv_df = st.dataframe(data=fruityvice_response.json(),use_container_width=True)


    st.write(ingredients_string)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
            values ('""" + ingredients_string + """','""" + name_on_order + """')"""

    time_to_insert = st.button('Submit Order')
    # st.write(my_insert_stmt)
    # st.stop()

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success(f'Your Smoothie is ordered! {name_on_order}', icon="✅")

