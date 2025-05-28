"""Tests for the visualization module."""

import pytest
import pandas as pd
import plotly.graph_objects as go
from pybleau.viz import TableauViz
from pybleau.auth import TableauClient
from unittest.mock import Mock, patch

@pytest.fixture
def sample_data():
    """Create sample data for testing."""
    return pd.DataFrame({
        'category': ['A', 'B', 'C', 'A', 'B', 'C'],
        'values': [10, 20, 15, 25, 30, 35],
        'group': ['X', 'X', 'X', 'Y', 'Y', 'Y'],
        'date': pd.date_range('2023-01-01', periods=6),
        'size': [100, 200, 150, 250, 300, 350],
        'target': [15, 25, 20, 30, 35, 40],
        'stage': ['Awareness', 'Interest', 'Consideration', 'Intent', 'Evaluation', 'Purchase']
    })

@pytest.fixture
def viz():
    """Create TableauViz instance."""
    return TableauViz()

@pytest.fixture
def mock_client():
    """Create a mock TableauClient."""
    client = Mock(spec=TableauClient)
    client.site_uuid = "test-site"
    client.is_authenticated = True
    return client

def test_bar_chart(viz, sample_data):
    """Test bar chart creation."""
    fig = viz.bar_chart(
        data=sample_data,
        x='category',
        y='values',
        title='Test Bar Chart',
        color='group'
    )
    assert isinstance(fig, go.Figure)
    assert fig.layout.title.text == 'Test Bar Chart'

def test_line_chart(viz, sample_data):
    """Test line chart creation."""
    fig = viz.line_chart(
        data=sample_data,
        x='date',
        y='values',
        title='Test Line Chart',
        color='group'
    )
    assert isinstance(fig, go.Figure)
    assert fig.layout.title.text == 'Test Line Chart'

def test_scatter_plot(viz, sample_data):
    """Test scatter plot creation."""
    fig = viz.scatter_plot(
        data=sample_data,
        x='category',
        y='values',
        title='Test Scatter Plot',
        color='group',
        tooltip=['date']
    )
    assert isinstance(fig, go.Figure)
    assert fig.layout.title.text == 'Test Scatter Plot'

def test_pie_chart(viz, sample_data):
    """Test pie chart creation."""
    # Aggregate data for pie chart
    pie_data = sample_data.groupby('category')['values'].sum().reset_index()
    fig = viz.pie_chart(
        data=pie_data,
        values='values',
        names='category',
        title='Test Pie Chart'
    )
    assert isinstance(fig, go.Figure)
    assert fig.layout.title.text == 'Test Pie Chart'

def test_box_plot(viz, sample_data):
    """Test box plot creation."""
    fig = viz.box_plot(
        data=sample_data,
        x='category',
        y='values',
        title='Test Box Plot',
        color='group'
    )
    assert isinstance(fig, go.Figure)
    assert fig.layout.title.text == 'Test Box Plot'

def test_heatmap(viz, sample_data):
    """Test heatmap creation."""
    fig = viz.heatmap(
        data=sample_data,
        x='category',
        y='group',
        values='values',
        title='Test Heatmap'
    )
    assert isinstance(fig, go.Figure)
    assert fig.layout.title.text == 'Test Heatmap'

def test_treemap(viz, sample_data):
    """Test treemap creation."""
    fig = viz.treemap(
        data=sample_data,
        path=['group', 'category'],
        values='values',
        title='Test Treemap',
        color='values'
    )
    assert isinstance(fig, go.Figure)
    assert fig.layout.title.text == 'Test Treemap'

def test_bubble_chart(viz, sample_data):
    """Test bubble chart creation."""
    fig = viz.bubble_chart(
        data=sample_data,
        x='category',
        y='values',
        size='size',
        title='Test Bubble Chart',
        color='group',
        tooltip=['date']
    )
    assert isinstance(fig, go.Figure)
    assert fig.layout.title.text == 'Test Bubble Chart'

def test_area_chart(viz, sample_data):
    """Test area chart creation."""
    fig = viz.area_chart(
        data=sample_data,
        x='date',
        y='values',
        title='Test Area Chart',
        color='group'
    )
    assert isinstance(fig, go.Figure)
    assert fig.layout.title.text == 'Test Area Chart'

def test_funnel_chart(viz, sample_data):
    """Test funnel chart creation."""
    # Aggregate data for funnel chart
    funnel_data = sample_data.groupby('stage')['values'].sum().reset_index()
    fig = viz.funnel_chart(
        data=funnel_data,
        values='values',
        stages='stage',
        title='Test Funnel Chart'
    )
    assert isinstance(fig, go.Figure)
    assert fig.layout.title.text == 'Test Funnel Chart'

def test_bullet_chart(viz, sample_data):
    """Test bullet chart creation."""
    bullet_data = sample_data.groupby('category').agg({
        'values': 'sum',
        'target': 'mean'
    }).reset_index().head(1)  # Take first row for bullet chart
    
    fig = viz.bullet_chart(
        data=bullet_data,
        measure='values',
        target='target',
        title='Test Bullet Chart'
    )
    assert isinstance(fig, go.Figure)
    assert fig.layout.title.text == 'Test Bullet Chart'

def test_dict_input(viz):
    """Test dictionary input handling."""
    data = {
        'x': ['A', 'B', 'C'],
        'y': [1, 2, 3]
    }
    fig = viz.bar_chart(data=data, x='x', y='y')
    assert isinstance(fig, go.Figure)

def test_tableau_colors(viz):
    """Test Tableau color palette."""
    assert len(viz.colors) == 10  # Should have 10 colors
    assert viz.colors[0] == '#4E79A7'  # First color should be blue

def test_invalid_input(viz):
    """Test invalid input handling."""
    with pytest.raises(ValueError):
        viz.bar_chart(data=None, x='x', y='y')

    with pytest.raises(KeyError):
        viz.bar_chart(data={'x': [1, 2]}, x='missing', y='y')

def test_from_tableau_view(mock_client):
    """Test fetching data from Tableau view."""
    viz = TableauViz(client=mock_client)
    mock_client.get.return_value.json.return_value = {
        'data': [{'column1': 1, 'column2': 2}]
    }
    
    df = viz.from_tableau_view('view-id')
    assert isinstance(df, pd.DataFrame)
    mock_client.get.assert_called_once_with('/api/3.8/sites/test-site/views/view-id/data')

def test_from_tableau_view_no_client():
    """Test error when no client is provided."""
    viz = TableauViz()
    with pytest.raises(ValueError, match="TableauClient is required for accessing Tableau data"):
        viz.from_tableau_view('view-id') 