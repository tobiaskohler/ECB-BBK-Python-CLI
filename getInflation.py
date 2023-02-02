import sdmx
import plotly.express as px
import plotly.graph_objects as go 
import pandas as pd
import traceback
import os

    
def get_inflation_data(startPeriod="1980-01", endPeriod="2099-12", save=False) -> pd.DataFrame:
    
    try:
        #ICP (Inflation Rates)
        ecb = sdmx.Client("ECB")

        exr_msg = ecb.dataflow("ICP")
        #exr_flow = exr_msg.dataflow.ICP
        
        params = dict(startPeriod=startPeriod, endPeriod=endPeriod)
        key = dict(ICP_ITEM="000000", FREQ="M", REF_AREA='U2', ICP_SUFFIX='INX', ADJUSTMENT='Y')

        data = ecb.data("ICP", key=key, params=params).data[0]
        df = sdmx.to_pandas(data, datetime="TIME_PERIOD")
        
        index_list = []
        for index, row in df.iterrows():
            index_list.append(index)

        value_list = []
        for index, value in df.iterrows():
            for i in value:
                value_list.append(i)
        
        inflation_index = pd.DataFrame(value_list, index=index_list, columns=['HICP'])
        inflation_index['HICP_ann_delta'] = inflation_index['HICP'].pct_change(12)*100
        inflation_index['HICP_ann_delta'] = inflation_index['HICP_ann_delta'].dropna()
        begin_date = inflation_index.index[-1].strftime('%Y-%m-%d')
        end_date = inflation_index.index[0].strftime('%Y-%m-%d')

        fig = px.line(inflation_index, x=inflation_index.index, y='HICP_ann_delta')
        fig.update_layout(template='plotly_white', width=600, height=600, title_x=0.5, hovermode="x unified")
        fig.update_layout(
        title=go.layout.Title(
            text=f"<b>Eurozone: Inflation rate</b><br><sup>{begin_date} - {end_date}</sup>",
            xref="paper",
            x=0.5
        ),
        yaxis=go.layout.YAxis(
        title=go.layout.yaxis.Title(
            text='Year-on-year inflation rate (%)'
            )
        ),
        xaxis=go.layout.XAxis(
        title=go.layout.xaxis.Title(
            text='Period'
            )
        )
    )

        fig.show()
        
        if save:

            folder_name = "output"
            save_dir = os.path.isdir(folder_name)
            current_dir = os.getcwd()
            print(f'{current_dir}/{folder_name}/HICP_Eurozone_{begin_date}-{end_date}.png')

            if not save_dir:
                os.makedirs(folder_name)
                
            fig.write_image(f"{current_dir}/{folder_name}/HICP_Eurozone_{begin_date}-{end_date}.png")
            fig.write_html(f"{current_dir}/{folder_name}/HICP_Eurozone_{begin_date}-{end_date}.html")
            print(f"Image saved to {current_dir}/{folder_name}.")
        
        return inflation_index
    
    except Exception as e:
        error_msg = f"Unexpected Error: {e}\nTraceback: {traceback.format_exc()}"
        print(error_msg)
        
        return error_msg

    
if __name__ == '__main__':
    
    get_inflation_data(save=True)