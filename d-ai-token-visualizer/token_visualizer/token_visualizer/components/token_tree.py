"""Token tree visualization components using SVG for rendering tree structures."""

import reflex as rx
from typing import List, Dict, Optional, Tuple, Any
import math
from dataclasses import dataclass

from ..utils.tree_structure import TokenTree, TreeNode
from .color_coded_text import get_probability_color, get_probability_background_color, get_text_color


@dataclass
class NodePosition:
    """Represents the position of a node in the SVG coordinate system."""
    x: float
    y: float
    node_id: str


@dataclass
class TreeLayout:
    """Represents the complete layout of the tree with all node positions."""
    node_positions: Dict[str, NodePosition]
    width: float
    height: float
    levels: List[List[str]]  # Node IDs grouped by depth level


class TreeLayoutCalculator:
    """Calculates positions for nodes in a tree layout."""
    
    def __init__(self, 
                 node_width: float = 120,
                 node_height: float = 40,
                 horizontal_spacing: float = 20,
                 vertical_spacing: float = 60):
        self.node_width = node_width
        self.node_height = node_height
        self.horizontal_spacing = horizontal_spacing
        self.vertical_spacing = vertical_spacing
    
    def calculate_layout(self, tree: TokenTree) -> TreeLayout:
        """Calculate the layout for all nodes in the tree."""
        # Handle the case where tree might be a Reflex state variable
        # We cannot use boolean operations on state variables
        try:
            # Try to access tree properties - if this fails, return empty layout
            if hasattr(tree, 'root_id') and hasattr(tree, 'nodes'):
                root_id = tree.root_id
                nodes = tree.nodes
                
                # Check if we have valid data
                if not root_id or not nodes or root_id not in nodes:
                    return TreeLayout({}, 0, 0, [])
            else:
                return TreeLayout({}, 0, 0, [])
        except (AttributeError, TypeError):
            # If we can't access the tree properties, return empty layout
            return TreeLayout({}, 0, 0, [])
        
        # Group nodes by depth level
        levels = self._group_nodes_by_level(tree)
        
        # Calculate positions for each level
        node_positions = {}
        max_width = 0
        
        for level_index, level_nodes in enumerate(levels):
            y = level_index * (self.node_height + self.vertical_spacing)
            level_width = len(level_nodes) * (self.node_width + self.horizontal_spacing)
            max_width = max(max_width, level_width)
            
            # Center nodes in the level
            start_x = 0
            if len(level_nodes) > 1:
                start_x = 0
            
            for node_index, node_id in enumerate(level_nodes):
                x = start_x + node_index * (self.node_width + self.horizontal_spacing)
                node_positions[node_id] = NodePosition(x, y, node_id)
        
        total_height = len(levels) * (self.node_height + self.vertical_spacing)
        
        return TreeLayout(
            node_positions=node_positions,
            width=max_width,
            height=total_height,
            levels=levels
        )
    
    def _group_nodes_by_level(self, tree: TokenTree) -> List[List[str]]:
        """Group nodes by their depth level."""
        levels = []
        max_depth = 0
        
        try:
            # Safely access tree nodes
            nodes = tree.nodes if hasattr(tree, 'nodes') else {}
            if not nodes:
                return []
            
            # Find maximum depth
            for node in nodes.values():
                if hasattr(node, 'depth'):
                    max_depth = max(max_depth, node.depth)
            
            # Initialize levels
            for _ in range(max_depth + 1):
                levels.append([])
            
            # Group nodes by depth
            for node_id, node in nodes.items():
                if hasattr(node, 'depth') and 0 <= node.depth <= max_depth:
                    levels[node.depth].append(node_id)
                    
        except (AttributeError, TypeError, KeyError):
            # If we can't access the tree data, return empty levels
            return []
        
        return levels


