import streamlit as st
import altair as alt
import plotly.express as px
import pandas as pd

def error_handle(message_object):
    if not message_object:
        return True
    
    if "chart_data" not in message_object:
        return True

    return False # No Error

# Render old existing charts from history
def create_and_display_chart(message_object):

    if error_handle(message_object):
        return

    table_data = message_object["results"]
    # mesasge_type = message_object["key"]

    # for debugging - save API calls
    chart_data = message_object.get("chart_data", {})

    if not chart_data:
        return 

    if "description" in chart_data:
        st.markdown(chart_data["description"])

    if chart_data.get('requires_visual') == False:
        st.text("No relevant visual generated. Ask me another question!")
        return

    if chart_data.get('requires_visual') == True:
        try: 
            plot_dataviz(chart_data, table_data)

        except Exception as e:
            error_text = (f'Could not produce visual because of error: {e}')
            st.caption(error_text)
            st.code("No Visualization Generated. See logs")

def plot_dataviz(data_viz_metadata, table_data):

    if data_viz_metadata.get('requires_visual') == False:
        st.text("No relevant visual generated. Ask me another question!")
        return {"description" : data_viz_metadata["description"]}
    
    requires_visual = data_viz_metadata["requires_visual"]
    properties = data_viz_metadata["properties"]
    plot_type = data_viz_metadata["plot_type"].upper()
    description = data_viz_metadata["description"]

    try: 
        # min_value = table_data[y_axis].min()
        # max_value = table_data[y_axis].max()
        # print("table data min max: ", min_value, max_value)

        if plot_type == 'BAR':
            axes = properties["axes"]
            x_axis = axes[0] # Always in position 0
            y_axis = axes[1] # Always in position 1

            # Take average of values instead of stacking multiple values onto each x
            numeric_columns = table_data.select_dtypes(include='number').columns
            table_data = table_data.groupby(x_axis)[numeric_columns].mean().reset_index()

            altair_source_chart = (
                alt.Chart(table_data).mark_bar().encode(
                    x=alt.X(x_axis, sort=alt.EncodingSortField(field=y_axis, order='ascending')),
                    y=alt.Y(y_axis)
                )
            )
            st.altair_chart(altair_source_chart, use_container_width=True)

        elif plot_type == 'LINE':
            axes = properties["axes"]
            x_axis = axes[0]
            y_axis = axes[1]
            hover_axes = axes

            altair_source_chart = (
                alt.Chart(table_data).mark_line().encode(
                    x=alt.X(x_axis, sort=alt.EncodingSortField(field=x_axis, order='ascending')),
                    y=alt.Y(y_axis),
                    tooltip=hover_axes
                )
            )
            st.altair_chart(altair_source_chart, use_container_width=True)

        elif plot_type == 'SCATTER':
            axes = properties["axes"]
            x_axis = axes[0]
            y_axis = axes[1]
            hover_axes = axes

            altair_source_chart = (
                alt.Chart(table_data).mark_circle().encode(
                    x=alt.X(x_axis, sort=alt.EncodingSortField(field=y_axis, order='ascending')),
                    y=alt.Y(y_axis),
                    tooltip=hover_axes,
                    color=alt.Color(hover_axes[0], legend=None)
                )
            )
            st.altair_chart(altair_source_chart, use_container_width=True)

        elif plot_type == "RADAR":

            player_col = properties["axes"][0]
            categories = properties["axes"][1:]
            table_data_grouped = table_data.groupby(player_col).mean().reset_index()

            table_data_long = pd.melt(table_data_grouped, id_vars=[player_col], 
                                      value_vars=categories, 
                                      var_name='Category', 
                                      value_name='Value')

            figure = px.line_polar(
                table_data_long, 
                r="Value",
                theta="Category",
                color=player_col,
                line_close=True,
                template="plotly_dark"
            )

            figure.update_polars(angularaxis_showgrid=False,
                radialaxis_gridwidth=0,
                gridshape='linear',
                bgcolor="#494b5a",
                radialaxis_showticklabels=False
            )

            st.plotly_chart(figure)

        else:
            st.code("Plot type was not understood. Please try again")

        # return chart data to store in messages
        return {
            "requires_visual": requires_visual,
            "properties": properties,
            "plot_type": plot_type,
            "description": description,
        }
    
    except Exception as e:
        error_text = f'Could not produce visual because of error: {e}'
        st.code("No Visualization Generated. See logs")
        print(error_text)
        return {
            "error": error_text
        }
