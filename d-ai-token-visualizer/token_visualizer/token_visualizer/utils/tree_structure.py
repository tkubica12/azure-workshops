"""Tree data structure for token tree visualization."""
from typing import List, Dict, Optional, Any, Set
from dataclasses import dataclass, field
from datetime import datetime
import uuid

from ..services.llm_client import TokenProbability


@dataclass
class TreeNode:
    """Represents a node in the token tree with branching capabilities."""
    
    # Node identification
    node_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    
    # Token information
    token: str = ""
    probability: float = 0.0
    
    # Tree structure
    parent_id: Optional[str] = None
    children: List[str] = field(default_factory=list)  # Store child node IDs
    
    # Position in generation sequence
    depth: int = 0  # 0 for root, 1 for first token, etc.
    position_in_parent: int = 0  # Index among siblings
    
    # Path information
    is_selected: bool = False  # Part of the main/selected path
    is_branch_root: bool = False  # Starting point of a branch
    
    # Metadata
    created_at: datetime = field(default_factory=datetime.now)
    generation_metadata: Dict[str, Any] = field(default_factory=dict)
    
    @property
    def is_leaf(self) -> bool:
        """Check if this node is a leaf (has no children)."""
        return len(self.children) == 0
    
    @property
    def is_root(self) -> bool:
        """Check if this node is the root (has no parent)."""
        return self.parent_id is None
    
    def add_child(self, child_id: str) -> None:
        """Add a child node ID to this node."""
        if child_id not in self.children:
            self.children.append(child_id)
    
    def remove_child(self, child_id: str) -> None:
        """Remove a child node ID from this node."""
        if child_id in self.children:
            self.children.remove(child_id)


