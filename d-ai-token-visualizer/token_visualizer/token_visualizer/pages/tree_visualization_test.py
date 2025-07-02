"""Tree visualization test page for verifying tree components."""

import reflex as rx
from typing import List, Optional
import plotly.graph_objects as go
import networkx as nx
import math

from ..components.token_tree import (
    TreeLayoutCalculator,
    tree_svg_container,
    tree_controls,
    tree_info_panel,
    responsive_tree_container,
    tree_path_display
)
from ..components.layout import app_layout
from ..utils.tree_structure import TokenTree, create_sample_tree
from ..services.llm_client import TokenProbability
from ..components.color_coded_text import get_probability_color, get_probability_background_color


class TreeVisualizationTestState(rx.State):
    """State for testing tree visualization components."""
    
    # Tree data
    tree: TokenTree = TokenTree()
    
    # Layout and display settings
    zoom_level: float = 1.0
    max_depth: int = 5
    max_branches: int = 5
    
    # Selection state
    selected_node_id: str = ""
    highlighted_node_id: str = ""
    
    # UI state
    is_generating: bool = False
    error_message: str = ""
    has_error: bool = False
    
    # Debug info
    tree_node_count: int = 0
    
    # Plotly figure state
    tree_figure: go.Figure = go.Figure()
    
    def get_tree_layout(self):
        """Get the current tree layout."""
        try:
            # Create calculator dynamically (not as state variable)
            calculator = TreeLayoutCalculator()
            return calculator.calculate_layout(self.tree)
        except Exception as e:
            # Return empty layout if calculation fails
            from ..components.token_tree import TreeLayout
            return TreeLayout({}, 400, 200, [])
    
    def create_sample_tree(self):
        """Create a sample tree for testing with proper left-to-right hierarchical structure."""
        try:
            # Use smaller limits for manageable visualization
            demo_max_depth = min(3, self.max_depth)  # Limit to 3 levels max for demo
            demo_max_branches = min(3, self.max_branches)  # Limit to 3 branches max for demo
            
            self.tree = TokenTree(max_depth=demo_max_depth, max_branches_per_node=demo_max_branches)
            
            # Create root node (Level 0)
            root_id = self.tree.create_root("Start")
            current_level_nodes = [root_id]
            
            # Define sample token alternatives for each level (limited set)
            level_alternatives = [
                # Level 1: Initial tokens (3 options)
                [
                    TokenProbability(token="The", probability=0.85, logprob=-0.16, percentage=85.0),
                    TokenProbability(token="A", probability=0.10, logprob=-2.30, percentage=10.0),
                    TokenProbability(token="My", probability=0.05, logprob=-3.00, percentage=5.0)
                ],
                # Level 2: Following tokens (3 options)
                [
                    TokenProbability(token="cat", probability=0.70, logprob=-0.36, percentage=70.0),
                    TokenProbability(token="dog", probability=0.25, logprob=-1.39, percentage=25.0),
                    TokenProbability(token="bird", probability=0.05, logprob=-3.00, percentage=5.0)
                ]
            ]
            
            # Build tree level by level (breadth-first) - limited depth
            for level_idx, alternatives in enumerate(level_alternatives):
                if level_idx >= demo_max_depth - 1:  # Respect demo max depth
                    break
                    
                next_level_nodes = []
                for parent_id in current_level_nodes:
                    # Only add children if we haven't exceeded branching limits
                    if len(self.tree.nodes[parent_id].children) == 0:  # Only add if no children yet
                        child_ids = self.tree.add_token_alternatives(parent_id, alternatives[:demo_max_branches])
                        next_level_nodes.extend(child_ids)
                
                current_level_nodes = next_level_nodes
                if not current_level_nodes:  # No more nodes to expand
                    break
            
            # Update debug info
            self.tree_node_count = len(self.tree.nodes)
            
            # Update the tree figure
            self.update_tree_figure()
            
        except Exception as e:
            self.error_message = f"Failed to create tree: {str(e)}"
            self.has_error = True
    
    def on_node_click(self, node_id: str):
        """Handle node click events."""
        self.selected_node_id = node_id
        self.tree.select_path_to_node(node_id)
    
    def on_zoom_in(self):
        """Increase zoom level."""
        self.zoom_level = min(self.zoom_level + 0.2, 3.0)
    
    def on_zoom_out(self):
        """Decrease zoom level."""
        self.zoom_level = max(self.zoom_level - 0.2, 0.5)
    
    def on_zoom_reset(self):
        """Reset zoom level."""
        self.zoom_level = 1.0
    
    def on_depth_change(self, value: str):
        """Handle max depth change."""
        try:
            new_depth = int(value)
            if 1 <= new_depth <= 20:
                self.max_depth = new_depth
                self.create_sample_tree()
        except ValueError:
            pass
    
    def on_branches_change(self, value: str):
        """Handle max branches change."""
        try:
            new_branches = int(value)
            if 1 <= new_branches <= 10:
                self.max_branches = new_branches
                self.create_sample_tree()
        except ValueError:
            pass
    
    def reset_tree(self):
        """Reset the tree to initial state."""
        self.tree = TokenTree()
        self.selected_node_id = ""
        self.highlighted_node_id = ""
        self.create_sample_tree()
    
    def clear_branches(self):
        """Clear all branches except the main path."""
        # This would implement branch clearing logic
        # For now, just reset
        self.reset_tree()
    
    def force_create_tree(self):
        """Force create the tree for debugging."""
        self.create_sample_tree()
        self.update_tree_figure()
    
    def update_tree_figure(self):
        """Create a Plotly tree visualization and update the state figure."""
        try:
            # Create NetworkX graph from tree
            G = nx.DiGraph()
            
            if not self.tree.nodes:
                # Return empty figure if no tree
                fig = go.Figure()
                fig.add_annotation(
                    text="No tree data available",
                    x=0.5, y=0.5,
                    xref="paper", yref="paper",
                    showarrow=False,
                    font=dict(size=16, color="gray")
                )
                fig.update_layout(
                    xaxis=dict(visible=False),
                    yaxis=dict(visible=False),
                    plot_bgcolor='white',
                    paper_bgcolor='white',
                    height=400
                )
                self.tree_figure = fig
                return
            
            # Add nodes to NetworkX graph
            for node_id, node in self.tree.nodes.items():
                # Get token text and probability for display
                token_text = node.token if node.token else "ROOT"
                probability = node.probability * 100 if node.probability else 100.0
                
                # Add node with attributes
                G.add_node(node_id, 
                          text=token_text,
                          probability=probability,
                          is_selected=getattr(node, 'is_selected', False))
                
                # Add edges to children
                for child_id in node.children:
                    G.add_edge(node_id, child_id)
            
            # Create hierarchical layout with manual positioning for better left-to-right flow
            pos = {}
            
            # Group nodes by depth level
            levels = {}
            for node_id, node in self.tree.nodes.items():
                depth = node.depth
                if depth not in levels:
                    levels[depth] = []
                levels[depth].append(node_id)
            
            # Position nodes level by level (left to right)
            x_spacing = 4.0  # Horizontal spacing between levels  
            y_spacing = 8.0  # Vertical spacing between nodes in same level (dramatically increased)
            
            for depth, node_ids in levels.items():
                x = depth * x_spacing
                # Center nodes vertically within each level
                total_height = (len(node_ids) - 1) * y_spacing
                start_y = -(total_height / 2)
                
                for i, node_id in enumerate(node_ids):
                    y = start_y + (i * y_spacing)
                    pos[node_id] = (x, y)
            
            # Add nodes to NetworkX graph with positions
            for node_id, node in self.tree.nodes.items():
                G.add_node(node_id, 
                          text=node.token if node.token else "ROOT",
                          probability=node.probability * 100 if node.probability else 100.0,
                          is_selected=getattr(node, 'is_selected', False))
                
                # Add edges to children
                for child_id in node.children:
                    G.add_edge(node_id, child_id)
            
            # Extract coordinates
            x_nodes = [pos[node][0] for node in G.nodes()]
            y_nodes = [pos[node][1] for node in G.nodes()]
            
            # Create edge traces with improved styling
            edge_x = []
            edge_y = []
            for edge in G.edges():
                x0, y0 = pos[edge[0]]
                x1, y1 = pos[edge[1]]
                edge_x.extend([x0, x1, None])
                edge_y.extend([y0, y1, None])
            
            edge_trace = go.Scatter(
                x=edge_x, y=edge_y,
                line=dict(width=2, color='#9CA3AF'),
                hoverinfo='none',
                mode='lines'
            )
            
            # Create node traces with pill-shaped styling and Interactive Generation color scheme
            node_colors = []
            node_border_colors = []
            node_text = []
            hover_text = []
            
            for node_id in G.nodes():
                node = self.tree.nodes[node_id]
                token_text = node.token if node.token else "ROOT"
                probability = node.probability * 100 if node.probability else 100.0
                
                # Use same color scheme as Interactive Generation page (color_coded_text.py)
                if probability >= 80:  # Very high probability
                    bg_color = '#D1FAE5'  # Green-100
                    border_color = '#10B981'  # Green-500
                elif probability >= 60:  # High probability
                    bg_color = '#ECFDF5'  # Green-50
                    border_color = '#34D399'  # Green-400
                elif probability >= 40:  # Medium probability
                    bg_color = '#FEF3C7'  # Yellow-100
                    border_color = '#FCD34D'  # Yellow-300
                elif probability >= 20:  # Medium-low probability
                    bg_color = '#FEF3C7'  # Yellow-100
                    border_color = '#F59E0B'  # Amber-500
                elif probability >= 10:  # Low probability
                    bg_color = '#FED7AA'  # Orange-100
                    border_color = '#F97316'  # Orange-500
                else:  # Very low probability
                    bg_color = '#FEE2E2'  # Red-100
                    border_color = '#EF4444'  # Red-500
                
                # Special styling for selected nodes
                if node_id == self.selected_node_id:
                    bg_color = '#DBEAFE'  # Blue-100
                    border_color = '#3B82F6'  # Blue-500
                
                node_colors.append(bg_color)
                node_border_colors.append(border_color)
                node_text.append(token_text)
                hover_text.append(f"Token: {token_text}<br>Probability: {probability:.1f}%<br>Click to select")
            
            # Create node trace with pill-shaped markers
            node_trace = go.Scatter(
                x=[pos[node][0] for node in G.nodes()],
                y=[pos[node][1] for node in G.nodes()],
                mode='markers+text',
                text=node_text,
                textposition='middle center',
                textfont=dict(size=14, color='#1F2937'),  # Dark gray text
                hovertext=hover_text,
                hoverinfo='text',
                marker=dict(
                    size=60,  # Larger nodes for better text visibility
                    color=node_colors,
                    line=dict(width=2, color=node_border_colors),
                    symbol='square',  # Use square as base for rounded rectangle effect
                    opacity=0.9
                ),
                customdata=[node_id for node_id in G.nodes()],
                name="Token Nodes"
            )
            # Create figure with both edge and node traces
            fig = go.Figure(data=[edge_trace, node_trace])
            fig.update_layout(
                title=dict(
                    text=f"Token Tree Visualization ({len(G.nodes())} nodes)",
                    x=0.5,
                    font=dict(size=18, family="Arial, sans-serif")
                ),
                showlegend=False,
                hovermode='closest',
                margin=dict(b=40, l=40, r=40, t=60),
                annotations=[ 
                    dict(
                        text="💡 Click nodes to select • Hover for details • Zoom and pan to explore",
                        showarrow=False,
                        xref="paper", yref="paper",
                        x=0.5, y=-0.05,
                        xanchor='center', yanchor='top',
                        font=dict(size=13, color="gray", family="Arial, sans-serif")
                    )
                ],
                xaxis=dict(
                    showgrid=False, 
                    zeroline=False, 
                    showticklabels=False,
                    fixedrange=False  # Allow zooming
                ),
                yaxis=dict(
                    showgrid=False, 
                    zeroline=False, 
                    showticklabels=False,
                    fixedrange=False  # Allow zooming
                ),
                plot_bgcolor='#FAFAFA',
                paper_bgcolor='white',
                height=1000,  # Increased height significantly for better visibility with larger spacing
                dragmode='pan'  # Enable panning by default
            )
            
            # Update the state figure
            self.tree_figure = fig
            
        except Exception as e:
            # Create error figure
            fig = go.Figure()
            fig.add_annotation(
                text=f"Error creating tree: {str(e)}",
                x=0.5, y=0.5,
                xref="paper", yref="paper",
                showarrow=False,
                font=dict(size=14, color="red")
            )
            fig.update_layout(
                xaxis=dict(visible=False),
                yaxis=dict(visible=False),
                plot_bgcolor='white',
                paper_bgcolor='white',
                height=400
            )
            self.tree_figure = fig


