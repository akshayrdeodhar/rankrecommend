from bs4 import BeautifulSoup
import requests as rq
import networkx as nx

def build_graph(root, graphsize = 1000):

	filename = "huge_graph.txt"

	unvisited = [root]
	visited = set()

	gitgraph = nx.DiGraph()

	while len(gitgraph) < graphsize:
	    newnode = unvisited[0]

	    
	    url = "https://github.com/" + newnode + "/followers"
	    print("Visiting " + url)
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
	    
	    
	    url2 = "https://github.com/" + newnode + "/following"
	    print("Visiting " + url2)
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

	    
	github_graph = list(gitgraph.edges())

	links = open(filename, "w")

	for link in github_graph:
	    links.write(link[0] + "\t" + link[1] + "\n")

	links.close()

    