@dataclass
class TokenTree:
    """Complete token tree structure with navigation and manipulation methods."""
    
    # Tree data
    nodes: Dict[str, TreeNode] = field(default_factory=dict)
    root_id: Optional[str] = None
    
    # Current state
    selected_path: List[str] = field(default_factory=list)  # Node IDs from root to current
    current_node_id: Optional[str] = None
    
    # Configuration
    max_depth: int = 20
    max_branches_per_node: int = 10
    
    # Metadata
    created_at: datetime = field(default_factory=datetime.now)
    initial_prompt: str = ""
    
    def create_root(self, prompt: str) -> str:
        """Create the root node with the initial prompt."""
        root_node = TreeNode(
            token=prompt,
            probability=1.0,
            depth=0,
            is_selected=True
        )
        
        self.nodes[root_node.node_id] = root_node
        self.root_id = root_node.node_id
        self.current_node_id = root_node.node_id
        self.selected_path = [root_node.node_id]
        self.initial_prompt = prompt
        
        return root_node.node_id
    
    def add_token_alternatives(self, parent_id: str, alternatives: List[TokenProbability]) -> List[str]:
        """Add token alternatives as children of the specified parent node."""
        if parent_id not in self.nodes:
            raise ValueError(f"Parent node {parent_id} not found")
        
        parent_node = self.nodes[parent_id]
        if parent_node.depth >= self.max_depth:
            raise ValueError(f"Maximum depth {self.max_depth} reached")
        
        child_ids = []
        for i, token_prob in enumerate(alternatives[:self.max_branches_per_node]):
            child_node = TreeNode(
                token=token_prob.token,
                probability=token_prob.probability,
                parent_id=parent_id,
                depth=parent_node.depth + 1,
                position_in_parent=i,
                is_selected=(i == 0),  # First alternative is selected by default
                generation_metadata={
                    "logprob": getattr(token_prob, 'logprob', None),
                    "rank": i
                }
            )
            
            self.nodes[child_node.node_id] = child_node
            parent_node.add_child(child_node.node_id)
            child_ids.append(child_node.node_id)
        
        # Update selected path if we're extending the current path
        if parent_id == self.current_node_id and child_ids:
            self.current_node_id = child_ids[0]  # Select first alternative
            self.selected_path.append(child_ids[0])
        
        return child_ids
    
    def select_path_to_node(self, node_id: str) -> bool:
        """Select a path from root to the specified node."""
        if node_id not in self.nodes:
            return False
        
        # Build path from node to root
        path = []
        current_id = node_id
        
        while current_id is not None:
            path.append(current_id)
            node = self.nodes[current_id]
            current_id = node.parent_id
        
        # Reverse to get root-to-node path
        path.reverse()
        
        # Update selected states
        self._clear_selected_states()
        for node_id in path:
            self.nodes[node_id].is_selected = True
        
        self.selected_path = path
        self.current_node_id = node_id
        
        return True
    
    def create_branch_from_node(self, node_id: str, alternatives: List[TokenProbability]) -> List[str]:
        """Create a new branch starting from the specified node."""
        if node_id not in self.nodes:
            raise ValueError(f"Node {node_id} not found")
        
        # Mark the node as a branch root if it's not already
        self.nodes[node_id].is_branch_root = True
        
        # Add alternatives as children
        return self.add_token_alternatives(node_id, alternatives)
    
    def get_node_path_text(self, node_id: str) -> str:
        """Get the complete text from root to the specified node."""
        if node_id not in self.nodes:
            return ""
        
        # Build path from node to root
        path = []
        current_id = node_id
        
        while current_id is not None:
            node = self.nodes[current_id]
            if not node.is_root:  # Skip root prompt
                path.append(node.token)
            current_id = node.parent_id
        
        # Reverse to get root-to-node order
        path.reverse()
        
        # Combine tokens (add space between tokens)
        return "".join(path)
    
    def get_selected_path_text(self) -> str:
        """Get the complete text of the currently selected path."""
        if not self.selected_path:
            return self.initial_prompt
        
        tokens = []
        for node_id in self.selected_path[1:]:  # Skip root
            node = self.nodes[node_id]
            tokens.append(node.token)
        
        return self.initial_prompt + "".join(tokens)
    
    def get_children(self, node_id: str) -> List[TreeNode]:
        """Get all child nodes of the specified node."""
        if node_id not in self.nodes:
            return []
        
        node = self.nodes[node_id]
        return [self.nodes[child_id] for child_id in node.children if child_id in self.nodes]
    
    def get_siblings(self, node_id: str) -> List[TreeNode]:
        """Get all sibling nodes of the specified node."""
        if node_id not in self.nodes:
            return []
        
        node = self.nodes[node_id]
        if node.parent_id is None:
            return []
        
        return self.get_children(node.parent_id)
    
    def get_branch_roots(self) -> List[TreeNode]:
        """Get all nodes that are branch roots."""
        return [node for node in self.nodes.values() if node.is_branch_root]
    
    def get_leaf_nodes(self) -> List[TreeNode]:
        """Get all leaf nodes in the tree."""
        return [node for node in self.nodes.values() if node.is_leaf]
    
    def get_nodes_at_depth(self, depth: int) -> List[TreeNode]:
        """Get all nodes at the specified depth."""
        return [node for node in self.nodes.values() if node.depth == depth]
    
    def delete_subtree(self, node_id: str) -> Set[str]:
        """Delete a subtree starting from the specified node. Returns set of deleted node IDs."""
        if node_id not in self.nodes or node_id == self.root_id:
            return set()
        
        # Collect all nodes in the subtree
        to_delete = set()
        stack = [node_id]
        
        while stack:
            current_id = stack.pop()
            if current_id in self.nodes:
                to_delete.add(current_id)
                node = self.nodes[current_id]
                stack.extend(node.children)
        
        # Remove from parent's children list
        node = self.nodes[node_id]
        if node.parent_id and node.parent_id in self.nodes:
            parent = self.nodes[node.parent_id]
            parent.remove_child(node_id)
        
        # Delete all nodes in subtree
        for delete_id in to_delete:
            del self.nodes[delete_id]
        
        # Update selected path if it was affected
        if any(node_id in to_delete for node_id in self.selected_path):
            self._rebuild_selected_path()
        
        return to_delete
    
    def reset_tree(self) -> None:
        """Reset the tree to just the root node."""
        if self.root_id:
            root_node = self.nodes[self.root_id]
            self.nodes = {self.root_id: root_node}
            root_node.children = []
            self.selected_path = [self.root_id]
            self.current_node_id = self.root_id
    
    def get_tree_stats(self) -> Dict[str, Any]:
        """Get statistics about the tree structure."""
        if not self.nodes:
            return {"total_nodes": 0, "max_depth": 0, "branch_count": 0, "leaf_count": 0}
        
        depths = [node.depth for node in self.nodes.values()]
        branch_roots = self.get_branch_roots()
        leaf_nodes = self.get_leaf_nodes()
        
        return {
            "total_nodes": len(self.nodes),
            "max_depth": max(depths) if depths else 0,
            "branch_count": len(branch_roots),
            "leaf_count": len(leaf_nodes),
            "selected_path_length": len(self.selected_path),
            "current_depth": self.nodes[self.current_node_id].depth if self.current_node_id else 0
        }
    
    def _clear_selected_states(self) -> None:
        """Clear selected state from all nodes."""
        for node in self.nodes.values():
            node.is_selected = False
    
    def _rebuild_selected_path(self) -> None:
        """Rebuild selected path after tree modifications."""
        if not self.root_id:
            self.selected_path = []
            self.current_node_id = None
            return
        
        # Find the deepest remaining node in the old selected path
        valid_path = []
        for node_id in self.selected_path:
            if node_id in self.nodes:
                valid_path.append(node_id)
            else:
                break
        
        if valid_path:
            self.selected_path = valid_path
            self.current_node_id = valid_path[-1]
            
            # Update selected states
            self._clear_selected_states()
            for node_id in valid_path:
                self.nodes[node_id].is_selected = True
        else:
            # Fallback to root
            self.selected_path = [self.root_id]
            self.current_node_id = self.root_id
            self.nodes[self.root_id].is_selected = True


def create_sample_tree() -> TokenTree:
    """Create a sample tree for testing purposes."""
    from ..services.llm_client import TokenProbability
    
    tree = TokenTree(max_depth=5)
    
    # Create root
    root_id = tree.create_root("The capital of France is")
    
    # Add first level alternatives
    alternatives_1 = [
        TokenProbability(token=" Paris", probability=0.85, logprob=-0.1625, percentage=85.0),
        TokenProbability(token=" Lyon", probability=0.08, logprob=-2.5257, percentage=8.0),
        TokenProbability(token=" Marseille", probability=0.04, logprob=-3.2189, percentage=4.0),
        TokenProbability(token=" Nice", probability=0.02, logprob=-3.9120, percentage=2.0),
        TokenProbability(token=" Bordeaux", probability=0.01, logprob=-4.6052, percentage=1.0)
    ]
    children_1 = tree.add_token_alternatives(root_id, alternatives_1)
    
    # Add second level for Paris branch
    if children_1:
        alternatives_2 = [
            TokenProbability(token=",", probability=0.6, logprob=-0.5108, percentage=60.0),
            TokenProbability(token=".", probability=0.3, logprob=-1.2040, percentage=30.0),
            TokenProbability(token=" and", probability=0.05, logprob=-2.9957, percentage=5.0),
            TokenProbability(token=" which", probability=0.03, logprob=-3.5066, percentage=3.0),
            TokenProbability(token=" the", probability=0.02, logprob=-3.9120, percentage=2.0)
        ]
        tree.add_token_alternatives(children_1[0], alternatives_2)
    
    return tree
