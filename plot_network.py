import pandas as pd
import re
import itertools
import networkx as nx
import plotly.graph_objects as go
import networkx as nx
import pickle

# 讀取資料
# 史料故事資料
storiesData = pd.read_excel('./data/storiesData.xls')

# 實體辨識人名整理清單
nerPersonData = pd.read_csv('./data/nerPersonData.csv')
personDict = dict()
for _, row in nerPersonData.iterrows():
    if personDict.get(row['synonym']):
        personDict[row['synonym']].append(row['word'])
    else:
        personDict[row['synonym']] = [row['word']]

# 實體辨識組織整理清單
nerOrgData = pd.read_csv('./data/nerOrgData.csv')
orgDict = dict()
for _, row in nerOrgData.iterrows():
    if orgDict.get(row['synonym']):
        orgDict[row['synonym']].append(row['word'])
    else:
        orgDict[row['synonym']] = [row['word']]

# 繪製網絡關係圖
def PlotNetwork(docClass, analysisType):

    # 依使用者選取類別取出文本
    if docClass == '全部':
        docs = list(storiesData['內文'])
    else:
        docs = list(storiesData[storiesData['分類'] == '世亞盟']['內文'])

    # 分析人名/組織
    if analysisType == 'ORG':
        analysisDict = orgDict
    elif analysisType == 'PERSON':
        analysisDict = personDict

    # 建立關係
    assoc_dictionary = dict()
    for article in docs:
        appears = []
        for elem in analysisDict:
            for name in analysisDict[elem]:
                if name in article:
                    appears.append(elem)
                    break
        relationships = itertools.combinations(sorted(appears),2)
        for relationship in relationships:
            if relationship in assoc_dictionary:
                assoc_dictionary[relationship] += 1
            else:
                assoc_dictionary[relationship] = 1

    # 隨機網絡點位
    G_ran = nx.random_geometric_graph(len(analysisDict), 0)
    G = nx.Graph()
    for elem, i in zip(analysisDict, range(len(analysisDict))):
        G.add_node(elem, pos = (G_ran.nodes[i]['pos'][0], G_ran.nodes[i]['pos'][1]))
    for edge, weight in assoc_dictionary.items():
        G.add_edge(edge[0], edge[1], weight=weight)
    edges = G.edges()
    weights = [G[u][v]['weight'] / len(docs) * 30 for u,v in edges]

    # 使用plotly
    # 記錄線的座標
    edge_x = []
    edge_y = []
    for edge in G.edges():
        x0, y0 = G.nodes[edge[0]]['pos']
        x1, y1 = G.nodes[edge[1]]['pos']
        edge_x.append(x0)
        edge_x.append(x1)
        edge_x.append(None)
        edge_y.append(y0)
        edge_y.append(y1)
        edge_y.append(None)
    # 記錄線的外觀
    edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=0.5, color='gainsboro'),
        hoverinfo='none',
        mode='lines')
    # 記錄點的座標
    node_x = []
    node_y = []
    for node in G.nodes():
        x, y = G.nodes[node]['pos']
        node_x.append(x)
        node_y.append(y)
    # 記錄點的外觀
    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode='markers',
        hoverinfo='text',
        marker=dict(
            showscale=True,
            colorscale='ice',
            reversescale=True,
            color=[],
            size=10,
            colorbar=dict(
                thickness=15,
                title='結點連結人數',
                xanchor='left',
                titleside='right'
            ),
            line_width=2))
    node_adjacencies = []
    node_text = []
    for node, adjacencies in enumerate(G.adjacency()):
        node_adjacencies.append(len(adjacencies[1]))
        node_text.append( adjacencies[0] + '的連結數: '+ str(len(adjacencies[1])))
    # 繪圖
    node_trace.marker.color = node_adjacencies
    node_trace.text = node_text
    fig = go.Figure(data=[edge_trace, node_trace],
                layout=go.Layout(
                    title= "",
                    titlefont_size=16,
                    showlegend=False,
                    hovermode='closest',
                    margin=dict(b=20,l=5,r=5,t=40),
                    height=900, width=1300, 
                    annotations=[ dict(
                        text="",
                        showarrow=False,
                        xref="paper", yref="paper",
                        x=0.005, y=-0.002 ) ],
                    xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                    yaxis=dict(showgrid=False, zeroline=False, showticklabels=False))
                    )
    
    return fig


# 繪製並儲存圖形
docClassList = ['全部','中國國民黨','中華救助總會','婦聯會','救國團','民眾服務社', 
                '中央日報社','三中案','革實院','黨營事業','世亞盟','松山油漆廠']
analysisTypeList = ['ORG', 'PERSON']
networkFigDict = dict()
for docClass in docClassList:
    iNetworkFigDict = dict()
    for analysisType in analysisTypeList:
        fig = PlotNetwork(docClass, analysisType)
        iNetworkFigDict[analysisType] = fig
    networkFigDict[docClass] = iNetworkFigDict

# 儲存圖形
saveFigName = f'./data/networkPlot.pickle'
with open(saveFigName, 'wb') as handle:
    pickle.dump(networkFigDict, handle)

# 讀取圖形
with open(saveFigName, 'rb') as handle:
    networkFigDict = pickle.load(handle)