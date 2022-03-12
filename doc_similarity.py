# 計算文章相似度
import numpy as np
import pandas as pd
import re
from scipy.spatial import distance_matrix
import pickle


# 清洗資料函數
def cleanText(text):
    # 移除數字, 空格(含跳行), 英文句點, 英文逗點
    # text = re.sub('\d|\s|\.|\,', '', text)
    # 移除空格(含跳行)
    text = re.sub('\s', '', text)
    # 移除 資料來源 / 本文參考 / 全文參考 / 引自 (含)以後的字元
    matchSite = re.search('資料來源|本文參考|全文參考|引自', text)
    if matchSite:
        text = text[:matchSite.span()[0]]
    return text


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

# 將人名與組織的key作為詞矩陣
wordDict = {**personDict, **orgDict}

# 建立詞頻矩陣
wordMatrix = {elem: list() for elem in wordDict}
for doc in storiesData['內文']:
    # 清洗資料
    doc = cleanText(doc)
    # 迴圈比對詞是否有在文章裡面
    for word in wordMatrix:
        if any([True if elem in doc else False for elem in wordDict[word]]):
            wordMatrix[word].append(1)
        else:
            wordMatrix[word].append(0)
# 詞頻矩陣轉為Df(row:文本 column:詞 value: 是否出現)
wordMatrix = pd.DataFrame(wordMatrix)

# 整理各篇文章相似度(minkowski_distance)
distanceMatrix = pd.DataFrame(
    distance_matrix(wordMatrix.values, wordMatrix.values), 
    index=wordMatrix.index, 
    columns=wordMatrix.index)

# 整理各篇文章對應的推薦文章
recommendDocs = dict()
for i in range(len(distanceMatrix)):
    recommendDocs[i] = list(distanceMatrix.iloc[i].sort_values().head(6).index)

# 儲存結果
savePath = f'./data/recommendDocs.pickle'
with open(savePath, 'wb') as handle:
    pickle.dump(recommendDocs, handle)