class TreeNode(object):
    """
    Binary Tree Node representation
    """

    def __init__(self, value):
        self.val = value
        self.right = None  # right node
        self.left = None   # left node


class BinarySearchTree:
    """
    Binary Search Tree implementation

    It is a rooted binary tree data structure whose internal nodes each store a key greater than
    all the keys in the node’s left subtree and less than those in its right subtree

    https://en.wikipedia.org/wiki/Binary_search_tree
    """

    @staticmethod
    def insert(root, key):
        if root is None:
            return TreeNode(key)
        else:
            if root.val == key:
                return root
            elif root.val < key:
                root.right = BinarySearchTree.insert(root.right, key)
            else:
                root.left = BinarySearchTree.insert(root.left, key)
        return root

    @staticmethod
    def lookup(root, key):
        # Base Cases: root is null or key is present at root
        if root is None or root.val == key:
            return root

        # Key is greater than root's key
        if root.val < key:
            return BinarySearchTree.lookup(root.right, key)

        # Key is smaller than root's key
        return BinarySearchTree.lookup(root.left, key)

    @staticmethod
    def __min_value_node(node):
        current = node

        # loop down to find the left most leaf
        while current.left is not None:
            current = current.left

        return current

    @staticmethod
    def delete(root, key):
        if root is None:
            return root
        # If the key to be deleted
        # is smaller than the root's
        # key then it lies in  left subtree
        if key < root.val:
            root.left = BinarySearchTree.delete(root.left, key)

        # If the kye to be delete
        # is greater than the root's key
        # then it lies in right subtree
        elif key > root.val:
            root.right = BinarySearchTree.delete(root.right, key)

        # If key is same as root's key, then this is the node
        # to be deleted
        else:
            # Node with only one child or no child
            if root.left is None:
                temp = root.right
                return temp
            elif root.right is None:
                temp = root.left
                return temp

            # Node with two children:
            # Get the inorder successor
            # (smallest in the right subtree)
            temp = BinarySearchTree.__min_value_node(root.right)

            # Copy the inorder successor's
            # content to this node
            root.key = temp.key

            # Delete the inorder successor
            root.right = BinarySearchTree.delete(root.right, temp.key)

        return root
