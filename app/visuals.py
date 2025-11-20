#This file is just a list of functions which generate graphs.
#They are used in app restart to regenerate

import pandas as pd
import plotly.graph_objects as go

def facebook(path):
    name = "facebook-followers"
    df=pd.read_csv(path)


    df["Followers 24"]=df["Followers 24"].fillna(0).astype(int)
    df["Followers 25"]=df["Followers 25"].fillna(0).astype(int)


    #standardization
    df["Category"]=(df["Category"].str.capitalize())

    fig = go.Figure(go.Bar(x=df["Category"],y=df["Followers 25"]))
    
    return fig.to_dict()


