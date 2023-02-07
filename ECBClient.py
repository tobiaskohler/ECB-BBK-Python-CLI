import sdmx
import plotly.express as px
import plotly.graph_objects as go 
import pandas as pd
import traceback
import os

from helperFunctions import log_stats
#test

class ECBClientClass():
    def __init__(self):
        self.ecb = sdmx.Client("ECB")
        
        self.folder_name = "output"
        self.save_dir = os.path.isdir(self.folder_name)
        self.current_dir = os.getcwd()

        if not self.save_dir:
            os.makedirs(self.folder_name)
            print(f'Created folder {self.current_dir}/{self.folder_name}')


    @log_stats
    def get_inflation_data(self, startPeriod="1980-01", endPeriod="2099-12", save=False) -> pd.DataFrame:
        
        try:
            
            params = dict(startPeriod=startPeriod, endPeriod=endPeriod)
            key = dict(ICP_ITEM="000000", FREQ="M", REF_AREA='U2', ICP_SUFFIX='INX', ADJUSTMENT='Y')
            data = self.ecb.data("ICP", key=key, params=params).data[0]
            
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
            end_date = inflation_index.index[12].strftime('%Y-%m-%d')

            fig = px.line(inflation_index, x=inflation_index.index, y='HICP_ann_delta')
            fig.update_layout(template='plotly_white', width=600, height=600, title_x=0.5, hovermode="x unified")
            fig.update_layout(
            title=go.layout.Title(
                text=f"<b>Eurozone: Inflation rate</b><br><sup>{end_date} - {begin_date}</sup>",
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
            
            save = input("Save output to the current folder? (y/n)")        

            if save.lower() == 'y':    

                print(f'{self.current_dir}/{self.folder_name}/HICP_Eurozone_{begin_date}-{end_date}.png')
                    
                fig.write_image(f"{self.current_dir}/{self.folder_name}/HICP_Eurozone_{begin_date}-{end_date}.png")
                fig.write_html(f"{self.current_dir}/{self.folder_name}/HICP_Eurozone_{begin_date}-{end_date}.html")
                inflation_index.to_csv(f"{self.current_dir}/{self.folder_name}/HICP_Eurozone_{begin_date}-{end_date}.csv", index=True)
                print(f"Image saved to {self.current_dir}/{self.folder_name}.")
            
            return inflation_index
        
        except Exception as e:
            
            error_msg = f"Unexpected Error: {e}\nTraceback: {traceback.format_exc()}"
            print(error_msg)
            
            return error_msg

       
    @log_stats
    def get_yield_data(self, spread=False, startPeriod="1980-01", endPeriod="2099-12", short_term="2Y", long_term="10Y", save=False) -> pd.DataFrame:

        
        try:
            
            supported_shortterm = ['3M', '6M', '9M', '1Y', '2Y']
            supported_longterm = ['5Y','10Y', '15Y', '20Y', '30Y']
            
            if short_term not in supported_shortterm:
                    raise Exception(f"Invalid short term: {short_term}. Valid values are: {supported_shortterm}")
            if long_term not in supported_longterm:
                    raise Exception(f"Invalid long term: {long_term}. Valid values are: {supported_longterm}")
            
            params = dict(startPeriod=startPeriod, endPeriod=endPeriod)
            short_term_key = dict(REF_AREA='U2', INSTRUMENT_FM='G_N_A', DATA_TYPE_FM=f'SR_{short_term}')
            long_term_key = dict(REF_AREA='U2', INSTRUMENT_FM='G_N_A', DATA_TYPE_FM=f'SR_{long_term}')

            short_term_data = self.ecb.data("YC", key=short_term_key, params=params).data[0]
            df_short_term_data = sdmx.to_pandas(short_term_data, datetime="TIME_PERIOD")
            
            long_term_data = self.ecb.data("YC", key=long_term_key, params=params).data[0]
            df_long_term_data = sdmx.to_pandas(long_term_data, datetime="TIME_PERIOD")


            ## Short Term Yield
            index_list_short_term_data = []
            for index, _ in df_short_term_data.iterrows():
                index_list_short_term_data.append(index)

            value_list_short_term_data = []
            for _, value in df_short_term_data.iterrows():
                for i in value:
                    value_list_short_term_data.append(i)
            
            short_term_yield_df = pd.DataFrame(value_list_short_term_data, index=index_list_short_term_data, columns=[f'{short_term}'])
            short_term_yield_df[f'{short_term}'] = short_term_yield_df[f'{short_term}'].dropna()
            begin_date = short_term_yield_df.index[-1].strftime('%Y-%m-%d')
            end_date = short_term_yield_df.index[0].strftime('%Y-%m-%d')
            
            
            ## Long Term Yield
            index_list_long_term_data = []
            for index, _ in df_long_term_data.iterrows():
                index_list_long_term_data.append(index)

            value_list_long_term_data = []
            for _, value in df_long_term_data.iterrows():
                for i in value:
                    value_list_long_term_data.append(i)
            
            long_term_yield_df = pd.DataFrame(value_list_long_term_data, index=index_list_long_term_data, columns=[f'{long_term}'])
            long_term_yield_df[f'{long_term}'] = long_term_yield_df[f'{long_term}'].dropna()
            begin_date = long_term_yield_df.index[-1].strftime('%Y-%m-%d')
            end_date = long_term_yield_df.index[0].strftime('%Y-%m-%d')

            yield_df = pd.concat([short_term_yield_df, long_term_yield_df], axis=1)
            
            if spread:
                yield_df['spread'] = yield_df[f'{long_term}'] - yield_df[f'{short_term}']
            
            if not spread:

                fig = px.line(yield_df, x=yield_df.index, y=[f'{short_term}', f'{long_term}'], labels={'value': 'Yield in %', 'index': 'Period'})

                fig.update_layout(template='plotly_white', width=600, height=600, title_x=0.5, hovermode="x unified")
                
                fig.update_layout(
                    legend_title="Maturity",

                    title=go.layout.Title(
                        text=f"<b>Eurozone: Yield curve (spot rate)</b><br><sup>{end_date} - {begin_date}</sup>",
                        xref="paper",
                        x=0.5
                    ),
                    yaxis=go.layout.YAxis(
                    title=go.layout.yaxis.Title(
                        text='Yield in %'
                        )
                    ),
                    xaxis=go.layout.XAxis(
                    title=go.layout.xaxis.Title(
                        text='Period'
                        )
                    )
                )
            
            else:
                fig = px.line(yield_df, x=yield_df.index, y=['spread'], labels={'value': 'Yield spread in %', 'index': 'Period'})

                fig.update_layout(template='plotly_white', width=600, height=600, title_x=0.5, hovermode="x unified")

                fig.update_layout(
                    legend_title=f"{long_term} minus {short_term}",

                    title=go.layout.Title(
                        text=f"<b>Eurozone: Yield spread (spot rate)</b><br><sup>{end_date} - {begin_date}</sup>",
                        xref="paper",
                        x=0.5
                    ),
                    yaxis=go.layout.YAxis(
                    title=go.layout.yaxis.Title(
                        text='Yield in %'
                        )
                    ),
                    xaxis=go.layout.XAxis(
                    title=go.layout.xaxis.Title(
                        text='Period'
                        )
                    )
                )

            fig.show()
            
            save = input("Save output to the current folder? (y/n)")        
                
            if save.lower() == 'y':    
                    
                fig.write_image(f"{self.current_dir}/{self.folder_name}/Yield_curve_{short_term}{long_term}_{begin_date}-{end_date}_spread-{spread}.png")
                fig.write_html(f"{self.current_dir}/{self.folder_name}/Yield_curve_{short_term}{long_term}_{begin_date}-{end_date}_spread-{spread}.html")
                yield_df.to_csv(f"{self.current_dir}/{self.folder_name}/Yield_curve_{short_term}{long_term}_{begin_date}-{end_date}_spread-{spread}.csv", index=True)
                print(f"Output saved to {self.current_dir}/{self.folder_name}.")
            
            return yield_df
        
        except Exception as e:
            
            error_msg = f"Unexpected Error: {e}\nTraceback: {traceback.format_exc()}"
            print(error_msg)
            
            return error_msg

        
    @log_stats
    def get_exchange_rate_data(self, fx='USD', startPeriod="2001-01", endPeriod="2023-12", save=False):
        
        try:
            params = dict(startPeriod=startPeriod, endPeriod=endPeriod)

            key = f'D.{fx}.EUR.SP00.A'
            
            fx_data = self.ecb.data("EXR", key=key, params=params).data[0]
            df_fx_data = sdmx.to_pandas(fx_data, datetime="TIME_PERIOD")
            
            begin_date = df_fx_data.index[0].strftime('%Y-%m-%d')
            end_date = df_fx_data.index[-1].strftime('%Y-%m-%d')
            
            index_list_fx_data = []
            for index, _ in df_fx_data.iterrows():
                index_list_fx_data.append(index)
            
            value_list_fx_data = []
            for _, value in df_fx_data.iterrows():
                for i in value:
                    value_list_fx_data.append(i)

                
            df_fx_data = pd.DataFrame(value_list_fx_data, index=index_list_fx_data, columns=[f'{fx}.EUR'])

            print(df_fx_data)
            
            fig = px.line(df_fx_data, x=df_fx_data.index, y=[f'{fx}.EUR'], labels={'value': f'(1 EUR costs .. {fx}', 'index': 'Period'})
            
            fig.update_layout(template='plotly_white', width=600, height=600, title_x=0.5, hovermode="x unified")
            
            fig.update_layout(template='plotly_white', width=600, height=600, title_x=0.5, hovermode="x unified", showlegend=False)

            fig.update_layout(
                legend_title=f"Currency Pair",

                title=go.layout.Title(
                    text=f"<b>EUR/{fx}</b><br><sup>{begin_date} - {end_date}</sup>",
                    xref="paper",
                    x=0.5
                ),
                yaxis=go.layout.YAxis(
                title=go.layout.yaxis.Title(
                    text=f'1 EUR costs .. {fx}'
                    )
                ),
                xaxis=go.layout.XAxis(
                title=go.layout.xaxis.Title(
                    text='Period'
                    )
                )
            )
            
            fig.show()

            save = input("Save output to the current folder? (y/n)")
            
            if save.lower() == 'y':
                
                fig.write_image(f"{self.current_dir}/{self.folder_name}/FX_{fx}_EUR_{begin_date}-{end_date}.png")
                fig.write_html(f"{self.current_dir}/{self.folder_name}/FX_{fx}_EUR_{begin_date}-{end_date}.html")
                df_fx_data.to_csv(f"{self.current_dir}/{self.folder_name}/FX_{fx}_EUR_{begin_date}-{end_date}.csv", index=True)
                print(f"Output saved to {self.current_dir}/{self.folder_name}.")
            
        except Exception as e:
                
            error_msg = f"Unexpected Error: {e}\nTraceback: {traceback.format_exc()}"
            print(error_msg)
            
            return error_msg

        
if __name__ == '__main__':
    
    ecbClient = ECBClientClass()
    
    #ecbClient.get_inflation_data(save=True)
    #ecbClient.get_yield_data(short_term='1Y', long_term='10Y')
    #ecbClient.get_exchange_rate_data(fx='CHF', startPeriod="2003-01", endPeriod="2017-12")
