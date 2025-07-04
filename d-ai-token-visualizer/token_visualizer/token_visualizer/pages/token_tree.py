"""Token Tree mode - Interactive tree visualization of token probabilities."""

import reflex as rx
import plotly.graph_objects as go
import networkx as nx
import traceback
from typing import List, Dict, Optional, Set
from datetime import datetime

from ..components.layout import app_layout
from ..services.llm_client import get_llm_client, TokenProbability
from ..utils.tree_structure import TokenTree, TreeNode


class TokenTreeState(rx.State):
    """State for the Token Tree mode."""
    
    # User input
    user_prompt: str = ""
    
    # Tree data
    tree: Optional[TokenTree] = None
    tree_figure: Optional[go.Figure] = None
    selected_node_id: Optional[str] = None  # Track selected node for expansion
    
    # Generation state
    is_generating: bool = False
    has_generated: bool = False
    is_expanding: bool = False  # Track if we're expanding a node
    
    # Error handling
    error_message: str = ""
    has_error: bool = False
    
    # Temperature setting (fixed for now)
    temperature: float = 1.0
    
    # Point mapping for click events (since customdata doesn't always work)
    point_to_node_mapping: List[str] = []  # Maps point index to node_id
    
    def clear_error(self):
        """Clear any existing error state."""
        self.error_message = ""
        self.has_error = False
    
    def set_error(self, message: str):
        """Set an error message."""
        self.error_message = message
        self.has_error = True
        self.is_generating = False

    def debug_click_handler(self):
        """Debug method to test click handling."""
        print("INFO: Debug click handler called - click detection working!")
        if self.tree and self.tree.nodes:
            # Try to expand the first leaf node we find
            for node_id, node in self.tree.nodes.items():
                if len(node.children) == 0 and node.depth > 0:  # Skip root node
                    print(f"INFO: Debug expanding node '{node.token}' (ID: {node_id})")
                    return self.expand_node(node_id)
        print("INFO: No expandable nodes found for debug test")
    
    @rx.event(background=True)
    async def generate_tree(self):
        """Generate the initial tree with prompt and next 5 token alternatives."""
        if not self.user_prompt.strip():
            async with self:
                self.set_error("Please enter a prompt first")
            return
        
        async with self:
            self.is_generating = True
            self.clear_error()
        
        try:
            # Get LLM client
            client = await get_llm_client()
            
            async with self:
                # Create new tree with the prompt as root
                self.tree = TokenTree(max_depth=100, max_branches_per_node=5)  # Very high max_depth for unlimited expansion
                root_id = self.tree.create_root(self.user_prompt.strip())
                
                print(f"INFO: Generating token tree for prompt: '{self.user_prompt.strip()}'")
            
            # Generate next 5 token alternatives
            result = await client.generate_tokens_with_probabilities(
                prompt=self.user_prompt.strip(),
                max_tokens=1,
                temperature=self.temperature,
                top_logprobs=5  # Get top 5 alternatives
            )
            
            # Add alternatives as children of root
            if result.alternatives:
                async with self:
                    child_ids = self.tree.add_token_alternatives(root_id, result.alternatives)
                    print(f"INFO: Added {len(child_ids)} token alternatives to tree")
                
                    # Update tree visualization
                    self.update_tree_figure()
                    
                    self.has_generated = True
                    self.is_generating = False
        
        except Exception as e:
            print(f"ERROR: Failed to generate tree: {str(e)}")
            async with self:
                self.set_error(f"Failed to generate tree: {str(e)}")
    
    def update_tree_figure(self):
        """Update the Plotly tree figure."""
        if not self.tree or not self.tree.nodes:
            return
        
        try:
            # Get only visible nodes (not collapsed by their parent)
            visible_nodes = self.tree.get_visible_nodes()
            
            # Create NetworkX graph with only visible nodes
            G = nx.DiGraph()
            
            # Group visible nodes by depth level for hierarchical layout
            levels = {}
            for node_id in visible_nodes:
                node = self.tree.nodes[node_id]
                depth = node.depth
                if depth not in levels:
                    levels[depth] = []
                levels[depth].append(node_id)
            
            # Position nodes manually for left-to-right hierarchy
            pos = {}
            x_spacing = 4.0  # Horizontal spacing between levels
            y_spacing = 1.5  # Vertical spacing between nodes at same level (reduced for rectangles)
            
            for depth, node_ids in levels.items():
                x = depth * x_spacing
                # Center nodes vertically within each level
                total_height = (len(node_ids) - 1) * y_spacing
                start_y = -(total_height / 2)
                
                for i, node_id in enumerate(node_ids):
                    y = start_y + (i * y_spacing)
                    pos[node_id] = (x, y)
            
            # Add visible nodes and edges to NetworkX graph
            for node_id in visible_nodes:
                node = self.tree.nodes[node_id]
                G.add_node(node_id, 
                          text=node.token if node.token else "ROOT",
                          probability=node.probability * 100 if node.probability else 100.0,
                          is_selected=getattr(node, 'is_selected', False))
                
                # Add edges to visible children only
                for child_id in node.children:
                    if child_id in visible_nodes:
                        G.add_edge(node_id, child_id)
            
            # Create edge traces
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
            
            # Create node traces with color coding based on probability
            node_colors = []
            node_border_colors = []
            node_text = []
            hover_text = []
            node_sizes = []
            
            for node_id in G.nodes():
                node = self.tree.nodes[node_id]
                token_text = node.token if node.token else "ROOT"
                probability = node.probability * 100 if node.probability else 100.0
                
                # Handle long text - use multiline wrapping for root node
                if node.depth == 0:  # Root node (prompt)
                    # Break text into multiple lines for better display
                    words = token_text.split()
                    lines = []
                    current_line = ""
                    max_chars_per_line = 20  # Characters per line
                    max_lines = 3  # Maximum lines in root node
                    
                    for word in words:
                        # Check if adding this word would exceed line length
                        test_line = current_line + (" " if current_line else "") + word
                        if len(test_line) <= max_chars_per_line:
                            current_line = test_line
                        else:
                            # Start new line
                            if current_line:
                                lines.append(current_line)
                            current_line = word
                            
                            # Stop if we've reached max lines
                            if len(lines) >= max_lines:
                                break
                    
                    # Add the last line
                    if current_line and len(lines) < max_lines:
                        lines.append(current_line)
                    
                    # If text was truncated, add "..." to last line
                    if len(lines) == max_lines and len(words) > len(" ".join(lines).split()):
                        if len(lines) > 0:
                            lines[-1] = lines[-1][:max_chars_per_line-3] + "..."
                    
                    display_text = "<br>".join(lines)  # Use HTML line breaks for Plotly
                    node_size = 180  # Larger root node for multiline text with better readability
                    full_text = token_text  # Keep full text for hover
                else:
                    # Token nodes - usually short, but handle edge cases
                    display_text = token_text if len(token_text) <= 12 else token_text[:10] + "..."
                    node_size = 100  # Larger token nodes for better text visibility
                    full_text = token_text
                
                # Use same color scheme as Interactive Generation page
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
                
                node_colors.append(bg_color)
                node_border_colors.append(border_color)
                node_text.append(display_text)  # Use truncated text for display
            # Create edge trace
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
            
            # Collect node data for the trace
            node_text = []
            hover_text = []
            node_colors = []
            node_border_colors = []
            node_sizes = []
            node_order = list(G.nodes())  # Keep track of node order for point mapping
            
            # Update the point to node mapping for click events
            self.point_to_node_mapping = node_order
            
            for node_id in node_order:
                node = self.tree.nodes[node_id]
                token_text = node.token if node.token else "ROOT"
                probability = node.probability * 100 if node.probability else 100.0
                
                # Handle text truncation and sizing
                if node.depth == 0:  # Root node - just display "prompt"
                    display_text = "prompt"
                    node_size = 80  # Same size as token nodes
                    full_text = token_text  # Keep full text for hover
                else:
                    # Token nodes
                    display_text = token_text if len(token_text) <= 12 else token_text[:10] + "..."
                    node_size = 80  # Standard token node size
                    full_text = token_text
                
                # Color scheme matching Interactive Generation
                if probability >= 80:
                    bg_color = '#D1FAE5'
                    border_color = '#10B981'
                elif probability >= 60:
                    bg_color = '#ECFDF5'
                    border_color = '#34D399'
                elif probability >= 40:
                    bg_color = '#FEF3C7'
                    border_color = '#FCD34D'
                elif probability >= 20:
                    bg_color = '#FEF3C7'
                    border_color = '#F59E0B'
                elif probability >= 10:
                    bg_color = '#FED7AA'
                    border_color = '#F97316'
                else:
                    bg_color = '#FEE2E2'
                    border_color = '#EF4444'
                
                # Note: Node selection will be implemented later
                
                node_colors.append(bg_color)
                node_border_colors.append(border_color)
                node_text.append(display_text)
                node_sizes.append(node_size)
                
                if node.depth == 0:
                    hover_text.append(f"Prompt: {full_text}<br>Root Node")
                else:
                    # Check if this node has children (can be collapsed/expanded) or is a leaf (can be expanded)
                    has_children = len(node.children) > 0
                    if has_children:
                        if node.is_collapsed:
                            hover_text.append(f"Token: {full_text}<br>Probability: {probability:.1f}%<br>📁 Click to expand collapsed subtree")
                        else:
                            hover_text.append(f"Token: {full_text}<br>Probability: {probability:.1f}%<br>📂 Click to collapse subtree")
                    else:
                        # Leaf node - can be expanded with LLM
                        hover_text.append(f"Token: {full_text}<br>Probability: {probability:.1f}%<br>🎯 Click to expand (add next tokens)")
            
            # Create invisible node trace for hover and click functionality
            node_trace = go.Scatter(
                x=[pos[node][0] for node in node_order],
                y=[pos[node][1] for node in node_order],
                mode='markers',
                hovertext=hover_text,
                hoverinfo='text',
                marker=dict(
                    size=node_sizes,
                    color='rgba(0,0,0,0)',  # Transparent markers
                    line=dict(width=0),
                    opacity=0
                ),
                name="Token Nodes",
                showlegend=False
            )
            
            # Create figure with edge trace and invisible node trace
            fig = go.Figure(data=[edge_trace, node_trace])
            
            # Ensure y_range exists for pixel scaling
            if pos:
                y_coords = [coord[1] for coord in pos.values()]
                y_min, y_max = min(y_coords), max(y_coords)
                y_padding = 1.0  # Padding in data units
                y_range = [y_min - y_padding, y_max + y_padding]
            else:
                y_range = [-2, 2]

            # Calculate pixel-per-unit for vertical scaling
            fig_height_px = fig.layout.height if fig.layout.height else 600
            # y_range now defined
            y_span = y_range[1] - y_range[0] if pos else 1
            y_unit_to_px = fig_height_px / y_span

            # Add rectangular shapes and text for each node
            text_annotations = []
            for i, node_id in enumerate(node_order):
                node = self.tree.nodes[node_id]
                x, y = pos[node_id]
                
                # Define rectangle size based on node type - uniform sizing for all nodes
                # Base rectangle size in data units for all nodes
                base_width, base_height = 1.5, 0.6
                height = base_height
                # Compute width based on character count with minimal padding
                max_chars = max((len(line) for line in node_text[i].split("<br>")), default=1)
                # Approximate data-unit width per character (fit 6 chars in base width)
                char_unit = base_width / 6
                padding_units = 0.1
                width = max(base_width, max_chars * char_unit + padding_units)

                # Compute dynamic font size from rectangle height
                pixel_height = height * y_unit_to_px
                font_size = int(pixel_height * 0.6)  # Standard font size for all nodes
                # Clamp font size
                font_size = max(8, min(font_size, 20))

                # Add rectangular shape
                fig.add_shape(
                    type="rect",
                    x0=x - width/2, y0=y - height/2,
                    x1=x + width/2, y1=y + height/2,
                    fillcolor=node_colors[i],
                    line=dict(color=node_border_colors[i], width=2),
                    opacity=0.95
                )
                
                # Add collapse indicator for nodes with children
                if len(node.children) > 0 and node.depth > 0:  # Skip root node
                    # Add small circle indicator in the bottom-right corner
                    indicator_x = x + width/2 - 0.15
                    indicator_y = y - height/2 + 0.15
                    indicator_color = "#4F46E5" if node.is_collapsed else "#10B981"
                    indicator_symbol = "+" if node.is_collapsed else "−"
                    
                    fig.add_shape(
                        type="circle",
                        x0=indicator_x - 0.1, y0=indicator_y - 0.1,
                        x1=indicator_x + 0.1, y1=indicator_y + 0.1,
                        fillcolor=indicator_color,
                        line=dict(color="white", width=1),
                        opacity=0.9
                    )
                    
                    # Add +/- symbol
                    text_annotations.append(dict(
                        x=indicator_x,
                        y=indicator_y,
                        text=indicator_symbol,
                        showarrow=False,
                        font=dict(size=10, color="white", family="Arial, sans-serif"),
                        align="center",
                        valign="middle",
                        xref="x",
                        yref="y"
                    ))
                
                # Prepare main text annotation
                text_annotations.append(dict(
                    x=x,
                    y=y,
                    text=node_text[i],
                    showarrow=False,
                    font=dict(size=font_size, color='#1F2937', family="Arial, sans-serif"),
                    align="center",
                    valign="middle",
                    xref="x",
                    yref="y"
                ))
            # Add the instruction annotation to the text annotations list
            instruction_text = "💡 Hover for details • Click leaf nodes to expand • Click nodes with children to collapse/expand"
            
            text_annotations.append(dict(
                text=instruction_text,
                showarrow=False,
                xref="paper", yref="paper",
                x=0.5, y=-0.05,
                xanchor='center', yanchor='top',
                font=dict(size=13, color="gray", family="Arial, sans-serif")
            ))
            
            # Calculate bounds of all node positions to maintain rectangle sizes
            if pos:
                x_coords = [pos[node][0] for node in pos]
                y_coords = [pos[node][1] for node in pos]
                
                x_min, x_max = min(x_coords), max(x_coords)
                y_min, y_max = min(y_coords), max(y_coords)
                
                # Add padding around the bounds (accounting for rectangle sizes)
                # All nodes now use similar dynamic sizing (max ~1.5-3.0 width)
                x_padding = 2.0  # Max expected rectangle width/2 + extra space
                y_padding = 1.0  # Max rectangle height/2 + extra space
                
                x_range = [x_min - x_padding, x_max + x_padding]
                y_range = [y_min - y_padding, y_max + y_padding]
            else:
                # Fallback ranges if no positions
                x_range = [-2, 2]
                y_range = [-2, 2]
            
            # Create title with truncated prompt
            if self.user_prompt:
                # Truncate prompt for title display
                max_title_chars = 60
                if len(self.user_prompt) > max_title_chars:
                    title_text = f"{self.user_prompt[:max_title_chars]}..."
                else:
                    title_text = f"{self.user_prompt}..."
            else:
                title_text = f"Token Tree ({len(G.nodes())} nodes)"
            
            fig.update_layout(
                title=dict(
                    text=title_text,
                    x=0.5,
                    font=dict(size=18, family="Arial, sans-serif")
                ),
                showlegend=False,
                hovermode='closest',
                dragmode='pan',  # Set Pan as the default tool
                margin=dict(b=40, l=40, r=40, t=60, autoexpand=True),
                annotations=text_annotations,  # Add all annotations at once
                xaxis=dict(
                    showgrid=False, 
                    zeroline=False, 
                    showticklabels=False,
                    fixedrange=False,
                    range=x_range,  # Set explicit range based on data bounds
                    scaleanchor="y",  # Maintain aspect ratio
                    scaleratio=1
                ),
                yaxis=dict(
                    showgrid=False, 
                    zeroline=False, 
                    showticklabels=False,
                    fixedrange=False,
                    range=y_range  # Set explicit range based on data bounds
                ),
                modebar=dict(
                    remove=["select", "lasso"]  # Remove box select and lasso select tools
                ),
                plot_bgcolor='#FAFAFA',
                paper_bgcolor='white',
                height=600,
                autosize=True
            )
            
            self.tree_figure = fig
        
        except Exception as e:
            print(f"ERROR: Failed to update tree figure: {str(e)}")
            self.set_error(f"Failed to create visualization: {str(e)}")
    
    def get_path_to_node(self, node_id: str) -> str:
        """Build the full text path from root to the specified node."""
        if not self.tree or node_id not in self.tree.nodes:
            return ""
        
        # Build path from node back to root
        path_nodes = []
        current_id = node_id
        
        while current_id is not None:
            node = self.tree.nodes[current_id]
            path_nodes.append(node)
            current_id = node.parent_id
        
        # Reverse to get root-to-node path
        path_nodes.reverse()
        
        # Combine tokens to create full prompt
        if len(path_nodes) == 1:
            # Root node only
            return path_nodes[0].token
        else:
            # Root prompt + selected tokens
            root_text = path_nodes[0].token
            selected_tokens = [node.token for node in path_nodes[1:]]
            return root_text + "".join(selected_tokens)
    
    @rx.event(background=True)
    async def expand_node(self, node_id: str):
        """Expand a leaf node by generating next token alternatives."""
        if not self.tree or node_id not in self.tree.nodes:
            return
        
        node = self.tree.nodes[node_id]
        
        # Only expand leaf nodes (nodes with no children)
        if len(node.children) > 0:
            return
        
        async with self:
            self.is_expanding = True
            self.selected_node_id = node_id
            self.clear_error()
        
        try:
            # Get LLM client
            client = await get_llm_client()
            
            # Build the prompt path from root to this node
            prompt_path = self.get_path_to_node(node_id)
            
            print(f"INFO: Expanding node '{node.token}' with path: '{prompt_path}'")
            
            # Generate next 5 token alternatives
            result = await client.generate_tokens_with_probabilities(
                prompt=prompt_path,
                max_tokens=1,
                temperature=self.temperature,
                top_logprobs=5  # Get top 5 alternatives
            )
            
            # Add alternatives as children of the clicked node
            if result.alternatives:
                async with self:
                    child_ids = self.tree.add_token_alternatives(node_id, result.alternatives)
                    print(f"INFO: Added {len(child_ids)} token alternatives to node '{node.token}'")
                
                    # Update tree visualization
                    self.update_tree_figure()
                    
                    self.is_expanding = False
        
        except Exception as e:
            print(f"ERROR: Failed to expand node: {str(e)}")
            async with self:
                self.set_error(f"Failed to expand node: {str(e)}")
                self.is_expanding = False
    
    @rx.event(background=True)
    async def handle_node_click(self, event: list):
        """Handle clicks on tree nodes to expand leaf nodes or collapse/expand parent nodes."""
        print(f"INFO: Node click detected - event data: {event}")

        try:
            point_index = -1
            if event and isinstance(event, list) and len(event) > 0 and isinstance(event[0], dict):
                event_data = event[0]
                # Ensure we are clicking on the correct trace (nodes, not edges)
                if event_data.get("curveNumber") != 1:
                    print(f"INFO: Clicked on wrong trace (curveNumber: {event_data.get('curveNumber')}), ignoring.")
                    return
                point_index = event_data.get("pointIndex", -1)

            if point_index == -1:
                print(f"WARNING: Could not extract valid point index from event: {event}")
                return

            node_id = ""
            node_token = ""
            has_children = False
            async with self:
                if not (0 <= point_index < len(self.point_to_node_mapping)):
                    print(f"WARNING: Point index {point_index} out of range.")
                    return
                
                node_id = self.point_to_node_mapping[point_index]
                if not self.tree or node_id not in self.tree.nodes:
                    print(f"WARNING: Node ID '{node_id}' not found in tree.")
                    return

                node = self.tree.nodes[node_id]
                node_token = node.token
                has_children = len(node.children) > 0
                print(f"INFO: User clicked on node '{node_token}' (ID: {node_id}, Children: {len(node.children)})")

                if has_children:
                    self.tree.toggle_node_collapse(node_id)
                    self.update_tree_figure()
                    print(f"INFO: Toggled collapse state for node '{node_token}'. Is collapsed: {node.is_collapsed}")
                    return

            if has_children: # Should not happen due to return, but as a safeguard
                return

            if self.is_expanding:
                print("INFO: Already expanding a node, ignoring click.")
                return

            async with self:
                self.is_expanding = True
                self.selected_node_id = node_id
                self.clear_error()

            try:
                client = await get_llm_client()
                prompt_path = self.get_path_to_node(node_id)
                print(f"INFO: Expanding leaf node '{node_token}' with path: '{prompt_path}'")

                result = await client.generate_tokens_with_probabilities(
                    prompt=prompt_path, max_tokens=1, temperature=self.temperature, top_logprobs=5
                )

                async with self:
                    if result.alternatives:
                        child_ids = self.tree.add_token_alternatives(node_id, result.alternatives)
                        print(f"INFO: Added {len(child_ids)} token alternatives to node '{node_token}'")
                        self.update_tree_figure()
                    else:
                        print(f"WARNING: No alternatives returned for node '{node_token}'")
                    self.is_expanding = False
            except Exception as e:
                print(f"ERROR: Failed to expand node '{node_token}': {str(e)}")
                async with self:
                    self.set_error(f"Failed to expand node: {str(e)}")
                    self.is_expanding = False
        except Exception as e:
            print(f"ERROR: Failed to handle node click: {str(e)}")
            import traceback
            print(f"DEBUG: Traceback: {traceback.format_exc()}")
            async with self:
                self.set_error(f"Click handling failed: {str(e)}")
                self.is_expanding = False


