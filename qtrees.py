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

    df = md_df[['longitude','latitude']]

    #as global or local in function, define all null or this:
    df['latitude'] = pd.to_numeric(df.latitude, errors='coerce')
    df['longitude'] = pd.to_numeric(df.longitude, errors='coerce')
    
    #drop nan values (formerly strings) from dataframe
    df = df.dropna(subset = ['longitude', 'latitude'])
  
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
    
    def subdivide(self, count, samples):
        count = 0
        id_1 = ""
        base = skbio.TreeNode(name="root")
        print(samples.head())
        recursive_subdivide(self.root, self.threshold, count, id_1, base)

            
        return base, bin_id

def recursive_subdivide(node, k, count, id_1, tree_node):
    

    if len(node.points) < k:
        return
    
    samples["H" + str(count)] = ""

    id_1 += str(count)
    samples["H" + str(count)] = ""

    bin_id.append("H" + str(count))
    
    w_ = node.width/2
    h_ = node.height/2    
    nodes = []
    sk_nodes = []

    for i in range(4):
        
        if(i ==0):
            quad = "sw"
            node.x0 = node.x0
            node.y0 = node.y0

        elif(i==1):
            quad = "nw"
            node.x0 = node.x0
            node.y0 = node.y0+h_
        elif(i == 2):
            quad = "ne"
            node.x0 = node.x0+w_
            node.y0 = node.y0
        elif(i == 3):
            quad = "se"
            node.x0 = node.x0
            node.y0 = node.y0-h_

        
        p = contains(node.x0, node.y0, w_, h_, node.points)
        quad_node= Node(node.x0, node.y0, w_, h_, p, id_1 + quad+";")
        tree_node = skbio.TreeNode(name=str(count) + quad)
        
        for pt in p:
            bin_1.append((pt.sample_id, count, quad_node.get_id()))
            #tree_node.extend([skbio.TreeNode(name=pt.sample_id)])
        nodes.append(quad_node)
        sk_nodes.append(tree_node)
        recursive_subdivide(quad_node, k, count, id_1+quad+";", tree_node)
        
    tree_node.extend(sk_nodes)
    node.children = nodes

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


def get_results(cleaned_df, threshold):
    cleaned_df = cleaned_df.reset_index()
    xy = cleaned_df.to_numpy()

    samples = pd.DataFrame()
    samples['index'] = cleaned_df['index']
    
    bin_1 = []
    bin_id = [] 
    print(samples.head())
    q = QTree(threshold, xy)
    tree = q.subdivide(0, samples)
    
    print("working here")
    for samp, bin_i, items in bin_0:
        bin_name = "H" + str(bin_i)
        samples[bin_name] = np.where(samples['index'] == samp, items, samples[bin_name])
    
    return tree, samples
    

