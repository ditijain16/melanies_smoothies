# # Import python packages
# import streamlit as st
# import pandas as pd
# from snowflake.snowpark.functions import col
# import requests

# # Write directly to the app
# st.title(f":cup_with_straw: Customize your smoothie! :cup_with_straw: ")
# st.write(
#   """Choose the fruits you want in your smoothie!
#   """
# )

# name_on_order = st.text_input('Name on smoothie: ')
# st.write('The name on your smoothie will be: ', name_on_order)

# cnx = st.connection('snowflake')
# session = cnx.session()
# my_dataframe = session.table("smoothies.public.fruit_options").select(col('fruit_name'), col('search_on'))
# pd_df = my_dataframe.to_pandas()
# st.dataframe(pd_df)
# st.stop()

# ingredient_list = st.multiselect(
#     'Choose upto 5 ingredients:',
#     my_dataframe,
#     max_selections = 5
# )


# if ingredients_list:
#     ingredients_string = ''

#     for fruit_chosen in ingredients_list:
#         ingredients_string += fruit_chosen + ' '

#         search_on = pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
#         # st.write('The search value for ', fruit_chosen, ' is ', search_on, '.')

#         st.subheader(fruit_chosen + ' Nutrition Information')
#         fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + search_on)
#         fv_df = st.dataframe(data=fruityvice_response.json(), use_container_width=True)

#     # st.write(ingredients_string)
  
#     my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
#             values ('""" + ingredient_string + """', '""" + name_on_order + """')"""
#     time_to_insert = st.button('Submit Order')
#     if time_to_insert:
#         session.sql(my_insert_stmt).collect()
#         st.success('Your Smoothie is ordered!', icon="✅")
  

# Import python packages
import streamlit as st
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col

# Write directly to the app
st.title("🥛Customize Your Smoothie!🥛")
st.write(
    "Choose the fruits you want in your custom Smoothie!"
)

# option = st.selectbox(
#     "How would you like to be contacted",
#     ('Email', 'Home phone', 'Mobile phone')
# )

# st.write('Your selected', option)

# fruit_option = st.selectbox(
#     "What is your favorite Fruit?",
#     ('Banana', 'Strawberries', 'Peaches')
# )

# st.write('Your Favorite Fruit is: ', fruit_option)

session = get_active_session()
# st.write(session)
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
# st.dataframe(data=my_dataframe, use_container_width=True)


name_on_order = st.text_input("Name on Smoothie:")
st.write("The name in your Smoothie will be: ", name_on_order)



# list data type
ingredients_list = st.multiselect(
 'Choose up to 5 ingredients: ',  my_dataframe, max_selections = 5
)


if ingredients_list:
    ingredients_string = ''
#     st.write("You selected:", ingredients_list)
#     st.text(ingredients_list)
    for element in ingredients_list:
        ingredients_string += element + ' '
    # st.write(ingredients_string)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
                values ('"""\
                + ingredients_string + """','""" + name_on_order + """'
                )"""
    # st.write(my_insert_stmt)
    # st.stop()
    
    time_to_insert = st.button('Submit Order')
        
    # st.write(my_insert_stmt)
    
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")



