#!/usr/bin/env python
# coding: utf-8


import biom
import pandas as pd
import numpy as np
import skbio
import s2sphere as s2
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
from shapely.geometry import Point, Polygon
#for ~fancy~ just do it as a qiime2 plugin
#Or python click
#set registration to be a choice
#look at q2_diversity - beta-diversity 
#upfront sanity checking
#input - q2 metadata object
#Parameterize category names - default to latitude and longitude

def clean(md_df):
    if 'latitude' not in md_df: #and selected method of binning
        raise ValueError("Must have latitude in metadata to use quadtrees")
    if 'latitude' not in md_df: #and selected method of binning
        raise ValueError("Must have longitude in metadata to use quadtrees")
    

    ## if selected method of binning is mock
    #md_edited['country'] = md_df['country']

    df = md_df[['latitude','longitude']]

    #as global or local in function, define all null or this:
    df['latitude'] = pd.to_numeric(df.latitude, errors='coerce')
    df['longitude'] = pd.to_numeric(df.longitude, errors='coerce')
    
    #drop nan values (formerly strings) from dataframe
    df = df.dropna(subset = ['latitude', 'longitude'])
  
    if df.empty is True:
        raise ValueError("Latitude and/or Longitude have no numeric values, please check your data.")

    #check if latitude and longitude is castable as float
    df['latitude'] = df['latitude'].astype(float)
    df['longitude'] = df['longitude'].astype(float)

    #make (0,0) be the bottom right corner for ease of calculation, probably a better way to do this?
    df['latitude'] = df['latitude'] + 90
    df['longitude'] = df['longitude'] + 180
    
    return df

#from matplotlib import patches
class Point():
    def __init__(self, x, y, sample_id):
        self.x = float(x)
        self.y = float(y)
        self.sample_id = sample_id        
    
class Node():
    def __init__(self, x0, y0, w, h, points, _id):
        self.x0 = x0
        self.y0 = y0
        self.width = float(w)
        self.height = float(h)
        self.points = points
        self.children = []
        self.id = _id

    def get_width(self):
        return self.width
    
    def get_height(self):
        return self.height
    
    def get_points(self):
        return self.points
    
    def get_id(self):
        return self.id
    
    def set_id(self, _id):
        self.id = self.id+_id

    
class QTree():
    def __init__(self, k, data):
        self.threshold = k
        self.points = [Point(x, y, sample_id) for sample_id, x, y in data]
        self.root = Node(0, 0, 360, 180, self.points, "0")

    def add_point(x, y, sample_id):
        self.points.append(Point(x, y, sample_id))
    
    def get_points(self):
        return self.points
    
    def subdivide(self, count):
        samples = pd.DataFrame()
        samples['index'] = df['index']
        samples = samples.set_index('index')

        count = 0
        id_1 = ""
        base = skbio.TreeNode(name="root")

        recursive_subdivide(self.root, self.threshold, count, id_1, base)

            
        return base
    ''' 
    def graph(self):
        vertices = []
        for i in range(0, 4):
            vertex = (node.x0, node.y0)
            vertices.append([latlng.lng().degrees,
                             latlng.lat().degrees])
        fig = plt.figure(figsize=(12, 6))
        plt.title("Quadtree")
        ax = fig.add_subplot(111)
        c = find_children(self.root)
        print("Number of segments: %d" %len(c))
        areas = set()
        for el in c:
            areas.add(el.width*el.height)
        print("Minimum segment area: %.3f units" %min(areas))
        for n in c:
            ax.add_patch(patches.Rectangle((n.x0, n.y0), n.width, n.height, fill=False))
        x = [point.x for point in self.points]
        y = [point.y for point in self.points]
        plt.plot(x, y, 'ro')
        plt.show()
        return
    '''

def recursive_subdivide(node, k, count, id_1, tree_node):
    count += 1
    id_1 += str(count)
    
    bin_id.append("H" + str(count))
    samples["H" + str(count)] = ""
    
     
    if len(node.points)<=k:
        return

    print(type(node.width))
    w_ = node.width/2
    h_ = node.height/2
    
    #fun challenge do it in a for loop
    #probably make it smaller
    p = contains(node.x0, node.y0, w_, h_, node.points)
    x1 = Node(node.x0, node.y0, w_, h_, p, id_1 + "sw;")
    node_1 = skbio.TreeNode(name=str(count) + "sw")
    for pt in p:
        bin_1.append((pt.sample_id, count, x1.get_id()))
        node_1.extend([skbio.TreeNode(name=pt.sample_id)])
    recursive_subdivide(x1, k, count, id_1+"sw;", node_1)
    
    p = contains(node.x0, node.y0+h_, w_, h_, node.points)
    x2 = Node(node.x0, node.y0+h_, w_, h_, p, id_1+"nw;")
    node_2 = skbio.TreeNode(name=str(count)+"nw")
    for pt in p:
        bin_1.append((pt.sample_id, count, x2.get_id()))
        node_2.extend([skbio.TreeNode(name=pt.sample_id)])
    recursive_subdivide(x2, k, count, id_1+"nw;", node_2)

    p = contains(node.x0+w_, node.y0, w_, h_, node.points)
    x3 = Node(node.x0 + w_, node.y0, w_, h_, p, id_1+"se;")
    node_3 = skbio.TreeNode(name=str(count)+"se")
    for pt in p:
        bin_1.append((pt.sample_id, count, x3.get_id()))
        node_3.extend([skbio.TreeNode(name=pt.sample_id)])
    recursive_subdivide(x3, k, count, id_1+"se;", node_3)

    p = contains(node.x0+w_, node.y0+h_, w_, h_, node.points)
    x4 = Node(node.x0+w_, node.y0+h_, w_, h_, p, id_1+"ne;")
    node_4 = skbio.TreeNode(name=str(count)+"ne")
    for pt in p:
        bin_1.append((pt.sample_id, count, x4.get_id()))
        node_4.extend([skbio.TreeNode(name=pt.sample_id)])
    recursive_subdivide(x4, k, count, id_1+"ne;", node_4)

    
    
    tree_node.extend([node_1, node_2, node_3, node_4])
    node.children = [x1, x2, x3, x4]

    
def contains(x, y, w, h, points):
    pts = []
    for point in points:
        if point.x >= x and point.x <= x+w and point.y>=y and point.y<=y+h:
            pts.append(point)
    return pts

'''
def find_children(node):
    if not node.children:
        return [node]
    else:
        children = []
        for child in node.children:
            children += (find_children(child))
    return children
'''


def get_results(cleaned_df, depth):
    cleaned_df = cleaned_df.reset_index()
    xy = cleaned_df.to_numpy()
    samples = pd.DataFrame()
    samples['index'] = cleaned_df['index']
    bin_0 = []
    bin_id = [] 
    q = QTree(depth, xy)
    tree = q.subdivide(count = 0)

    for samp, bin_i, items in bin_0:
        bin_name = "H" + str(bin_i)
        samples[bin_name] = np.where(samples['index'] == samp, items, samples[bin_name])
    
    return tree, samples
    

