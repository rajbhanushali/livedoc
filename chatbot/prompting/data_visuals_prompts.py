data_visuals_prompt_text = """
Using the table response, you are now responsible for determining the appropriate visualization for the following basketball data, given the user's query.  

Evaluate whether the data should be visualized at all.

For a question like "Which players meet [THRESHOLD T] for [STATISTIC S]?" 
I want you to set the "x" to be the Player Name, and I want you to set Y to be the statistic itself. 
You may see multiple columns in the table that are not correspondending to the user's request. In that case, just pick the column that does correspond and place it as x or y axis based on the best way to visualize this.

If there's a lot of variety and large quantity of data points (rows), then use a scatter plot instead of a bar chart.
Bar chart should only be used if there's categorical x-axes like wins and losses as x axis values. Otherwise mostly Scatter Plot.
ONE ROW : If there's only one row, set {"requires_visual" = false} for now.

DO NOT FORGET: 
Always make sure to set the names of axes match to columns in the table_data, precisely with Caps and all characters considered. Otherwise, visualizing the table data will fail.
ALWAYS return your answer in JSON format only. No text or description before or after the JSON. Make sure all keys and values are in quotes so it's JSON valid.

MVQ Prompting:
For instance if the user query is 
"Who shot above 40 percent from 3?" The x should be the column in table-data that corresponds to player name, and the Y-axis should be "3PT%" 

Choosing the type of Plot:
If a question is pertaining to time / months / days / points in events / trends, choose a line graph.

If you determine that the data cannot be visualized or it is unclear, return:
{"requires_visuals": false, "description": [your reasoning for not needing visuals]}. Return only JSON, no other text or description!!

If you determine visualization is possible, this json format is the exact response you should save. Make sure no brackets in your answer, only strings as keys and values.
Please specify within the JSON response which type of chart, the columns for the x and y axes, and a description of the chart:
{
    "requires_visuals": true,
    "type": "[BAR, SCATTER, or LINE]",
    "x": "[the column name for data to be displayed on the x axis]",
    "y": "[the column name for data to be displayed on the y axis]",
    "description": [Describing the chart to make it easy to interpret for the user]
}

Now feed those into the custom function plot_dataviz.
"""

{
  "name": "plot_dataviz",
  "description": "Use this function to plot the table response from the database",
  "parameters": {
    "type": "object",
    "properties": {
      "requires_visual": {
        "type": "boolean",
        "description": "Whether or not a visual is even required"
      },
      "x-axis": {
        "type": "string",
        "description": "column name for the x axis, must match table_response columns"
      },
      "y-axis": {
        "type": "string",
        "description": "column name for the y axis, must match table_response columns"
      },
      "type": {
        "type": "string",
        "description": "which type of plot to use between bar, scatter, or line"
      },
      "description": {
        "type": "string",
        "description": "chart description describing to the user what they're looking at"
      },
      "table_response": {
          "type": "string",
          "description": "json of the table_response from the run_conn_query_sql output."
      }
    },
    "required": [
      "x-axis",
      "y-axis",
      "type",
      "description"
    ]
  }
}
