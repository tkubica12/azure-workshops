"""Tree state management for the Interactive Token Tree mode."""
from typing import List, Dict, Any, Optional, Set
from datetime import datetime
import reflex as rx

from .base_state import BaseState
from ..services.llm_client import get_llm_client, TokenProbability, TokenGenerationResult
from ..utils.tree_structure import TokenTree, TreeNode


class TreeState(BaseState):
    """State management for token tree generation and visualization."""
    
    # Tree data structure
    tree: TokenTree = TokenTree()
    
    # Current session state
    initial_prompt: str = ""
    is_initialized: bool = False
    
    # Generation configuration
    max_depth: int = 20
    max_branches_per_node: int = 5
    temperature: float = 1.0
    top_k_alternatives: int = 5
    
    # UI state
    is_generating: bool = False
    current_error: str = ""
    has_error: bool = False
    
    # Progress tracking
    progress_message: str = ""
    has_progress_message: bool = False
    
    # Tree navigation state
    selected_node_id: str = ""
    hovered_node_id: str = ""
    
    # Tree visualization settings
    show_probabilities: bool = True
    show_branch_probabilities: bool = True
    compact_view: bool = False
    
    # Statistics (computed properties)
    total_nodes: int = 0
    current_depth: int = 0
    branch_count: int = 0
    leaf_count: int = 0
    
    def initialize_tree(self, prompt: str) -> None:
        """Initialize a new tree with the given prompt."""
        self.initial_prompt = prompt
        self.tree = TokenTree(max_depth=self.max_depth, max_branches_per_node=self.max_branches_per_node)
        root_id = self.tree.create_root(prompt)
        self.selected_node_id = root_id
        self.is_initialized = True
        self.clear_error()
        self._update_stats()
        self.mark_updated()
    
    def reset_tree(self) -> None:
        """Reset the current tree to just the root node."""
        if self.is_initialized:
            self.tree.reset_tree()
            self.selected_node_id = self.tree.root_id or ""
            self.clear_error()
            self._update_stats()
            self.mark_updated()
    
    def clear_tree(self) -> None:
        """Clear the entire tree and reset to uninitialized state."""
        self.tree = TokenTree()
        self.initial_prompt = ""
        self.is_initialized = False
        self.selected_node_id = ""
        self.hovered_node_id = ""
        self.clear_error()
        self._update_stats()
        self.mark_updated()
    
    @rx.event(background=True)
    async def generate_alternatives_for_node(self, node_id: str) -> None:
        """Generate token alternatives for the specified node."""
        async with self:
            if not self.is_initialized or node_id not in self.tree.nodes:
                self.set_error("Invalid node or tree not initialized")
                return
            
            self.is_generating = True
            self.set_progress("Generating token alternatives...")
        
        try:
            # Get the text path to this node
            path_text = self.tree.get_node_path_text(node_id)
            if not path_text:
                path_text = self.initial_prompt
            else:
                path_text = self.initial_prompt + path_text
            
            # Generate alternatives using LLM service
            client = await get_llm_client()
            result = await client.generate_tokens(
                prompt=path_text,
                max_tokens=1,
                temperature=self.temperature,
                top_logprobs=self.top_k_alternatives
            )
            
            async with self:
                if result.alternatives:
                    # Add alternatives to the tree
                    child_ids = self.tree.add_token_alternatives(node_id, result.alternatives)
                    
                    # Update selected node if this was extending the current path
                    if node_id == self.selected_node_id and child_ids:
                        self.selected_node_id = child_ids[0]
                    
                    self._update_stats()
                    self.clear_progress()
                    self.mark_updated()
                else:
                    self.set_error("No alternatives generated")
                    
        except Exception as e:
            async with self:
                self.set_error(f"Generation failed: {str(e)}")
        finally:
            async with self:
                self.is_generating = False
    
    @rx.event(background=True)
    async def generate_alternatives_for_current_node(self) -> None:
        """Generate alternatives for the currently selected node."""
        await self.generate_alternatives_for_node(self.selected_node_id)
    
    @rx.event(background=True)
    async def create_branch_from_node(self, node_id: str) -> None:
        """Create a new branch starting from the specified node."""
        async with self:
            if not self.is_initialized or node_id not in self.tree.nodes:
                self.set_error("Invalid node or tree not initialized")
                return
            
            self.is_generating = True
            self.set_progress("Creating new branch...")
        
        try:
            # Get the text path to this node
            path_text = self.tree.get_node_path_text(node_id)
            if not path_text:
                path_text = self.initial_prompt
            else:
                path_text = self.initial_prompt + path_text
            
            # Generate alternatives using LLM service
            client = await get_llm_client()
            result = await client.generate_tokens(
                prompt=path_text,
                max_tokens=1,
                temperature=self.temperature,
                top_logprobs=self.top_k_alternatives
            )
            
            async with self:
                if result.alternatives:
                    # Create branch from the specified node
                    child_ids = self.tree.create_branch_from_node(node_id, result.alternatives)
                    self._update_stats()
                    self.clear_progress()
                    self.mark_updated()
                else:
                    self.set_error("No alternatives generated for branch")
                    
        except Exception as e:
            async with self:
                self.set_error(f"Branch creation failed: {str(e)}")
        finally:
            async with self:
                self.is_generating = False
    
    def select_node(self, node_id: str) -> None:
        """Select a node and update the selected path."""
        if self.is_initialized and node_id in self.tree.nodes:
            success = self.tree.select_path_to_node(node_id)
            if success:
                self.selected_node_id = node_id
                self._update_stats()
                self.mark_updated()
    
    def hover_node(self, node_id: str) -> None:
        """Set the hovered node for UI feedback."""
        self.hovered_node_id = node_id
    
    def clear_hover(self) -> None:
        """Clear the hovered node."""
        self.hovered_node_id = ""
    
    def delete_subtree(self, node_id: str) -> None:
        """Delete a subtree starting from the specified node."""
        if self.is_initialized and node_id in self.tree.nodes and node_id != self.tree.root_id:
            deleted_ids = self.tree.delete_subtree(node_id)
            
            # Update selected node if it was deleted
            if self.selected_node_id in deleted_ids:
                self.selected_node_id = self.tree.current_node_id or ""
            
            self._update_stats()
            self.mark_updated()
    
    def get_current_node(self) -> Optional[TreeNode]:
        """Get the currently selected node."""
        if self.selected_node_id and self.selected_node_id in self.tree.nodes:
            return self.tree.nodes[self.selected_node_id]
        return None
    
    def get_node(self, node_id: str) -> Optional[TreeNode]:
        """Get a specific node by ID."""
        return self.tree.nodes.get(node_id)
    
    def get_children_of_node(self, node_id: str) -> List[TreeNode]:
        """Get all children of the specified node."""
        return self.tree.get_children(node_id)
    
    def get_siblings_of_node(self, node_id: str) -> List[TreeNode]:
        """Get all siblings of the specified node."""
        return self.tree.get_siblings(node_id)
    
    def get_selected_path_text(self) -> str:
        """Get the complete text of the selected path."""
        if self.is_initialized:
            return self.tree.get_selected_path_text()
        return ""
    
    def get_node_path_text(self, node_id: str) -> str:
        """Get the complete text path to a specific node."""
        if self.is_initialized:
            full_text = self.tree.get_node_path_text(node_id)
            return self.initial_prompt + full_text
        return ""
    
    def get_all_nodes(self) -> List[TreeNode]:
        """Get all nodes in the tree."""
        return list(self.tree.nodes.values())
    
    def get_nodes_at_depth(self, depth: int) -> List[TreeNode]:
        """Get all nodes at the specified depth."""
        return self.tree.get_nodes_at_depth(depth)
    
    def get_branch_roots(self) -> List[TreeNode]:
        """Get all nodes that are branch roots."""
        return self.tree.get_branch_roots()
    
    def get_leaf_nodes(self) -> List[TreeNode]:
        """Get all leaf nodes in the tree."""
        return self.tree.get_leaf_nodes()
    
    def can_generate_from_node(self, node_id: str) -> bool:
        """Check if we can generate alternatives from the specified node."""
        if not self.is_initialized or node_id not in self.tree.nodes:
            return False
        
        node = self.tree.nodes[node_id]
        return (
            node.depth < self.max_depth and
            len(node.children) == 0 and  # No existing children
            not self.is_generating
        )
    
    def can_create_branch_from_node(self, node_id: str) -> bool:
        """Check if we can create a branch from the specified node."""
        if not self.is_initialized or node_id not in self.tree.nodes:
            return False
        
        node = self.tree.nodes[node_id]
        return (
            node.depth < self.max_depth and
            not self.is_generating
        )
    
    def update_configuration(self, 
                           max_depth: Optional[int] = None,
                           max_branches: Optional[int] = None,
                           temperature: Optional[float] = None,
                           top_k: Optional[int] = None) -> None:
        """Update tree generation configuration."""
        if max_depth is not None:
            self.max_depth = max(1, min(50, max_depth))
            if self.is_initialized:
                self.tree.max_depth = self.max_depth
        
        if max_branches is not None:
            self.max_branches_per_node = max(1, min(20, max_branches))
            if self.is_initialized:
                self.tree.max_branches_per_node = self.max_branches_per_node
        
        if temperature is not None:
            self.temperature = max(0.0, min(2.0, temperature))
        
        if top_k is not None:
            self.top_k_alternatives = max(1, min(20, top_k))
        
        self.mark_updated()
    
    def toggle_view_setting(self, setting: str) -> None:
        """Toggle a view setting."""
        if setting == "probabilities":
            self.show_probabilities = not self.show_probabilities
        elif setting == "branch_probabilities":
            self.show_branch_probabilities = not self.show_branch_probabilities
        elif setting == "compact":
            self.compact_view = not self.compact_view
        
        self.mark_updated()
    
    def set_error(self, message: str) -> None:
        """Set an error message."""
        self.current_error = message
        self.has_error = bool(message)
        self.clear_progress()
    
    def clear_error(self) -> None:
        """Clear the current error."""
        self.current_error = ""
        self.has_error = False
    
    def set_progress(self, message: str) -> None:
        """Set a progress message."""
        self.progress_message = message
        self.has_progress_message = bool(message)
        self.clear_error()
    
    def clear_progress(self) -> None:
        """Clear the progress message."""
        self.progress_message = ""
        self.has_progress_message = False
    
    def _update_stats(self) -> None:
        """Update tree statistics."""
        if self.is_initialized:
            stats = self.tree.get_tree_stats()
            self.total_nodes = stats["total_nodes"]
            self.current_depth = stats["current_depth"]
            self.branch_count = stats["branch_count"]
            self.leaf_count = stats["leaf_count"]
        else:
            self.total_nodes = 0
            self.current_depth = 0
            self.branch_count = 0
            self.leaf_count = 0


# Utility functions for testing
def create_sample_tree_state() -> TreeState:
    """Create a sample tree state for testing."""
    state = TreeState()
    state.initialize_tree("The capital of France is")
    return state


async def test_tree_operations() -> Dict[str, Any]:
    """Test basic tree operations and return results."""
    results = {
        "tree_creation": False,
        "node_addition": False,
        "path_selection": False,
        "branch_creation": False,
        "tree_statistics": {},
        "errors": []
    }
    
    try:
        # Test tree creation
        state = TreeState()
        state.initialize_tree("Hello world")
        results["tree_creation"] = state.is_initialized
        
        # Test getting current node
        current_node = state.get_current_node()
        if current_node and current_node.token == "Hello world":
            results["node_addition"] = True
        
        # Test path selection (using root node)
        if state.tree.root_id:
            state.select_node(state.tree.root_id)
            results["path_selection"] = state.selected_node_id == state.tree.root_id
        
        # Test statistics
        results["tree_statistics"] = {
            "total_nodes": state.total_nodes,
            "current_depth": state.current_depth,
            "is_initialized": state.is_initialized
        }
        
    except Exception as e:
        results["errors"].append(str(e))
    
    return results