def tree_layout_test() -> rx.Component:
    """Test the tree layout calculation and Plotly rendering."""
    
    return rx.vstack(
        rx.heading("Tree Layout Test", size="4"),
        
        # Tree visualization with Plotly interactive graph
        rx.box(
            rx.cond(
                TreeVisualizationTestState.tree_node_count > 0,
                rx.vstack(
                    rx.text(f"Tree has {TreeVisualizationTestState.tree_node_count} nodes", font_size="1rem", font_weight="500"),
                    # Interactive Plotly tree visualization
                    rx.plotly(
                        data=TreeVisualizationTestState.tree_figure,
                        style={"width": "100%", "height": "1000px"}
                    ),
                    spacing="2",
                    width="100%"
                ),
                rx.text("No tree data - click 'Force Create Tree' to initialize", color="red.500", font_size="1rem")
            ),
            width="100%",
            min_height="1000px",
            padding="4",
            border="1px solid",
            border_color="gray.300",
            border_radius="8px",
            bg="white"
        ),
        
        spacing="4",
        width="100%"
    )


def tree_controls_test() -> rx.Component:
    """Test the tree controls component."""
    
    return rx.vstack(
        rx.heading("Tree Controls Test", size="4"),
        
        tree_controls(
            tree=TreeVisualizationTestState.tree,
            max_depth=TreeVisualizationTestState.max_depth,
            max_branches=TreeVisualizationTestState.max_branches,
            on_depth_change=TreeVisualizationTestState.on_depth_change,
            on_branches_change=TreeVisualizationTestState.on_branches_change,
            on_reset=TreeVisualizationTestState.reset_tree,
            on_clear_branches=TreeVisualizationTestState.clear_branches
        ),
        
        spacing="4",
        width="100%"
    )


