# モジュールのインポート
import re
import csv
import time
import MeCab
import random
import pandas as pd
from statistics import mean

# PN Tableを読み込み
# パスは各自適当なものになります
pn_df = pd.read_csv('pn_ja.dic.txt',\
                    sep=':',
                    encoding='SHIFT-JIS',
                    names=('Word','Reading','POS', 'PN')
                   )

# MeCabインスタンス作成
m = MeCab.Tagger('')  # 指定しなければIPA辞書


# -----テキストを形態素解析して辞書のリストを返す関数----- #
def get_diclist(text):
    parsed = m.parse(text)      # 形態素解析結果（改行を含む文字列として得られる）
    lines = parsed.split('\n')  # 解析結果を1行（1語）ごとに分けてリストにする
    lines = lines[0:-2]         # 後ろ2行は不要なので削除
    diclist = []
    for word in lines:
        l = re.split('\t|,',word)  # 各行はタブとカンマで区切られてるので
        d = {'Surface':l[0], 'POS1':l[1], 'POS2':l[2], 'BaseForm':l[7]}
        diclist.append(d)
    return(diclist)

# PN Tableをデータフレームからdict型に変換しておく
word_list = list(pn_df['Word'])
pn_list = list(pn_df['PN'])  # 中身の型はnumpy.float64
pn_dict = dict(zip(word_list, pn_list))


# 形態素解析結果の単語ごとdictデータにPN値を追加する関数
def add_pnvalue(diclist_old):
    diclist_new = []
    for word in diclist_old:
        base = word['BaseForm']        # 個々の辞書から基本形を取得
        if base in pn_dict:
            pn = float(pn_dict[base])  # 中身の型があれなので
        else:
            pn = 'notfound'            # その語がPN Tableになかった場合
        word['PN'] = pn
        diclist_new.append(word)
    return(diclist_new)

# 各ツイートのPN平均値をとる関数
def get_pnmean(diclist):
    pn_list = []
    for word in diclist:
        pn = word['PN']
        if pn != 'notfound':
            pn_list.append(pn)  # notfoundだった場合は追加もしない
    if len(pn_list) > 0:        # 「全部notfound」じゃなければ
        pnmean = mean(pn_list)
    else:
        pnmean = 0              # 全部notfoundならゼロにする
    return(pnmean)



if __name__ == '__main__':
    text = input()
    a = get_pnmean(add_pnvalue(get_diclist(text)))
    print(a)