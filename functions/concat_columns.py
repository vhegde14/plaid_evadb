import pandas as pd

from evadb.catalog.catalog_type import ColumnType, NdArrayType
from evadb.functions.abstract.abstract_function import AbstractFunction
from evadb.functions.decorators.decorators import forward, setup
from evadb.functions.decorators.io_descriptors.data_types import PandasDataframe

class ConcatColumns(AbstractFunction):
    """
    Arguments:
        None

    Input Signatures:
        input_dataframe (DataFrame) : A DataFrame containing 2 or more columns

    Output Signatures:
        output_dataframe (DataFrame) : A DataFrame containing one columns.

    Example Usage:
        You can use this function to cocatenate multiple columnds into just one, barring the id column.

        input_dataframe = [id: John][Age: 30][Country: USA]
        output_dataframe = [id: John][Age: 30, Country: USA]
    """
    @property
    def name(self) -> str:
        return "ConcatColumns"
    
    @setup(cacheable=False)
    def setup(self) -> None:
        # Any setup or initialization can be done here if needed
        pass
    
    @forward(
        input_signatures=[
            PandasDataframe(
                columns=["transactions.id", "transactions.amount", "transactions.category", "transactions.date", "transactions.merchant_name"],
                column_types=[NdArrayType.STR, NdArrayType.FLOAT32, NdArrayType.STR, NdArrayType.STR, NdArrayType.STR],
                column_shapes=[(None,), (None,), (None,), (None,), (None,)],
            )
        ],
        output_signatures=[
            PandasDataframe(
                columns=["ids", "summaries"],
                column_types=[NdArrayType.STR, NdArrayType.STR],
                column_shapes=[(None,), (None,)],
            )
        ],
    )
    def forward(self, input_df):
        # Ensure input is provided
        if input_df.empty or input_df.iloc[0] is None:
            raise ValueError("Input DF must be provided.")

        # Initialize lists for columns
        values_list = []
        output_dataframe = pd.DataFrame()

        # Iterate over rows of the input DataFrame
        for _, row in input_df.iterrows():
            # Get values for this row
            id = row['id']
            amount = row['amount']
            category = row['category']
            date = row['date']
            merchant_name = row['merchant_name']
            
            # Initialize lists for columns in this row
            values = []
            values.append(id)
            values.append(f'Spent ${amount} on the date {date} for {merchant_name} (category: {category})')
            summary_string = f'Spent ${amount} on the date {date} for {merchant_name} (category: {category})'
            values_list.append(
                {"ids": id, "summaries": summary_string}
            )

        # Create a DataFrame from the parsed data
        output_dataframe = pd.DataFrame(values_list, columns=['ids', 'summaries'])

        return output_dataframe