class Node:
    def __init__(self, data = None) -> None:
        if data:
            self.data = data
        else:
            self.data = None
        self.next = None

    def getData(self):
        return self.data
    
    def setData(self, data):
        self.data = data

    def setNext(self, data):
        self.next = Node(data)

    def getNext(self):
        return self.next
    



# node = Node(5)

# node.setNext(1)

# secondNode = node.getNext()

# secondNode.setNext(3)

# pointer = node

# print(pointer.getData())

# while pointer.getNext():
#     pointer = pointer.getNext()
#     print(pointer.getData())