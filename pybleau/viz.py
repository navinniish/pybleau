"""Visualization module for creating Tableau-style charts."""

import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
from typing import List, Dict, Union, Optional
from .auth import TableauClient

# Tableau-like color palette
TABLEAU_COLORS = {
    'blue': '#4E79A7',
    'orange': '#F28E2B',
    'red': '#E15759',
    'teal': '#76B7B2',
    'green': '#59A14F',
    'yellow': '#EDC948',
    'purple': '#B07AA1',
    'pink': '#FF9DA7',
    'brown': '#9C755F',
    'gray': '#BAB0AC'
}

class TableauViz:
    """Class for creating Tableau-style visualizations."""

    def __init__(self, theme: str = "tableau", client: Optional[TableauClient] = None):
        """
        Initialize TableauViz with a specific theme and optional Tableau client.
        
        Args:
            theme (str): The theme to use ('tableau', 'plotly', etc.)
            client (TableauClient, optional): Authenticated Tableau client for direct data access
        """
        self.theme = theme
        self.colors = list(TABLEAU_COLORS.values())
        self.client = client

    def from_tableau_view(self, view_id: str) -> pd.DataFrame:
        """
        Get data directly from a Tableau view.
        
        Args:
            view_id: ID of the Tableau view
            
        Returns:
            DataFrame containing the view data
        """
        if not self.client:
            raise ValueError("TableauClient is required for accessing Tableau data")
        
        # Use the client to fetch data from the view
        response = self.client.get(f"/api/3.8/sites/{self.client.site_uuid}/views/{view_id}/data")
        return pd.DataFrame(response.json()['data'])

    def bar_chart(self, 
                 data: Union[pd.DataFrame, Dict], 
                 x: str, 
                 y: str, 
                 title: str = "",
                 color: Optional[str] = None,
                 orientation: str = 'vertical',
                 stacked: bool = False) -> go.Figure:
        """
        Create a Tableau-style bar chart.
        
        Args:
            data: DataFrame or dictionary containing the data
            x: Column name for x-axis
            y: Column name for y-axis
            title: Chart title
            color: Column name for color grouping
            orientation: 'vertical' or 'horizontal'
            stacked: Whether to stack bars when using colors
            
        Returns:
            Plotly figure object
        """
        if isinstance(data, dict):
            data = pd.DataFrame(data)

        fig = px.bar(
            data,
            x=x if orientation == 'vertical' else y,
            y=y if orientation == 'vertical' else x,
            title=title,
            color=color,
            color_discrete_sequence=self.colors,
            barmode='stack' if stacked else 'group'
        )

        # Apply Tableau-style formatting
        fig.update_layout(
            plot_bgcolor='white',
            paper_bgcolor='white',
            title={
                'x': 0.5,
                'xanchor': 'center',
                'font': {'size': 24}
            },
            font={'family': 'Arial', 'size': 14},
            showlegend=True if color else False,
            legend={'orientation': 'h', 'y': -0.15}
        )

        # Add gridlines
        fig.update_yaxes(
            showgrid=True,
            gridwidth=1,
            gridcolor='lightgray',
            zeroline=True,
            zerolinewidth=1,
            zerolinecolor='gray'
        )

        return fig

    def line_chart(self,
                  data: Union[pd.DataFrame, Dict],
                  x: str,
                  y: str,
                  title: str = "",
                  color: Optional[str] = None,
                  markers: bool = True) -> go.Figure:
        """
        Create a Tableau-style line chart.
        
        Args:
            data: DataFrame or dictionary containing the data
            x: Column name for x-axis
            y: Column name for y-axis
            title: Chart title
            color: Column name for color grouping
            markers: Whether to show markers on the lines
            
        Returns:
            Plotly figure object
        """
        if isinstance(data, dict):
            data = pd.DataFrame(data)

        fig = px.line(
            data,
            x=x,
            y=y,
            title=title,
            color=color,
            color_discrete_sequence=self.colors,
            markers=markers
        )

        # Apply Tableau-style formatting
        fig.update_layout(
            plot_bgcolor='white',
            paper_bgcolor='white',
            title={
                'x': 0.5,
                'xanchor': 'center',
                'font': {'size': 24}
            },
            font={'family': 'Arial', 'size': 14},
            showlegend=True if color else False,
            legend={'orientation': 'h', 'y': -0.15}
        )

        # Add gridlines
        fig.update_yaxes(
            showgrid=True,
            gridwidth=1,
            gridcolor='lightgray',
            zeroline=True,
            zerolinewidth=1,
            zerolinecolor='gray'
        )

        return fig

    def scatter_plot(self,
                    data: Union[pd.DataFrame, Dict],
                    x: str,
                    y: str,
                    title: str = "",
                    color: Optional[str] = None,
                    size: Optional[str] = None,
                    tooltip: Optional[List[str]] = None) -> go.Figure:
        """
        Create a Tableau-style scatter plot.
        
        Args:
            data: DataFrame or dictionary containing the data
            x: Column name for x-axis
            y: Column name for y-axis
            title: Chart title
            color: Column name for color grouping
            size: Column name for point sizes
            tooltip: List of column names to show in tooltip
            
        Returns:
            Plotly figure object
        """
        if isinstance(data, dict):
            data = pd.DataFrame(data)

        fig = px.scatter(
            data,
            x=x,
            y=y,
            title=title,
            color=color,
            size=size,
            color_discrete_sequence=self.colors,
            hover_data=tooltip
        )

        # Apply Tableau-style formatting
        fig.update_layout(
            plot_bgcolor='white',
            paper_bgcolor='white',
            title={
                'x': 0.5,
                'xanchor': 'center',
                'font': {'size': 24}
            },
            font={'family': 'Arial', 'size': 14},
            showlegend=True if color else False,
            legend={'orientation': 'h', 'y': -0.15}
        )

        # Add gridlines
        fig.update_yaxes(
            showgrid=True,
            gridwidth=1,
            gridcolor='lightgray',
            zeroline=True,
            zerolinewidth=1,
            zerolinecolor='gray'
        )
        fig.update_xaxes(
            showgrid=True,
            gridwidth=1,
            gridcolor='lightgray',
            zeroline=True,
            zerolinewidth=1,
            zerolinecolor='gray'
        )

        return fig

    def pie_chart(self,
                 data: Union[pd.DataFrame, Dict],
                 values: str,
                 names: str,
                 title: str = "") -> go.Figure:
        """
        Create a Tableau-style pie chart.
        
        Args:
            data: DataFrame or dictionary containing the data
            values: Column name for slice values
            names: Column name for slice names
            title: Chart title
            
        Returns:
            Plotly figure object
        """
        if isinstance(data, dict):
            data = pd.DataFrame(data)

        fig = px.pie(
            data,
            values=values,
            names=names,
            title=title,
            color_discrete_sequence=self.colors
        )

        # Apply Tableau-style formatting
        fig.update_layout(
            plot_bgcolor='white',
            paper_bgcolor='white',
            title={
                'x': 0.5,
                'xanchor': 'center',
                'font': {'size': 24}
            },
            font={'family': 'Arial', 'size': 14},
            showlegend=True
        )

        # Update trace settings
        fig.update_traces(
            textposition='inside',
            textinfo='percent+label'
        )

        return fig

    def box_plot(self,
                data: Union[pd.DataFrame, Dict],
                x: str,
                y: str,
                title: str = "",
                color: Optional[str] = None) -> go.Figure:
        """
        Create a Tableau-style box plot.
        
        Args:
            data: DataFrame or dictionary containing the data
            x: Column name for x-axis categories
            y: Column name for y-axis values
            title: Chart title
            color: Column name for color grouping
            
        Returns:
            Plotly figure object
        """
        if isinstance(data, dict):
            data = pd.DataFrame(data)

        fig = px.box(
            data,
            x=x,
            y=y,
            title=title,
            color=color,
            color_discrete_sequence=self.colors
        )

        # Apply Tableau-style formatting
        fig.update_layout(
            plot_bgcolor='white',
            paper_bgcolor='white',
            title={
                'x': 0.5,
                'xanchor': 'center',
                'font': {'size': 24}
            },
            font={'family': 'Arial', 'size': 14},
            showlegend=True if color else False,
            legend={'orientation': 'h', 'y': -0.15}
        )

        # Add gridlines
        fig.update_yaxes(
            showgrid=True,
            gridwidth=1,
            gridcolor='lightgray',
            zeroline=True,
            zerolinewidth=1,
            zerolinecolor='gray'
        )

        return fig

    def heatmap(self,
               data: Union[pd.DataFrame, Dict],
               x: str,
               y: str,
               values: str,
               title: str = "",
               colorscale: Optional[str] = "RdYlBu_r") -> go.Figure:
        """
        Create a Tableau-style heatmap.
        
        Args:
            data: DataFrame or dictionary containing the data
            x: Column name for x-axis
            y: Column name for y-axis
            values: Column name for cell values
            title: Chart title
            colorscale: Color scale for the heatmap
            
        Returns:
            Plotly figure object
        """
        if isinstance(data, dict):
            data = pd.DataFrame(data)

        # Pivot data if needed
        if len(data[[x, y, values]].drop_duplicates()) == len(data):
            pivot_data = data.pivot(index=y, columns=x, values=values)
        else:
            pivot_data = data.pivot_table(index=y, columns=x, values=values, aggfunc='mean')

        fig = go.Figure(data=go.Heatmap(
            z=pivot_data.values,
            x=pivot_data.columns,
            y=pivot_data.index,
            colorscale=colorscale,
            hoverongaps=False
        ))

        # Apply Tableau-style formatting
        fig.update_layout(
            plot_bgcolor='white',
            paper_bgcolor='white',
            title={
                'text': title,
                'x': 0.5,
                'xanchor': 'center',
                'font': {'size': 24}
            },
            font={'family': 'Arial', 'size': 14}
        )

        return fig

    def treemap(self,
                data: Union[pd.DataFrame, Dict],
                path: List[str],
                values: str,
                title: str = "",
                color: Optional[str] = None) -> go.Figure:
        """
        Create a Tableau-style treemap.
        
        Args:
            data: DataFrame or dictionary containing the data
            path: List of columns defining the hierarchy
            values: Column name for size values
            title: Chart title
            color: Column name for color values
            
        Returns:
            Plotly figure object
        """
        if isinstance(data, dict):
            data = pd.DataFrame(data)

        fig = px.treemap(
            data,
            path=path,
            values=values,
            color=color,
            color_discrete_sequence=self.colors,
            title=title
        )

        # Apply Tableau-style formatting
        fig.update_layout(
            plot_bgcolor='white',
            paper_bgcolor='white',
            title={
                'x': 0.5,
                'xanchor': 'center',
                'font': {'size': 24}
            },
            font={'family': 'Arial', 'size': 14}
        )

        return fig

    def bubble_chart(self,
                    data: Union[pd.DataFrame, Dict],
                    x: str,
                    y: str,
                    size: str,
                    title: str = "",
                    color: Optional[str] = None,
                    text: Optional[str] = None,
                    tooltip: Optional[List[str]] = None) -> go.Figure:
        """
        Create a Tableau-style bubble chart.
        
        Args:
            data: DataFrame or dictionary containing the data
            x: Column name for x-axis
            y: Column name for y-axis
            size: Column name for bubble sizes
            title: Chart title
            color: Column name for color grouping
            text: Column name for bubble labels
            tooltip: List of column names to show in tooltip
            
        Returns:
            Plotly figure object
        """
        if isinstance(data, dict):
            data = pd.DataFrame(data)

        fig = px.scatter(
            data,
            x=x,
            y=y,
            size=size,
            color=color,
            text=text,
            title=title,
            color_discrete_sequence=self.colors,
            hover_data=tooltip
        )

        # Apply Tableau-style formatting
        fig.update_layout(
            plot_bgcolor='white',
            paper_bgcolor='white',
            title={
                'x': 0.5,
                'xanchor': 'center',
                'font': {'size': 24}
            },
            font={'family': 'Arial', 'size': 14},
            showlegend=True if color else False,
            legend={'orientation': 'h', 'y': -0.15}
        )

        # Add gridlines
        fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='lightgray')
        fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='lightgray')

        return fig

    def area_chart(self,
                  data: Union[pd.DataFrame, Dict],
                  x: str,
                  y: str,
                  title: str = "",
                  color: Optional[str] = None,
                  stacked: bool = True) -> go.Figure:
        """
        Create a Tableau-style area chart.
        
        Args:
            data: DataFrame or dictionary containing the data
            x: Column name for x-axis
            y: Column name for y-axis
            title: Chart title
            color: Column name for color grouping
            stacked: Whether to stack areas
            
        Returns:
            Plotly figure object
        """
        if isinstance(data, dict):
            data = pd.DataFrame(data)

        fig = px.area(
            data,
            x=x,
            y=y,
            color=color,
            title=title,
            color_discrete_sequence=self.colors,
            groupnorm='fraction' if stacked else None
        )

        # Apply Tableau-style formatting
        fig.update_layout(
            plot_bgcolor='white',
            paper_bgcolor='white',
            title={
                'x': 0.5,
                'xanchor': 'center',
                'font': {'size': 24}
            },
            font={'family': 'Arial', 'size': 14},
            showlegend=True if color else False,
            legend={'orientation': 'h', 'y': -0.15}
        )

        # Add gridlines
        fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='lightgray')
        fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='lightgray')

        return fig

    def funnel_chart(self,
                    data: Union[pd.DataFrame, Dict],
                    values: str,
                    stages: str,
                    title: str = "") -> go.Figure:
        """
        Create a Tableau-style funnel chart.
        
        Args:
            data: DataFrame or dictionary containing the data
            values: Column name for values
            stages: Column name for funnel stages
            title: Chart title
            
        Returns:
            Plotly figure object
        """
        if isinstance(data, dict):
            data = pd.DataFrame(data)

        fig = go.Figure(go.Funnel(
            y=data[stages],
            x=data[values],
            textposition="inside",
            textinfo="value+percent initial",
            opacity=0.85,
            marker={
                "color": self.colors,
                "line": {"width": 2, "color": "white"}
            },
            connector={"line": {"color": "white", "dash": "solid", "width": 2}}
        ))

        # Apply Tableau-style formatting
        fig.update_layout(
            plot_bgcolor='white',
            paper_bgcolor='white',
            title={
                'text': title,
                'x': 0.5,
                'xanchor': 'center',
                'font': {'size': 24}
            },
            font={'family': 'Arial', 'size': 14},
            showlegend=False
        )

        return fig

    def bullet_chart(self,
                    data: Union[pd.DataFrame, Dict],
                    measure: str,
                    target: str,
                    title: str = "",
                    orientation: str = "h") -> go.Figure:
        """
        Create a Tableau-style bullet chart.
        
        Args:
            data: DataFrame or dictionary containing the data
            measure: Column name for actual values
            target: Column name for target values
            title: Chart title
            orientation: 'h' for horizontal or 'v' for vertical
            
        Returns:
            Plotly figure object
        """
        if isinstance(data, dict):
            data = pd.DataFrame(data)

        fig = go.Figure()

        # Add the measure bar
        fig.add_trace(go.Bar(
            x=data[measure] if orientation == "h" else [0],
            y=[0] if orientation == "h" else data[measure],
            orientation=orientation,
            name="Actual",
            marker_color=self.colors[0],
            width=0.5
        ))

        # Add the target line
        fig.add_trace(go.Scatter(
            x=data[target] if orientation == "h" else [0],
            y=[0] if orientation == "h" else data[target],
            mode="markers",
            name="Target",
            marker=dict(symbol="line-ns-open" if orientation == "h" else "line-ew-open",
                       color="black",
                       size=20,
                       line=dict(width=4))
        ))

        # Apply Tableau-style formatting
        fig.update_layout(
            plot_bgcolor='white',
            paper_bgcolor='white',
            title={
                'text': title,
                'x': 0.5,
                'xanchor': 'center',
                'font': {'size': 24}
            },
            font={'family': 'Arial', 'size': 14},
            showlegend=True,
            legend={'orientation': 'h', 'y': -0.15},
            barmode='overlay'
        )

        # Add gridlines
        fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='lightgray')
        fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='lightgray')

        return fig 