def tree_info_test() -> rx.Component:
    """Test the tree information panel."""
    
    return rx.vstack(
        rx.heading("Tree Information Test", size="4"),
        
        rx.box(
            rx.vstack(
                rx.heading("Tree Statistics", size="3"),
                rx.text(f"Node Count: {TreeVisualizationTestState.tree_node_count}", font_size="0.875rem"),
                rx.text(f"Max Depth Setting: {TreeVisualizationTestState.max_depth}", font_size="0.875rem"),
                rx.text(f"Max Branches Setting: {TreeVisualizationTestState.max_branches}", font_size="0.875rem"),
                rx.text(f"Selected Node: {rx.cond(TreeVisualizationTestState.selected_node_id, TreeVisualizationTestState.selected_node_id, 'None')}", font_size="0.875rem"),
                spacing="1",
                align_items="start"
            ),
            padding="4",
            border="1px solid",
            border_color="gray.200",
            border_radius="8px",
            bg="white"
        ),
        
        spacing="4",
        width="100%"
    )


def tree_path_test() -> rx.Component:
    """Test the tree path display."""
    
    return rx.vstack(
        rx.heading("Tree Path Test", size="4"),
        
        tree_path_display(tree=TreeVisualizationTestState.tree),
        
        spacing="4",
        width="100%"
    )


