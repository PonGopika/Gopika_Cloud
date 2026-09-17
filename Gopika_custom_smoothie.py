# Import python packages
import streamlit as st
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col


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
session = get_active_session()

my_dataframe = session.table("smoothies.public.fruit_options").select(col("FRUIT_NAME"))

# st.dataframe(data=my_dataframe, use_container_width=True)

ingredients = st.multiselect(
  "Choose up to 5 ingredients:",
  my_dataframe,
)

if ingredients:
  ingredients_string = ""

  for fruit_chosen in ingredients:
    ingredients_string += fruit_chosen

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
