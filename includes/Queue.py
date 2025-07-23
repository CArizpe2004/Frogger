from typing import Any
from includes.Node import Node

class Queue:
    def __init__(self, data = None) -> None:
        if data:
            self.head = Node(data)
        else: self.head = None
        self.length = 0

    def add(self, data):
        if self.head == None:
            self.head = Node(data)
        else:
            pointer : Node = self.head

            while pointer.getNext() != None:
                pointer = pointer.getNext()
            
            pointer.setNext(data)
        self.length += 1


    def printQueue(self):
        pointer : Node = self.head

        print('[ ', end='')
        while pointer:
            print(str(pointer.getData()) + ' ', end='')
            pointer = pointer.getNext()
        print(']')

    def peek(self):
        if self.head == None:
            return None
        return self.head.getData()
    
    def pop(self):
        poppedNode : Node = self.head
        self.head = self.head.getNext()
        self.length -= 1
        return poppedNode
    
    def isEmpty(self) -> bool:
        return self.head == None
    
    def clearQueue(self):
        self.head = None

    def toList(self) -> list:
        list = []
        pointer = self.head

        while pointer:
            list.append(pointer.getData())
            pointer = pointer.getNext()

        return list
    
    def isEmpty(self) -> bool:
        return self.peek() == None
    
    
    
