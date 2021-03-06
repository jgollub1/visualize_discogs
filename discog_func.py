from collections import defaultdict
import discogs_client
import math
import numpy as np
from plotly.graph_objs import *
import plotly.plotly as py
import networkx as nx
import time

def pol2cart(rho, phi):
    x = rho * np.cos(phi)
    y = rho * np.sin(phi)
    return(x, y)

# retrieve all collaborators from artist's "master" releases
def discog(artist,token):
    # get the artist's id; search for releases
    d = discogs_client.Client('ExampleApplication/0.2',user_token=token)
    artist_id = d.search(artist, type='artist')[0].id
    releases = d.search(str(artist_id), type='release')
    r_dict = {}
    collab_dict = defaultdict(list)

    for i,release in enumerate(releases):
        r_title = release.title.split(' - ')[-1]
        time.sleep(1)
        #print r_title
        if release.master==None:
            continue
        elif release.master.id in r_dict:
            continue

        r_dict[release.master.id] = 1
        artist_ids = set([artist.id for artist in release.credits])
        #print artist_ids

        # add the album to list of collaborations
        for a_id in artist_ids:
            collab_dict[a_id] += [(r_title,release.year)]
        r_dict[r_title] = 1
    
    # sort each collaboration by year, then all collaborators by volume
    for collab in collab_dict.keys():
        collab_dict[collab] = sorted(collab_dict[collab],key=lambda a:a[1])

    collab_list = []
    for key in sorted(collab_dict,key=lambda x:len(collab_dict[x]),reverse=True):
        collab_list.append((key,collab_dict[key]))
    return [collab for collab in collab_list if collab[0] not in (0,artist_id)]

# construct a graph with the artist and top 'n' collaborators
def construct_g(artist,top_collab,token):
	d = discogs_client.Client('ExampleApplication/0.2',user_token=token)
	G = nx.MultiGraph()
	G.add_node(0,name=artist,num=0)
	ann_height = .025
	pos = {0: (0,0)}
	labels = {0: artist}
	annots = [{'showarrow':False,'text':artist,'x':0,'xref':'x','y':ann_height,'yref':'y'}]
	for i,collab in enumerate(top_collab):
	    a_name = d.artist(collab[0]).name
	    G.add_node(i+1,name=a_name,num=i+1)
	    labels[i+1] = a_name
	    rho, phi = (1/float(len(collab[1]))), i*(2*math.pi/len(top_collab))
	    location = pol2cart(rho,phi)
	    pos[i+1] = location
	    a_dict = {'showarrow':False,'text':a_name,'x':location[0],'xref':'x','y':location[1]+ann_height,'yref':'y'}
	    annots.append(a_dict)
	    
	    for album in collab[1]:
	        G.add_edge(0,i+1)

	label_pos = {}
	for n, p in pos.iteritems():
	    G.node[n]['pos'] = p
	    label_pos[n] = map(sum,zip(p,(0,.05)))


	pos=nx.get_node_attributes(G,'pos')

	edge_trace = Scatter(
	    x=[],
	    y=[],
	    line=Line(width=0.5,color='#888'),
	    hoverinfo='none',
	    mode='lines')

	for edge in G.edges():
	    x0, y0 = G.node[edge[0]]['pos']
	    x1, y1 = G.node[edge[1]]['pos']
	    edge_trace['x'] += [x0, x1, None]
	    edge_trace['y'] += [y0, y1, None]

	node_trace = Scatter(
	    x=[],
	    y=[],
	    text=[''],
	    textposition='top',
	    mode='markers',
	    hoverinfo='text',
	    marker=Marker(
	        showscale=True,
	        # colorscale options
	        # 'Greys' | 'Greens' | 'Bluered' | 'Hot' | 'Picnic' | 'Portland' |
	        # Jet' | 'RdBu' | 'Blackbody' | 'Earth' | 'Electric' | 'YIOrRd' | 'YIGnBu'
	        colorscale='YIGnBu',
	        reversescale=True,
	        color=[],
	        size=10,
	        colorbar=dict(
	            thickness=15,
	            title='Node Connections',
	            xanchor='left',
	            titleside='right'
	        ),
	        line=dict(width=2)))

	for node in G.nodes():
	    x, y = G.node[node]['pos']
	    node_trace['x'].append(x)
	    node_trace['y'].append(y)

	node_trace['marker']['color'].append(0)
	for i, node in enumerate(top_collab):
	    node_trace['marker']['color'].append(len(G.adj[i+1][0]))
	    # add annotation if greater than 0
	    node_info = '# of connections: '+str(len(G.adj[i+1][0]))
	    node_info += '<br>' + '<br>'.join([str(tup[1])+': '+str(tup[0]) for tup in top_collab[i][1]])
	    node_trace['text'].append(node_info)
	#return node_trace, edge_trace, annots
	return Figure(data=Data([edge_trace, node_trace]),
             layout=Layout(
                title=artist + "'s Top Five Collaborators", #'<br>Network graph made with Python',
                titlefont=dict(size=16),
                showlegend=False,
                hovermode='closest',
                margin=dict(b=20,l=5,r=5,t=40),
                annotations= annots,
                xaxis=XAxis(showgrid=False, zeroline=False, showticklabels=False),
                yaxis=YAxis(showgrid=False, zeroline=False, showticklabels=False)))

# run the above functions to visualize top five collabs
def visualize(artist,token):
	collabs = discog(artist,token)
	top_five = collabs[:5]

	node_trace, edge_trace, annots = construct_g(artist,top_five,token)
	fig = Figure(data=Data([edge_trace, node_trace]),
	             layout=Layout(
	                title=artist + "'s Top Five Collaborators", #'<br>Network graph made with Python',
	                titlefont=dict(size=16),
	                showlegend=False,
	                hovermode='closest',
	                margin=dict(b=20,l=5,r=5,t=40),
	                annotations= annots,
	                xaxis=XAxis(showgrid=False, zeroline=False, showticklabels=False),
	                yaxis=YAxis(showgrid=False, zeroline=False, showticklabels=False)))

	py.iplot(fig, filename=artist+"'s Collaborators")
