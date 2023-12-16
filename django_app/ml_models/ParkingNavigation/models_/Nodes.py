import numpy as np
import json
import heapq

class Node:
    def __init__(self, x, y, is_entrance=False, is_empty=False,id = None, is_parking=False, 
                 direction=0):
        # direction为0表示该坐标位于左上角，否则位于右上角
        self.x = x  # 横坐标
        self.y = y  # 纵坐标
        self.id = id
        self.is_entrance = is_entrance  # 是否为入口，默认为False
        self.is_empty = is_empty  # 是否为空车位，默认为False
        self.is_parking = is_parking
        self.direction = direction

    def __str__(self):
        return f"Node at ({self.x}, {self.y}), Entrance: {self.is_entrance}, Empty: {self.is_empty}"
    
    def distance(self, w):
        if isinstance(w, Node):
            dx = self.x - w.x
            dy = self.y - w.y
        else:
            dx = self.x - w[0]
            dy = self.y - w[1]
        return np.sqrt(dx * dx + dy * dy)


def read(file):
    with open(file, 'r') as f:
        data = json.load(f)
    return [Node(item['x'], item['y'], item['is_entrance'], 
                    item['is_empty'], item['id'], item['is_parking'], 
                    item['direction']) for item in data]
            
def Get_Nearest_Node(NodeList, node):
    if isinstance(node, Node):
        dis = [item.distance(node) for item in NodeList]
    else:
        dis = [item.distance([node[0], node[1]]) for item in NodeList]
    return NodeList[np.argmin(dis)].id  
        


if __name__ == '__main__':
    node1 = Node(3, 4, True, False)
    node2 = Node(5, 6, False, True)
    print(node1.distance(node2))
