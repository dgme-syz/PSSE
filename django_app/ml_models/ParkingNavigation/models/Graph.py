import numpy as np
from pathlib import Path
import json, heapq, cv2, sys, os

base_dir = Path(__file__).parent.parent.absolute().__str__()
sys.path.append(base_dir)

from models.Nodes import *
import matplotlib.pyplot as plt
class Graph:
    def __init__(self):
        self.Nodes = read(os.path.join(base_dir ,"config/data.json"))

        self.dic = {}
        for node in self.Nodes:
            self.dic[node.id] = node

        self.Edges = []
        with open(os.path.join(base_dir, "config/edge.txt"), "r") as f:
            for line in f:
                self.Edges.append(map(int, line.strip().split()))

        # 建立邻接表
        self.adj = [[] for _ in range(len(self.Nodes))]
        for a, b in self.Edges:
            self.adj[a].append(b)
            self.adj[b].append(a)
        

        self.f = []
        with open(os.path.join(base_dir, "config/START.json"), "r") as f:
            self.f = json.load(f)

    def Dijkstra(self, x):
        """u是起点，从0开始"""
        dis = []
        vis = []
        heap = []
        pre = []

        for i in range(len(self.Nodes)):
            dis.append(np.inf)
            vis.append(False)
            pre.append(-1)

        dis[self.f[x]] = 0
        heapq.heappush(heap, (0, self.f[x]))
        while len(heap) > 0:
            d, u = heapq.heappop(heap)
            if vis[u]:
                continue
            vis[u] = True
            for z in self.adj[u]:
                d = dis[u] + self.dic[u].distance(self.dic[z])
                if dis[z] > d:
                    dis[z] = d
                    pre[z] = u
                    heapq.heappush(heap, (d, z))

        node_empty = [item for item in self.Nodes if item.is_empty]
        dist = [dis[item.id] for item in node_empty]   

        target = node_empty[np.argmin(dist)]

        List = []
        z = target.id
        while z != -1:
            List.append(self.dic[z])
            z = pre[z]
        return dis[target.id], target, List

def Visulize(Nodes, img_path):
    def imshow(image, cmap=None, title=None):
        fig, ax = plt.subplots(1, 1)
        img = image.copy()

        if cmap == 'gray':
            ax.imshow(img, cmap=cmap)
        else:
            img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
            ax.imshow(img)
        ax.axis('off')

        if title:
            ax.set_title(title)
        plt.show()

    img = cv2.imread(img_path)

    for node in Nodes:
        cv2.circle(img, (int(node.x), int(node.y)), 5, (0, 0, 255), thickness=3)

    for i in range(1, len(Nodes)):
        cv2.line(img, 
                (int(Nodes[i - 1].x), int(Nodes[i - 1].y)), 
                (int(Nodes[i].x), int(Nodes[i].y)), 
                (255, 0, 0), thickness=2)
    return img

if __name__ == '__main__':
    w = Graph()
    x, z, NodesList = w.Dijkstra(0)
    print(z.id)
    Visulize(NodesList, os.path.join(base_dir, "saveImg/scene1410.jpg"))