def prompt_input_section() -> rx.Component:
    """Compact input section for entering the initial prompt."""
    return rx.vstack(
        # Header
        rx.vstack(
            rx.heading("Token Tree", size="5", margin_bottom="0.25rem"),
            rx.text(
                "Enter a prompt to visualize the most likely next tokens as an interactive tree.",
                color="#6B7280",
                font_size="0.875rem"
            ),
            spacing="1",
            align="start",
            width="100%"
        ),
        
        # Text input and button in horizontal layout
        rx.hstack(
            rx.text_area(
                placeholder="Enter your prompt here (e.g., 'The weather today is')",
                value=TokenTreeState.user_prompt,
                on_change=TokenTreeState.set_user_prompt,
                width="100%",
                height="60px",  # Compact height
                resize="vertical",
                font_size="0.875rem",
                border="1px solid #D1D5DB",
                border_radius="6px",
                padding="0.5rem",
                _focus={
                    "border_color": "#3B82F6",
                    "box_shadow": "0 0 0 2px rgba(59, 130, 246, 0.1)"
                }
            ),
            rx.button(
                rx.cond(
                    TokenTreeState.is_generating,  # Animate only when generating
                    rx.hstack(
                        rx.spinner(size="2"),
                        rx.text("Generating..."),
                        spacing="1",
                        align="center"
                    ),
                    rx.hstack(
                        rx.icon("git-branch", size=14),
                        rx.text("Generate Tree"),
                        spacing="1",
                        align="center"
                    )
                ),
                on_click=TokenTreeState.generate_tree,
                disabled=TokenTreeState.is_generating | TokenTreeState.is_expanding, # Keep disabled during expansion
                size="3",
                variant="solid",
                color_scheme="blue",
                height="60px",  # Match text area height
                white_space="nowrap",
                min_width="140px",
                flex_shrink="0"
            ),
            spacing="2",
            align="stretch",
            width="100%"
        ),
        
        # Error display (compact)
        rx.cond(
            TokenTreeState.has_error,
            rx.callout(
                TokenTreeState.error_message,
                icon="triangle_alert",
                color_scheme="red",
                variant="soft",
                size="1"  # Smaller callout
            )
        ),
        
        spacing="2",  # Reduced spacing
        align="stretch",
        width="100%"
    )


