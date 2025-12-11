#This file is just a list of functions which generate graphs.
#They are used in app restart to regenerate

import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import os
import numpy as np







    
def activity_count(df:pd.DataFrame)->go.Figure:

    # Parse dates (mixed formats allowed)
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')

    # Extract month name
    df['Month'] = df['Date'].dt.month_name()

    # Count number of activities per month
    monthly_counts = df['Month'].value_counts().reset_index()
    monthly_counts.columns = ['Month', 'ActivityCount']

    # Correct month order
    month_order = [
        "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"
    ]
    monthly_counts['Month'] = pd.Categorical(monthly_counts['Month'], categories=month_order, ordered=True)
    monthly_counts = monthly_counts.sort_values('Month')

    # Line chart
    fig = px.line(
        monthly_counts,
        x="Month",
        y="ActivityCount",
        markers=True,
        title="Monthly Activity Trend (2025)",
        
        template="plotly_white",
        color_discrete_sequence=["#1f77b4"]
    )

    fig.update_layout(
        xaxis_title="Month",
        yaxis_title="Number of Activities",
        hovermode="x unified"
    )

    return fig


def workstream_activities(df:pd.DataFrame)->go.Figure:
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')

    # Group activity counts
    ws_scale_counts = df.groupby(['Workstreams', 'Scale']).size().reset_index(name='Count')

    # Stacked bar with correct blue palette
    fig = px.bar(
        ws_scale_counts,
        x='Workstreams',
        y='Count',
        color='Scale',
        title='Activities by Workstream and Scale (2025)',
        barmode='stack',
        template='plotly_white',
        
        color_discrete_sequence=px.colors.sequential.Blues_r  # ✅ FIXED
    )

    fig.update_layout(
        xaxis_title="Workstream",
        yaxis_title="Number of Activities"
    )
    return fig


def type_output_bar(df:pd.DataFrame)->go.Figure:
    
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')

    # ---------------------------------------
    # 2. Group counts by Activity Type and Output
    # ---------------------------------------
    act_out_counts = (
        df.groupby(['Activity Type', 'Output'])
        .size()
        .reset_index(name='Count')
    )

    # ---------------------------------------
    # 3. Horizontal Stacked Bar Chart
    # ---------------------------------------
    fig = px.bar(
        act_out_counts,
        x='Count',
        y='Activity Type',
        color='Output',
        orientation='h',                   # <-- horizontal
        title='Activity Type vs Output (2025)',
        barmode='stack',
        template='plotly_white',
        color_discrete_sequence=px.colors.sequential.Blues_r  # darker blues
    )

    fig.update_layout(
        xaxis_title="Number of Activities",
        yaxis_title="Activity Type",
        legend_title="Output"
    )
    return fig


def engagement_levels(df =pd.DataFrame)->go.Figure:
    # Parse dates
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')

    # Group by workstream and engagement
    ws_eng_counts = (
        df.groupby(['Workstreams', 'Engagement'])
        .size()
        .reset_index(name='Count')
    )

    # Grouped bar chart
    fig = px.bar(
        ws_eng_counts,
        x='Workstreams',
        y='Count',
        color='Engagement',
        barmode='group',                           # <-- grouped, not stacked
        title='Workstream vs Engagement Levels (2025)',
        template='plotly_white',
        color_discrete_sequence=px.colors.sequential.Blues_r  # clean dark blues
    )

    fig.update_layout(
        xaxis_title="Workstream",
        yaxis_title="Number of Activities",
        legend_title="Engagement Level"
    )

    return fig


def access_pie(df = pd.DataFrame)->go.Figure:

    # Count Access values
    access_counts = df['Access'].value_counts().reset_index()
    access_counts.columns = ['Access', 'Count']

    # Pie chart
    fig_access = px.pie(
        access_counts,
        names='Access',
        values='Count',
        title='Access Proportion Across All Activities',
        color_discrete_sequence=px.colors.sequential.Blues_r,   # dark blues
        hole=0.0                                                 # full pie
    )

    fig_access.update_layout(
        template='plotly_white',
    )

    return fig_access


