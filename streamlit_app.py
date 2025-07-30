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
import pandas as pd
from snowflake.snowpark.functions import col
import requests

# Title and instructions
st.title(":cup_with_straw: Customize your smoothie! :cup_with_straw:")
st.write("Choose the fruits you want in your smoothie!")

# Name input
name_on_order = st.text_input('Name on smoothie:')
st.write('The name on your smoothie will be:', name_on_order)

# Snowflake connection
cnx = st.connection('snowflake')
session = cnx.session()

# Get fruit options from Snowflake
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'), col('SEARCH_ON'))
pd_df = my_dataframe.to_pandas()

# Display fruit options
st.dataframe(pd_df)

# Convert the Pandas DF column to list for multiselect
fruit_names = pd_df['FRUIT_NAME'].tolist()

# Let user pick up to 5 fruits
ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:',
    options=fruit_names,
    max_selections=5
)

# Only proceed if ingredients selected
if ingredients_list:
    ingredients_string = ', '.join(ingredients_list)  # for inserting into DB

    for fruit_chosen in ingredients_list:
        st.subheader(f"{fruit_chosen} Nutrition Information")
        
        # Get the API search key from dataframe
        search_on = pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
        
        # Call fruityvice API
        fruityvice_response = requests.get(f"https://fruityvice.com/api/fruit/{search_on}")
        
        # Normalize and display response
        if fruityvice_response.status_code == 200:
            fv_df = pd.json_normalize(fruityvice_response.json())
            st.dataframe(fv_df, use_container_width=True)
        else:
            st.error(f"Failed to fetch data for {fruit_chosen}")

    # Insert smoothie order into Snowflake
    if st.button('Submit Order'):
        insert_stmt = f"""
            INSERT INTO smoothies.public.orders(ingredients, name_on_order)
            VALUES ('{ingredients_string}', '{name_on_order}')
        """
        session.sql(insert_stmt).collect()
        st.success("Your Smoothie is ordered! ✅")

