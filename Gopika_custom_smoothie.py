# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
import requests
import pandas as pd

name_on_order = st.text_input("Name on order:")

# Write directly to the app
st.title(f"Example Streamlit App :balloon: {st.__version__}")
st.write(
  """Replace this example with your own code!
  **And if you're new to Streamlit,** check
  out our easy-to-follow guides at
  [docs.streamlit.io](https://docs.streamlit.io).
  """
)

# Get the current credentials
cnx = st.connection("snowflake")
session = cnx.session()

my_dataframe = session.table("smoothies.public.fruit_options").select(
    col("FRUIT_NAME"),
    col("SEARCH_ON")
)

# Convert the Snowpark DataFrame to a Pandas DataFrame
# so we can use the loc function
pd_df = my_dataframe.to_pandas()

ingredients_list = st.multiselect(
    "Choose up to 5 ingredients:",
    my_dataframe,
    max_selections=5
)

if ingredients_list:
    ingredients_string = ''

    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '

        search_on = pd_df.loc[
            pd_df['FRUIT_NAME'] == fruit_chosen,
            'SEARCH_ON'
        ].iloc[0]

        st.write(
            'The search value for ',
            fruit_chosen,
            ' is ',
            search_on,
            '.'
        )

        st.subheader(fruit_chosen + ' Nutrition Information')

        fruitvice_response = requests.get(
    "https://www.fruityvice.com/api/fruit/" + search_on
)

        st.dataframe(
            data=fruitvice_response.json(),
            use_container_width=True
        )

    st.write("Your ingredients:")
    st.text(ingredients_string)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
                      values ('""" + ingredients_string + """','""" + name_on_order + """')"""

    st.write(my_insert_stmt)

    submit = st.button("Submit Order")

    if submit:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")

# Use an interactive slider to get user input
hifives_val = st.slider(
  "Number of high-fives in Q3",
  min_value=0,
  max_value=90,
  value=60,
  help="Use this to enter the number of high-fives you gave in Q3",
)

# Create an example dataframe
created_dataframe = session.create_dataframe(
  [[50, 25, "Q1"], [20, 35, "Q2"], [hifives_val, 30, "Q3"]],
  schema=["HIGH_FIVES", "FIST_BUMPS", "QUARTER"],
)

# Execute the query and convert it into a Pandas dataframe
queried_data = created_dataframe.to_pandas()

# Create a simple bar chart
st.subheader("Number of high-fives")
st.bar_chart(data=queried_data, x="QUARTER", y="HIGH_FIVES")

st.subheader("Underlying data")
st.dataframe(queried_data, use_container_width=True)
