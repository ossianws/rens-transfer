# PIE CHART – TtoR Distribution
#This file is just a list of functions which generate graphs.
#They are used in app restart to regenerate

import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import os




def visualpie(df: pd.DataFrame) -> go.Figure:
    counts = df.groupby('TtoR')['Organisation'].count().reset_index()
    counts.columns = ['TtoR', 'Organisation_Count']

    fig = go.Figure(
        go.Pie(
            labels=counts['TtoR'],
            values=counts['Organisation_Count'],
            hoverinfo='label+percent'
        )
    )
    fig.update_layout(title="Number of Organisations by TtoR")
    return fig


# HEATMAP – TtoR × Variety
def visualheatmap(df: pd.DataFrame) -> go.Figure:
    counts = df.groupby(['TtoR', 'Variety'])['Organisation'].count().reset_index()
    table = counts.pivot(index='TtoR', columns='Variety', values='Organisation').fillna(0)

    fig = go.Figure(
        go.Heatmap(
            z=table.values,
            x=table.columns,
            y=table.index,
            colorscale='Blues'
        )
    )
    fig.update_layout(title='Organisations by TtoR & Variety')
    return fig


# HEATMAP – TtoR × Area of Operation
def visualheatmap2(df: pd.DataFrame) -> go.Figure:
    counts = df.groupby(['TtoR', 'Area of Operation'])['Organisation'].count().reset_index()
    table = counts.pivot(index='TtoR', columns='Area of Operation', values='Organisation').fillna(0)

    fig = go.Figure(
        go.Heatmap(
            z=table.values,
            x=table.columns,
            y=table.index,
            colorscale='Blues'
        )
    )
    fig.update_layout(title='Organisations by TtoR & Area of Operation')
    return fig


# STACKED BAR – Regularity × Focus
def visualstackbar(df: pd.DataFrame) -> go.Figure:
    counts = df.groupby(['Regularity', 'Focus'])['Organisation'].count().reset_index()
    
    fig = go.Figure()
    for focus in counts['Focus'].unique():
        sub = counts[counts['Focus'] == focus]
        fig.add_trace(go.Bar(x=sub['Regularity'], y=sub['Organisation'], name=focus))

    fig.update_layout(title="Organisations vs Regularity (Focus)", barmode='stack')
    return fig


# STACKED BAR – Regularity × Type
def visualstackbar2(df: pd.DataFrame) -> go.Figure:
    counts = df.groupby(['Regularity', 'Type'])['Organisation'].count().reset_index()
    
    fig = go.Figure()
    for t in counts['Type'].unique():
        sub = counts[counts['Type'] == t]
        fig.add_trace(go.Bar(x=sub['Regularity'], y=sub['Organisation'], name=t))

    fig.update_layout(title="Organisations vs Regularity (Type)", barmode='stack')
    return fig


# BAR CHART – Regularity Count
def visualbar(df: pd.DataFrame) -> go.Figure:
    counts = df.groupby('Regularity')['Organisation'].count().reset_index()

    fig = go.Figure(go.Bar(x=counts['Regularity'], y=counts['Organisation']))
    fig.update_layout(title="Organisations by Regularity")
    return fig


# HEATMAP – Priorities × Regularity
def visualheatmap3(df: pd.DataFrame) -> go.Figure:
    cols = ["Organisation", "Regularity", "EQ", "RJ", "CU", "CJ", "SO", "SJ", "CE", "SC"]

    df_bin = df[cols].copy()
    priority_cols = df_bin.columns[2:]
    df_bin[priority_cols] = df_bin[priority_cols].eq("Y").astype(int)

    counts = df_bin.groupby("Regularity")[priority_cols].sum()

    fig = go.Figure(
        go.Heatmap(
            z=counts.values,
            x=counts.columns,
            y=counts.index,
            colorscale='Blues'
        )
    )
    fig.update_layout(title="Priorities by Regularity")
    return fig


# HEATMAP – Priorities × Variety
def visualheatmap4(df: pd.DataFrame) -> go.Figure:
    cols = ["Organisation", "Variety", "EQ", "RJ", "CU", "CJ", "SO", "SJ", "CE", "SC"]

    df_bin = df[cols].copy()
    priority_cols = df_bin.columns[2:]
    df_bin[priority_cols] = df_bin[priority_cols].eq("Y").astype(int)

    counts = df_bin.groupby("Variety")[priority_cols].sum()

    fig = go.Figure(
        go.Heatmap(
            z=counts.values,
            x=counts.columns,
            y=counts.index,
            colorscale='Blues'
        )
    )
    fig.update_layout(title="Priorities by Variety")
    return fig