def tree_visualization_section() -> rx.Component:
    """Tree visualization section."""
    return rx.cond(
        TokenTreeState.has_generated,
        rx.vstack(
            rx.divider(),
            rx.hstack(
                rx.heading("Token Tree Visualization", size="4"),
                rx.cond(
                    TokenTreeState.is_expanding,
                    rx.hstack(
                        rx.spinner(size="2"),
                        rx.text("Expanding node...", color="#6B7280", font_size="0.875rem"),
                        spacing="1",
                        align="center"
                    )
                ),
                justify="between",
                align="center",
                width="100%",
                margin_bottom="1rem"
            ),
            
            # Tree visualization
            rx.box(
                rx.plotly(
                    data=TokenTreeState.tree_figure,
                    style={"width": "100%", "height": "600px"},
                    on_click=TokenTreeState.handle_node_click  # Simplified click handler
                ),
                width="100%",
                border="1px solid #E5E7EB",
                border_radius="8px",
                overflow="hidden"
            ),
            
            spacing="4",
            align="stretch",
            width="100%"
        ),
        rx.box()  # Empty box when no tree generated yet
    )


@rx.page(route="/token-tree", title="Token Tree | Token Visualizer")
def token_tree_page() -> rx.Component:
    """Token Tree mode page."""
    return app_layout(
        rx.container(
            rx.vstack(
                prompt_input_section(),
                tree_visualization_section(),
                spacing="3",  # Reduced spacing
                align="stretch",
                width="100%",
                padding="1rem 0"  # Reduced padding
            ),
            max_width="100%",  # Use full width
            padding="0 0.5rem"  # Minimal horizontal padding
        )
    )
