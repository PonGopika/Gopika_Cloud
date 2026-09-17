# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col, when_matched

# Get the current credentials
cnx = st.connection("snowflake")
session = cnx.session()

my_dataframe = session.table("smoothies.public.orders") \
    .filter(col("ORDER_FILLED") == 0) \
    .collect()

if len(my_dataframe) > 0:

    editable_df = st.data_editor(my_dataframe)

    submit = st.button("Submit Changes")

    if submit:
        og_dataset = session.table("smoothies.public.orders")
        edited_dataset = session.create_dataframe(editable_df)

        merge_result = og_dataset.merge(
            edited_dataset,
            (og_dataset["ORDER_UID"] == edited_dataset["ORDER_UID"]),
            [when_matched().update(
                {"ORDER_FILLED": edited_dataset["ORDER_FILLED"]}
            )]
        )

        if merge_result:
            st.success("Changes saved!", icon="👍")

else:
    st.write("No pending orders.")
