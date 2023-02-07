import sdmx
import plotly.express as px
import plotly.graph_objects as go 
import pandas as pd
import traceback
import os
from datetime import datetime

from helperFunctions import log_stats


class BBKClientClass():
    def __init__(self):
        self.ecb = sdmx.Client("BBK")
        
        self.folder_name = "output"
        self.save_dir = os.path.isdir(self.folder_name)
        self.current_dir = os.getcwd()

        if not self.save_dir:
            os.makedirs(self.folder_name)
            print(f'Created folder {self.current_dir}/{self.folder_name}')
            

    def get_euribor_data(self, startPeriod="1980-01-01", endPeriod="2099-12-31", short_term='3M', long_term=None, spread=None):
        
        
        try:
            startPeriod = datetime.strptime(startPeriod,'%Y-%m-%d')
            endPeriod = datetime.strptime(endPeriod,'%Y-%m-%d')
            
            frequency_key_map = {
                '1W': 'ST0307',
                '1M': 'ST0310',
                '3M': 'ST0316',
                '6M': 'ST0325',
                '9M': 'ST0334',
                '12M': 'ST0343'
            }

            if long_term == '10Y':
                long_term = None
            
                
            if (short_term or long_term) not in frequency_key_map:
                
                raise Exception(f"Invalid short term: {short_term}. Valid values are: {frequency_key_map.keys()}")

            else:
                key = frequency_key_map[short_term]

                data = self.ecb.data("BBK01", key=key).data[0]
                df = sdmx.to_pandas(data, datetime="TIME_PERIOD")
                df = df.rename(columns={key: f'EURIBOR{short_term}'})

                df = df[(df.index >= startPeriod) & (df.index <= endPeriod)]

                df = df.dropna()

                begin_date = df.index[-1].strftime('%Y-%m-%d')
                end_date = df.index[12].strftime('%Y-%m-%d')

                if not long_term:
                    
                    fig = px.line(df, x=df.index, y=f'EURIBOR{short_term}')
                    fig.update_layout(template='plotly_white', width=600, height=600, title_x=0.5, hovermode="x unified")
                    fig.update_layout(
                    title=go.layout.Title(
                        text=f"<b>{short_term} Euribor</b><br><sup>{end_date} - {begin_date}</sup>",
                        xref="paper",
                        x=0.5
                    ),
                    yaxis=go.layout.YAxis(
                    title=go.layout.yaxis.Title(
                        text='Percent'
                        )
                    ),
                    xaxis=go.layout.XAxis(
                    title=go.layout.xaxis.Title(
                        text='Period'
                            )
                        )
                    )
                
                    fig.show()
                    
                else:
                    key = frequency_key_map[long_term]

                    data_long_term = self.ecb.data("BBK01", key=key).data[0]
                    df_long_term = sdmx.to_pandas(data_long_term, datetime="TIME_PERIOD")
                    df_long_term = df_long_term.rename(columns={key: f'EURIBOR{long_term}'})
                    df_long_term = df_long_term[(df_long_term.index >= startPeriod) & (df_long_term.index <= endPeriod)]

                    df_long_term = df_long_term.dropna()
                    
                    df = pd.concat([df, df_long_term], axis=1)
                    
                    if spread:
                        df['spread'] = df[f'EURIBOR{long_term}'] - df[f'EURIBOR{short_term}']
                        fig = px.line(df, x=df.index, y=['spread'])
                        fig.update_layout(template='plotly_white', width=600, height=600, title_x=0.5, hovermode="x unified")
                        fig.update_layout(
                        title=go.layout.Title(
                            text=f"<b>Euribor spread ({long_term}-{short_term})</b><br><sup>{end_date} - {begin_date}</sup>",
                            xref="paper",
                            x=0.5
                        ),
                        yaxis=go.layout.YAxis(
                        title=go.layout.yaxis.Title(
                            text='Percent'
                            )
                        ),
                        xaxis=go.layout.XAxis(
                        title=go.layout.xaxis.Title(
                            text='Period'
                                )
                            )
                        )
                        
                    else:
                        fig = px.line(df, x=df.index, y=[f'EURIBOR{short_term}', f'EURIBOR{long_term}'])
                        fig.update_layout(template='plotly_white', width=600, height=600, title_x=0.5, hovermode="x unified")
                        fig.update_layout(
                        title=go.layout.Title(
                            text=f"<b>Euribor rates</b><br><sup>{end_date} - {begin_date}</sup>",
                            xref="paper",
                            x=0.5
                        ),
                        yaxis=go.layout.YAxis(
                        title=go.layout.yaxis.Title(
                            text='Percent'
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

                    print(f'{self.current_dir}/{self.folder_name}/EURIBOR{short_term}_{long_term}_spread-{spread}_{begin_date}-{end_date}.png')
                        
                    fig.write_image(f"{self.current_dir}/{self.folder_name}/EURIBOR{short_term}_{long_term}_spread-{spread}_{begin_date}-{end_date}.png")
                    fig.write_html(f"{self.current_dir}/{self.folder_name}/EURIBOR{short_term}_{long_term}_spread-{spread}_{begin_date}-{end_date}.html")
                    df.to_csv(f"{self.current_dir}/{self.folder_name}/EURIBOR{short_term}_{long_term}_spread-{spread}_{begin_date}-{end_date}.csv", index=True)
                    print(f"Image saved to {self.current_dir}/{self.folder_name}.")
                
                return df
    
        except Exception as e:
            
            error_msg = f"Unexpected Error: {e}\nTraceback: {traceback.format_exc()}"
            print(error_msg)
            
            return error_msg


    def get_eonia_data(self, startPeriod="2021-01-01", endPeriod="2022-12-31"):
        """
        The Euro Short-Term Rate (€STR) published by the European Central Bank is determined as a substitute interest rate for the Euro Overnight Index Average (EONIA). Since October 2, 2019, the EONIA has been calculated as €STR + 8.5bp.) 
        This function takes EONIA history until last day (2021-12-31) and continues with up-to-date €STR data.
        """
        
        try: 
            

            
            startPeriod = datetime.strptime(startPeriod,'%Y-%m-%d')
            endPeriod = datetime.strptime(endPeriod,'%Y-%m-%d')
            
            eonia_key = 'ST0304'
            eonia_data = self.ecb.data("BBK01", key=eonia_key).data[0]
            eonia_df = sdmx.to_pandas(eonia_data, datetime="TIME_PERIOD")
            eonia_df = eonia_df.rename(columns={eonia_key: f'EONIA'})
            eonia_df = eonia_df.dropna()
            print(eonia_df)
            
            estr_key = 'D.EU000A2X2A25.WT' 
            estr_data = self.ecb.data("BBMMB", key=estr_key).data[0]
            estr_df = sdmx.to_pandas(estr_data, datetime="TIME_PERIOD")
            estr_df = estr_df.dropna()
        
            index_list_estr_data = []
            for index, _ in estr_df.iterrows():
                index_list_estr_data.append(index)

            value_list_estr_data = []
            for _, value in estr_df.iterrows():
                for i in value:
                    value_list_estr_data.append(i)

            estr_df = pd.DataFrame(value_list_estr_data, index=index_list_estr_data, columns=['ESTR'])

            eonia_df = eonia_df.join(estr_df, how='outer').fillna(0)           
            eonia_df['EONIA_ESTR'] = eonia_df['EONIA'] + (eonia_df['ESTR'])
            df = eonia_df.drop(['EONIA', 'ESTR'], axis=1)
            df = df[(df.index >= startPeriod) & (df.index <= endPeriod)]
        
            begin_date = df.index[-1].strftime('%Y-%m-%d')
            end_date = df.index[0].strftime('%Y-%m-%d')
            
            fig = px.line(df, x=df.index, y=f'EONIA_ESTR')
            fig.update_layout(template='plotly_white', width=600, height=600, title_x=0.5, hovermode="x unified")
            fig.update_layout(
            title=go.layout.Title(
                text=f"<b>EONIA / €STR</b><br><sup>{end_date} - {begin_date} / €STR-data since 2022-01-01</sup>",
                xref="paper",
                x=0.5
            ),
            yaxis=go.layout.YAxis(
            title=go.layout.yaxis.Title(
                text='Percent'
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

                print(f'{self.current_dir}/{self.folder_name}/EONIA_{begin_date}-{end_date}.png')
                    
                fig.write_image(f"{self.current_dir}/{self.folder_name}/EONIA_{begin_date}-{end_date}.png")
                fig.write_html(f"{self.current_dir}/{self.folder_name}/EONIA_{begin_date}-{end_date}.html")
                df.to_csv(f"{self.current_dir}/{self.folder_name}/EONIA_{begin_date}-{end_date}.csv", index=True)
                print(f"Image saved to {self.current_dir}/{self.folder_name}.")
            
            return df
            
            

        except Exception as e:
            
            error_msg = f"Unexpected Error: {e}\nTraceback: {traceback.format_exc()}"
            print(error_msg)
            
            return error_msg



if __name__ == '__main__':
    bbkClient = BBKClientClass()
    bbkClient.get_euribor_data(long_term='9M', spread=True)
    #bbkClient.get_eonia_data()