def activity_heatmap(df = pd.DataFrame)->go.Figure:
    ws_counts = df['Workstreams'].value_counts().reset_index()
    ws_counts.columns = ['Workstream', 'Count']
    
    # Number of workstreams
    n = len(ws_counts)
    
    # Determine grid size (square or rectangle close to square)
    grid_size = int(np.ceil(np.sqrt(n)))
    
    # Pad data to fill the grid
    padded_counts = ws_counts['Count'].tolist() + [0] * (grid_size**2 - n)
    padded_labels = ws_counts['Workstream'].tolist() + [""] * (grid_size**2 - n)
    
    # Convert to a matrix
    count_matrix = np.array(padded_counts).reshape(grid_size, grid_size)
    label_matrix = np.array(padded_labels).reshape(grid_size, grid_size)
    
    # Square heatmap
    fig = px.imshow(
        count_matrix,
        color_continuous_scale=px.colors.sequential.Blues_r,
        aspect='equal',  # ensures squares
        text_auto=False  # no numbers on tiles
    )
    
    # Hover tooltips with the correct Workstream name
    fig.update_traces(
        hovertemplate="Workstream: %{customdata}<br>Count: %{z}<extra></extra>",
        customdata=label_matrix
    )
    fig.update_layout(
        title="Workstream Activity Heatmap (Square Tiles)",
        template="plotly_white",
        xaxis_visible=False,
        yaxis_visible=False
    )
    
    return fig
    
    
    
def activity_trend_ex_meetings(df:pd.DataFrame)->go.Figure:
    
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')

   
    df['Activity Type'] = df['Activity Type'].astype(str).str.strip().str.lower()
    df_filtered = df[df['Activity Type'] != 'meeting'].copy()
    
    # ---------------------------------------
    # 4. Extract Month
    # ---------------------------------------
    df_filtered['Month'] = df_filtered['Date'].dt.month_name()
    
    # Keep Jan to Oct only
    month_order = [
        "January", "February", "March", "April", "May",
        "June", "July", "August", "September", "October"
    ]
    df_filtered = df_filtered[df_filtered['Month'].isin(month_order)]
    
    # ---------------------------------------
    # 5. Count activities per month
    # ---------------------------------------
    monthly_counts = (
        df_filtered.groupby("Month")
                   .size()
                   .reindex(month_order)      # ensures correct order
                   .reset_index(name="Count")
    )
    
    fig = px.line(
        monthly_counts,
        x='Month',
        y='Count',
        markers=True,
        title='Activity Trend (Jan–Oct) — Excluding Meetings',
        template='plotly_white',
        color_discrete_sequence=["#1f77b4"],  # Blue line
    )
    
    fig.update_layout(
        xaxis_title="Month",
        yaxis_title="Number of Activities",
        hovermode="x unified"
    )
    
    return fig
    
    
    
def meetings_monthly(df):
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')

    df['Activity Type'] = df['Activity Type'].astype(str).str.strip().str.lower()
    
    df_meetings = df[df['Activity Type'] == 'meeting'].copy()
    
    # ---------------------------------------
    # 4. Extract Month
    # ---------------------------------------
    df_meetings['Month'] = df_meetings['Date'].dt.month_name()
    
    # Filter only Sept–Oct
    target_months = ["September", "October"]
    df_meetings = df_meetings[df_meetings['Month'].isin(target_months)]
    
    # ---------------------------------------
    # 5. Count meetings per month
    # ---------------------------------------
    monthly_counts = (
        df_meetings.groupby('Month')
                   .size()
                   .reindex(target_months)
                   .reset_index(name='Count')
    )
    
    fig = px.line(
        monthly_counts,
        x='Month',
        y='Count',
        markers=True,
        title='Meetings Trend (September–October)',
        template='plotly_white',
        color_discrete_sequence=["#004c99"],  # deep blue
    )
    
    fig.update_layout(
        xaxis_title="Month",
        yaxis_title="Number of Meetings",
        hovermode="x unified"
    )
    return fig
    
    
def activity_monthly_trend(df):
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')

    df['Month'] = df['Date'].dt.month_name()
    
    # Keep only September + October
    target_months = ["September", "October"]
    df_sep_oct = df[df['Month'].isin(target_months)].copy()
    
    # ---------------------------------------
    # 4. Count activities per month
    # ---------------------------------------
    monthly_counts = (
        df_sep_oct.groupby("Month")
                  .size()
                  .reindex(target_months)     # ensure correct order
                  .reset_index(name="Count")
    )
    
    fig = px.line(
        monthly_counts,
        x='Month',
        y='Count',
        markers=True,
        title='Activity Trend (September–October)',
        template='plotly_white',
        color_discrete_sequence=["#1f77b4"],  # blue line
    )
    
    fig.update_layout(
        xaxis_title="Month",
        yaxis_title="Number of Activities",
        hovermode="x unified"
    )
    return fig



