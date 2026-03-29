from utils import RMITLinkedList, RMITDoubleLinkedList, RMTCircularLinkedList

if __name__ == "__main__":
    llist = RMITLinkedList([1, 2, 3, 4, 5])
    print(llist)
    llist.traverse()
    llist.insert(6, 0)
    llist.traverse()
    llist.delete(0)
    llist.traverse()