def tree_visualization_test_content() -> rx.Component:
    """Main content for tree visualization testing."""
    
    return rx.vstack(
        rx.heading("Tree Visualization Components Test", size="6"),
        rx.text(
            "This page tests the tree visualization components using interactive Plotly network graphs. "
            "Features include color-coded probability visualization, interactive zoom/pan, hover details, and node selection.",
            color="gray.600"
        ),
        
        # Error display
        rx.cond(
            TreeVisualizationTestState.has_error,
            rx.callout(
                TreeVisualizationTestState.error_message,
                icon="alert-circle",
                color_scheme="red",
                role="alert"
            )
        ),
        
        # Debug section
        rx.box(
            rx.vstack(
                rx.heading("Debug Information", size="4"),
                rx.text(f"Tree Node Count: {TreeVisualizationTestState.tree_node_count}", font_size="0.875rem"),
                rx.text(f"Max Depth: {TreeVisualizationTestState.max_depth}", font_size="0.875rem"),
                rx.text(f"Max Branches: {TreeVisualizationTestState.max_branches}", font_size="0.875rem"),
                rx.button(
                    "Force Create Tree",
                    size="2",
                    variant="outline",
                    color_scheme="blue",
                    on_click=TreeVisualizationTestState.force_create_tree
                ),
                spacing="2",
                align_items="start"
            ),
            padding="4",
            border="1px solid",
            border_color="blue.200",
            border_radius="8px",
            bg="blue.50"
        ),
        
        # Main tree visualization
        rx.box(
            tree_layout_test(),
            width="100%",
            padding="4",
            border="1px solid",
            border_color="gray.200",
            border_radius="8px"
        ),
        
        # Side panels
        rx.hstack(
            # Controls panel
            rx.box(
                tree_controls_test(),
                width="50%",
                padding="4",
                border="1px solid",
                border_color="gray.200",
                border_radius="8px"
            ),
            
            # Info panel
            rx.box(
                tree_info_test(),
                width="50%",
                padding="4",
                border="1px solid",
                border_color="gray.200",
                border_radius="8px"
            ),
            
            spacing="4",
            width="100%"
        ),
        
        # Path display
        rx.box(
            tree_path_test(),
            width="100%",
            padding="4",
            border="1px solid",
            border_color="gray.200",
            border_radius="8px"
        ),
        
        spacing="6",
        width="100%",
        padding="4"
    )


def tree_visualization_test_page() -> rx.Component:
    """Tree visualization test page with layout."""
    
    return app_layout(
        tree_visualization_test_content()
    )
