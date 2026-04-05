class StudentNode:
    def __init__(self, name: str, score: int):
        self.name = name
        self.score = score
        self.left = None
        self.right = None


class StudentBST:
    def __init__(self):
        self.root = None
    
    def add_student(self, student: StudentNode):
        self.root = self._add_student(self.root, name=student.name, score=student.score)

    def _add_student(self, node, name, score):
        if node is None:
            return StudentNode(name, score)
        if score < node.score:
            node.left = self._add_student(node.left, name, score)
        elif score > node.score:
            node.right = self._add_student(node.right, name, score)
        else:
            print(f"{name} already in tree; skipped.")
        return node

    def inorder(self):
        """Left → root → right (prints sorted order for a valid BST)."""
        self._inorder(self.root)
        print()

    def _inorder(self, node):
        if node is None:
            return
        self._inorder(node.left)
        print(f'({node.name}, {node.score})', end=" ")
        self._inorder(node.right)


student_bst = StudentBST()
student_bst.add_student(StudentNode(name="John", score=85))
student_bst.add_student(StudentNode(name="Jane", score=90))
student_bst.add_student(StudentNode(name="Jim", score=80))
student_bst.add_student(StudentNode(name="Jill", score=88))
student_bst.add_student(StudentNode(name="Jack", score=82))
student_bst.add_student(StudentNode(name="Jill", score=88))
student_bst.add_student(StudentNode(name="Jill", score=88))

print("Inorder:")
student_bst.inorder()