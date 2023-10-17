import pandas as pd

from evadb.catalog.catalog_type import ColumnType, NdArrayType
from evadb.functions.abstract.abstract_function import AbstractFunction
from evadb.functions.decorators.decorators import forward, setup
from evadb.functions.decorators.io_descriptors.data_types import PandasDataframe

class Summarize(AbstractFunction):
    """
    Arguments:
        None

    Input Signatures:
        input_dataframe (DataFrame) : A DataFrame containing 1 column and many rows

    Output Signatures:
        output_dataframe (DataFrame) : A DataFrame containing 1 column and 1 row with each row appended to a list.

    Example Usage:
        You can use this function to cocatenate multiple rows into just one for a column.

    """
    @property
    def name(self) -> str:
        return "Summarize"
    
    @setup(cacheable=False)
    def setup(self) -> None:
        # Any setup or initialization can be done here if needed
        pass
    
    @forward(
        input_signatures=[
            PandasDataframe(
                columns=["summary_table.summaries"],
                column_types=[NdArrayType.STR],
                column_shapes=[(None,)],
            )
        ],
        output_signatures=[
            PandasDataframe(
                columns=["total_summary"],
                column_types=[NdArrayType.STR],
                column_shapes=[(None,)],
            )
        ],
    )
    def forward(self, input_df):
        # Ensure input is provided
        if input_df.empty or input_df.iloc[0] is None:
            raise ValueError("Input DF must be provided.")

        # Initialize lists for columns
        value_list = []

        # Iterate over rows of the input DataFrame
        for _, row in input_df.iterrows():
            # Get values for this row
            string = row['summaries']
            
            value_list.append(string)

        rows = [str(value_list)]
        # Create a DataFrame from the parsed data
        output_dataframe = pd.DataFrame(rows, columns=['total_summary'])

        return output_dataframe