from typing_extensions import Self
from typing import Any, Callable

"""
Реализуем бинарное дерево для сортировки любых списков
"""


class TreeNode:
    """
    Узел бинарного дерева
    """

    def __init__(self, value: Any):
        self.left: TreeNode | None = None
        self.right: TreeNode | None = None
        self.value: Any | None = value

    def add_child(self, new_node: Self, comparison_function: Callable) -> None:
        """
        Добавление нового элемента в левое поддерево
        
        :param new_node: новый узел, добавляемый в дерево со значением, меньшим, чем у текущего узла 
        :param comparison_function: пользовательская функция, сравнивающая два значения, 
        возвращает True, если левое значение меньше 
        """
        if comparison_function(new_node, self):
            if self.left:
                self.left.add_child(new_node, comparison_function)
            else:
                self.left = new_node
        else:
            if self.right:
                self.right.add_child(new_node, comparison_function)
            else:
                self.right = new_node


class BinaryTree:
    """
    Бинарное дерево
    """

    def __init__(self):
        self.root: TreeNode | None = None

        # #
        # self.comparison_function: Callable | None = None

        # # пользовательская функция, извлекающая целевое значение элемента для сравнения
        # self.value_to_compare: Callable | None = None

    def populate(self, nodes_to_sort: list[TreeNode], comparison_function: Callable) -> None:
        """
        Наполнение дерева новыми элементами
        :param nodes_to_sort: набор узлов дерева, значения которых надо отсортировать
        :param comparison_function: пользовательская функция, сравнивающая два значения,
        возвращает True, если левое значение меньше
        """
        for new_node in nodes_to_sort:
            if self.root:
                self.root.add_child(new_node, comparison_function)
            else:
                self.root = new_node

    def get_sorted(self, ascending_order: bool = True) -> list:

        def add_this_subtree(start_node: TreeNode):
            if ascending_order:
                if start_node.left:
                    add_this_subtree(start_node.left)
                result.append(start_node)
                if start_node.right:
                    add_this_subtree(start_node.right)
            else:
                if start_node.right:
                    add_this_subtree(start_node.right)
                    result.append(start_node)
                if start_node.left:
                    add_this_subtree(start_node.left)

        result = []
        add_this_subtree(self.root)
        return result
