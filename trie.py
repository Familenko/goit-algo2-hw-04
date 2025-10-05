from collections import deque
from dataclasses import dataclass
from typing import Hashable, Any, Optional, Dict, List


@dataclass
class Node:
    children: Dict[str, "Node"]
    value: Optional[Any] = None


class Trie:
    def __init__(self):
        self.root = Node(children={})
        self.size = 0

    def __setitem__(self, key: str, value: Any) -> None:
        if not key:
            raise TypeError("Key must be a non-empty string")

        current = self.root
        for char in key:
            if char not in current.children:
                current.children[char] = Node(children={})
            current = current.children[char]

        if current.value is None:
            self.size += 1
        current.value = value

    def __getitem__(self, key: str) -> Any:
        if not key:
            raise TypeError("Key must be a non-empty string")

        current = self.root
        for char in key:
            if char not in current.children:
                raise KeyError(f"Key not found: {key}")
            current = current.children[char]

        if current.value is None:
            raise KeyError(f"Key not found: {key}")
        return current.value

    def __delitem__(self, key: str) -> None:
        if not key:
            raise TypeError("Key must be a non-empty string")

        def _delete(node: Node, key: str, depth: int) -> bool:
            if depth == len(key):
                if node.value is not None:
                    node.value = None
                    self.size -= 1
                    return len(node.children) == 0
                return False
            char = key[depth]
            if char in node.children:
                should_delete = _delete(node.children[char], key, depth + 1)
                if should_delete:
                    del node.children[char]
                    return len(node.children) == 0 and node.value is None
            return False

        _delete(self.root, key, 0)

    def get(self, key: str, default: Any = None) -> Any:
        try:
            return self[key]
        except KeyError:
            return default

    def __len__(self) -> int:
        return self.size

    def keys(self) -> List[str]:
        result: List[str] = []
        self._collect(self.root, [], result)
        return result

    def keys_with_prefix(self, prefix: str) -> List[str]:
        current = self.root
        for char in prefix:
            if char not in current.children:
                return []
            current = current.children[char]

        result: List[str] = []
        self._collect(current, list(prefix), result)
        return result

    def longest_prefix_of(self, s: str) -> str:
        current = self.root
        longest_prefix = ""
        current_prefix = ""
        for char in s:
            if char in current.children:
                current = current.children[char]
                current_prefix += char
                if current.value is not None:
                    longest_prefix = current_prefix
            else:
                break
        return longest_prefix

    def _collect(self, node: Node, path: List[str], result: List[str]) -> None:
        if node.value is not None:
            result.append("".join(path))
        for c, n in node.children.items():
            path.append(c)
            self._collect(n, path, result)
            path.pop()
            