def tree_node_svg(node: TreeNode, position: NodePosition, 
                  is_selected: bool = False, 
                  is_highlighted: bool = False,
                  on_click: Optional[rx.EventHandler] = None) -> rx.Component:
    """Create an SVG representation of a single tree node."""
    
    # Calculate colors based on probability
    bg_color = get_probability_background_color(node.probability)
    border_color = get_probability_color(node.probability)
    text_color = get_text_color(node.probability)
    
    # Adjust styling based on selection state
    if is_selected:
        border_width = "3"
        border_color = "#3B82F6"  # Blue-500
    elif is_highlighted:
        border_width = "2"
        border_color = "#6366F1"  # Indigo-500
    else:
        border_width = "1"
    
    # Node dimensions
    node_width = 120
    node_height = 40
    
    # Create the node group
    node_group = rx.fragment(
        # Background rectangle
        rx.el.rect(
            x=str(position.x),
            y=str(position.y),
            width=str(node_width),
            height=str(node_height),
            fill=bg_color,
            stroke=border_color,
            stroke_width=border_width,
            rx=str(8),  # Rounded corners
            ry=str(8),
            cursor="pointer" if on_click else "default",
            on_click=on_click
        ),
        # Token text
        rx.el.text(
            node.token[:15] + ("..." if len(node.token) > 15 else ""),  # Truncate long tokens
            x=str(position.x + node_width // 2),
            y=str(position.y + node_height // 2 - 5),
            text_anchor="middle",
            dominant_baseline="middle",
            fill=text_color,
            font_size="12",
            font_weight="600",
            cursor="pointer" if on_click else "default",
            on_click=on_click
        ),
        # Probability text
        rx.el.text(
            f"{node.probability:.1%}",
            x=str(position.x + node_width // 2),
            y=str(position.y + node_height // 2 + 8),
            text_anchor="middle",
            dominant_baseline="middle",
            fill=text_color,
            font_size="10",
            cursor="pointer" if on_click else "default",
            on_click=on_click
        )
    )
    
    return node_group


def tree_connection_svg(parent_pos: NodePosition, child_pos: NodePosition,
                       is_selected: bool = False) -> rx.Component:
    """Create an SVG line connection between parent and child nodes."""
    
    # Calculate connection points
    node_width = 120
    node_height = 40
    
    # Parent connection point (bottom center)
    parent_x = parent_pos.x + node_width // 2
    parent_y = parent_pos.y + node_height
    
    # Child connection point (top center)
    child_x = child_pos.x + node_width // 2
    child_y = child_pos.y
    
    # Line styling
    stroke_color = "#3B82F6" if is_selected else "#D1D5DB"  # Blue-500 or Gray-300
    stroke_width = "2" if is_selected else "1"
    
    return rx.el.line(
        x1=str(parent_x),
        y1=str(parent_y),
        x2=str(child_x),
        y2=str(child_y),
        stroke=stroke_color,
        stroke_width=stroke_width
    )


def tree_svg_container(tree: TokenTree, 
                      layout: TreeLayout,
                      selected_node_id: Optional[str] = None,
                      highlighted_node_id: Optional[str] = None,
                      on_node_click: Optional[rx.EventHandler] = None) -> rx.Component:
    """Create the complete SVG tree visualization."""
    
    # Create empty tree display component
    empty_tree_display = rx.box(
        rx.text("No tree data to display", color="gray.500"),
        width="100%",
        height="200px",
        display="flex",
        align_items="center",
        justify_content="center"
    )
    
    # Create SVG tree component
    def create_tree_svg():
        # This function will be called when we have valid tree data
        # For now, return a basic tree structure
        connections = []
        nodes = []
        
        try:
            # Safely access tree and layout data
            tree_nodes = tree.nodes if hasattr(tree, 'nodes') else {}
            layout_positions = layout.node_positions if hasattr(layout, 'node_positions') else {}
            
            # Create connections
            for node_id, node in tree_nodes.items():
                if (hasattr(node, 'parent_id') and node.parent_id and 
                    node.parent_id in layout_positions and node_id in layout_positions):
                    parent_pos = layout_positions[node.parent_id]
                    child_pos = layout_positions[node_id]
                    is_selected = (hasattr(node, 'is_selected') and node.is_selected and 
                                 hasattr(tree_nodes.get(node.parent_id, None), 'is_selected') and 
                                 tree_nodes[node.parent_id].is_selected)
                    
                    connections.append(
                        tree_connection_svg(parent_pos, child_pos, is_selected)
                    )
            
            # Create nodes
            for node_id, position in layout_positions.items():
                if node_id in tree_nodes:
                    node = tree_nodes[node_id]
                    is_selected = hasattr(node, 'is_selected') and node.is_selected
                    is_highlighted = node_id == highlighted_node_id
                    
                    # Create click handler if provided
                    click_handler = None
                    if on_node_click:
                        click_handler = lambda node_id=node_id: on_node_click(node_id)
                    
                    nodes.append(
                        tree_node_svg(node, position, is_selected, is_highlighted, click_handler)
                    )
            
            # Create the SVG element
            svg_width = max(getattr(layout, 'width', 400), 400)
            svg_height = max(getattr(layout, 'height', 200), 200)
            
            return rx.el.svg(
                *connections,
                *nodes,
                width=str(svg_width),
                height=str(svg_height),
                view_box=f"0 0 {svg_width} {svg_height}"
            )
            
        except (AttributeError, TypeError):
            return empty_tree_display
    
    return create_tree_svg()


def tree_controls(tree: TokenTree,
                 max_depth: int = 20,
                 max_branches: int = 10,
                 on_depth_change: Optional[rx.EventHandler] = None,
                 on_branches_change: Optional[rx.EventHandler] = None,
                 on_reset: Optional[rx.EventHandler] = None,
                 on_clear_branches: Optional[rx.EventHandler] = None) -> rx.Component:
    """Create control panel for tree manipulation."""
    
    return rx.box(
        rx.hstack(
            # Depth control
            rx.vstack(
                rx.text("Max Depth", font_size="0.875rem", font_weight="500"),
                rx.input(
                    type="number",
                    value=str(max_depth),
                    min="1",
                    max="50",
                    step="1",
                    width="80px",
                    on_change=on_depth_change
                ),
                spacing="1",
                align_items="start"
            ),
            
            # Branches control
            rx.vstack(
                rx.text("Max Branches", font_size="0.875rem", font_weight="500"),
                rx.input(
                    type="number",
                    value=str(max_branches),
                    min="1",
                    max="20",
                    step="1",
                    width="80px",
                    on_change=on_branches_change
                ),
                spacing="1",
                align_items="start"
            ),
            
            # Action buttons
            rx.hstack(
                rx.button(
                    "Reset Tree",
                    size="2",
                    variant="outline",
                    color_scheme="red",
                    on_click=on_reset
                ),
                rx.button(
                    "Clear Branches",
                    size="2",
                    variant="outline",
                    color_scheme="orange",
                    on_click=on_clear_branches
                ),
                spacing="2"
            ),
            
            spacing="4",
            align_items="end"
        ),
        padding="4",
        border="1px solid",
        border_color="gray.200",
        border_radius="8px",
        bg="gray.50"
    )


def tree_info_panel(tree: TokenTree, 
                   selected_node_id: Optional[str] = None) -> rx.Component:
    """Create information panel showing tree statistics and selected node info."""
    
    # Calculate tree statistics safely
    def get_tree_stats():
        try:
            nodes = tree.nodes if hasattr(tree, 'nodes') else {}
            total_nodes = len(nodes) if nodes else 0
            max_depth = max((getattr(node, 'depth', 0) for node in nodes.values()), default=0) if nodes else 0
            leaf_nodes = sum(1 for node in nodes.values() if getattr(node, 'is_leaf', False)) if nodes else 0
            return total_nodes, max_depth, leaf_nodes
        except (AttributeError, TypeError):
            return 0, 0, 0
    
    total_nodes, max_depth, leaf_nodes = get_tree_stats()
    
    # Selected node information
    def get_selected_node_info():
        try:
            if selected_node_id and hasattr(tree, 'nodes') and tree.nodes and selected_node_id in tree.nodes:
                return tree.nodes[selected_node_id]
        except (AttributeError, TypeError, KeyError):
            pass
        return None
    
    selected_node = get_selected_node_info()
    
    return rx.box(
        rx.vstack(
            rx.heading("Tree Information", size="4"),
            
            # Tree statistics
            rx.vstack(
                rx.text(f"Total Nodes: {total_nodes}", font_size="0.875rem"),
                rx.text(f"Max Depth: {max_depth}", font_size="0.875rem"),
                rx.text(f"Leaf Nodes: {leaf_nodes}", font_size="0.875rem"),
                spacing="1",
                align_items="start"
            ),
            
            # Selected node info - Use conditional rendering
            rx.cond(
                selected_node is not None,
                rx.vstack(
                    rx.heading("Selected Node", size="3"),
                    rx.text(f"Token: {getattr(selected_node, 'token', '') if selected_node else ''}", font_size="0.875rem"),
                    rx.text(f"Probability: {getattr(selected_node, 'probability', 0):.1%}" if selected_node else "", font_size="0.875rem"),
                    rx.text(f"Depth: {getattr(selected_node, 'depth', 0)}" if selected_node else "", font_size="0.875rem"),
                    rx.text(f"Children: {len(getattr(selected_node, 'children', []))}" if selected_node else "", font_size="0.875rem"),
                    spacing="1",
                    align_items="start"
                ),
                rx.text("No node selected", font_size="0.875rem", color="gray.500")
            ),
            
            spacing="4",
            align_items="start"
        ),
        padding="4",
        border="1px solid",
        border_color="gray.200",
        border_radius="8px",
        bg="white",
        width="250px"
    )


def tree_zoom_controls(zoom_level: float = 1.0,
                      on_zoom_in: Optional[rx.EventHandler] = None,
                      on_zoom_out: Optional[rx.EventHandler] = None,
                      on_zoom_reset: Optional[rx.EventHandler] = None) -> rx.Component:
    """Create zoom controls for the tree visualization."""
    
    return rx.hstack(
        rx.button(
            rx.icon("zoom-out"),
            size="2",
            variant="outline",
            on_click=on_zoom_out
        ),
        rx.text(f"{zoom_level:.1f}x", font_size="0.875rem", font_weight="500"),
        rx.button(
            rx.icon("zoom-in"),
            size="2",
            variant="outline",
            on_click=on_zoom_in
        ),
        rx.button(
            "Reset",
            size="2",
            variant="outline",
            on_click=on_zoom_reset
        ),
        spacing="2",
        align_items="center"
    )


def responsive_tree_container(tree: TokenTree, 
                            layout: TreeLayout,
                            zoom_level: float = 1.0,
                            selected_node_id: Optional[str] = None,
                            highlighted_node_id: Optional[str] = None,
                            on_node_click: Optional[rx.EventHandler] = None,
                            show_zoom_controls: bool = True) -> rx.Component:
    """Create a responsive container for the tree visualization with zoom and pan."""
    
    tree_svg = tree_svg_container(
        tree=tree,
        layout=layout,
        selected_node_id=selected_node_id,
        highlighted_node_id=highlighted_node_id,
        on_node_click=on_node_click
    )
    
    # Apply zoom transformation using rx.cond instead of if statement
    # This handles the case where zoom_level is a state variable
    tree_svg_with_zoom = rx.cond(
        zoom_level != 1.0,
        rx.box(
            tree_svg,
            transform=f"scale({zoom_level})",
            transform_origin="top left"
        ),
        tree_svg
    )
    
    return rx.vstack(
        # Zoom controls - conditional rendering
        rx.cond(
            show_zoom_controls,
            rx.hstack(
                tree_zoom_controls(zoom_level),
                justify_content="center",
                width="100%"
            )
        ),
        
        # Scrollable tree container
        rx.box(
            tree_svg_with_zoom,
            width="100%",
            height="600px",
            overflow="auto",
            border="1px solid",
            border_color="gray.200",
            border_radius="8px",
            bg="white"
        ),
        
        spacing="4",
        width="100%"
    )


def tree_path_display(tree: TokenTree) -> rx.Component:
    """Display the current selected path as a breadcrumb."""
    
    # Safely get selected path
    def get_selected_path():
        try:
            if hasattr(tree, 'selected_path') and tree.selected_path:
                return tree.selected_path
        except (AttributeError, TypeError):
            pass
        return []
    
    selected_path = get_selected_path()
    
    # Return early message if no path
    if not selected_path:
        return rx.text("No path selected", color="gray.500", font_size="0.875rem")
    
    # Build path elements safely
    def build_path_elements():
        path_elements = []
        try:
            nodes = tree.nodes if hasattr(tree, 'nodes') else {}
            
            for i, node_id in enumerate(selected_path):
                if node_id not in nodes:
                    continue
                    
                node = nodes[node_id]
                
                # Add separator between nodes (except for the first one)
                if i > 0:
                    path_elements.append(
                        rx.icon("chevron-right", size=16, color="gray.400")
                    )
                
                # Add node token
                token = getattr(node, 'token', 'Unknown')
                probability = getattr(node, 'probability', 0.0)
                
                # Truncate long tokens
                display_token = token[:20] + ("..." if len(token) > 20 else "")
                
                path_elements.append(
                    rx.text(
                        display_token,
                        font_size="0.875rem",
                        font_weight="500",
                        color=get_text_color(probability)
                    )
                )
        except (AttributeError, TypeError, KeyError):
            # If we can't build the path, return a simple message
            return [rx.text("Path data unavailable", color="gray.500", font_size="0.875rem")]
        
        return path_elements
    
    path_elements = build_path_elements()
    
    return rx.hstack(
        rx.text("Path:", font_size="0.875rem", font_weight="600", color="gray.700"),
        *path_elements,
        spacing="2",
        align_items="center",
        wrap="wrap"
    )
