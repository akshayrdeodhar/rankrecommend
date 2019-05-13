from linkpredict import rooted_pagerank
from bs4 import BeautifulSoup
import requests as rq
import networkx as nx
import os
import csv


def build_graph(root, graphsize = 1000):
    visited = set()
    unvisited = [root]
    gitgraph = nx.DiGraph()
    gitgraph.add_node(root)
    filename = "data/" + str(root) + "_graph.txt"

    if os.path.isfile(filename):
        fp = open(filename, "r")
        reader = csv.reader(fp, delimiter = "\t")
        for line in reader:
            gitgraph.add_edge(line[0], line[1])

        fp.close()

        return gitgraph

    url1 = "https://github.com/" + root
    userpage = rq.get(url1)
    if userpage.status_code != 200:
        return False


    while len(gitgraph) < graphsize and len(unvisited) != 0:
        newnode = unvisited[0]
        
        url2 = "https://github.com/" + newnode + "/following"
        # print("Visiting " + url2)
        resource = rq.get(url2)
        follower_raw = resource.text
        follower_soup = BeautifulSoup(follower_raw)
        preprocess_list = follower_soup.find_all("a", class_ = "d-inline-block")
        try:
            names = [user['href'][1:] for user in preprocess_list]
            # print(names)
            for amala in names[2:]:
                gitgraph.add_edge(newnode, amala)
                if amala not in visited:
                    unvisited.append(amala)
        except:
            print("Unable to find folowees for " + newnode)
    
        visited.add(unvisited.pop(0))
    
        url = "https://github.com/" + newnode + "/followers"
        # print("Visiting " + url)
        resource = rq.get(url)
        follower_raw = resource.text
        follower_soup = BeautifulSoup(follower_raw)
        preprocess_list = follower_soup.find_all("a", class_ = "d-inline-block")
        try:
            names = [user['href'][1:] for user in preprocess_list]
            # print(names)
            for hrudaya in names[2:]:
                gitgraph.add_edge(hrudaya, newnode)
                if hrudaya not in visited:
                    unvisited.append(hrudaya)
        except:
            print("Unable to find folowers for " + newnode)
    
    
        
    github_graph = list(gitgraph.edges())
    links = open(filename, "w")

    for link in github_graph:
        links.write(link[0] + "\t" + link[1] + "\n")
    
    links.close()

    return gitgraph
    
def get_recommendations(graph, node, n = 10):
    recommendation_list = rooted_pagerank(graph, node, 0.3, 1e-6)
    get_val = lambda key: recommendation_list[key]
    top_recommendations = sorted(recommendation_list.keys(), key = get_val, reverse = True)
    print("Cleared Checkpoint")
    recommends = []
    found = 0
    i = 0

    while len(recommends) < n:
        if i < len(top_recommendations):
            if not graph.has_edge(node, top_recommendations[i]) and node != top_recommendations[i]:
                recommends.append((top_recommendations[i], recommendation_list[top_recommendations[i]]))
            i += 1

    return recommends

def build_graph_from_file(file_object):
    file_object.save(os.path.join('/home/akshay/Desktop/COEP/SY/PPL/project/app/', "temp.sv"))
    file_object = open("temp.sv", "r")
    graph = nx.DiGraph()
    reader = csv.reader(file_object, delimiter = "\t")
    for line in reader:
        graph.add_edge(line[0], line[1])

    file_object.close()

    return graph


