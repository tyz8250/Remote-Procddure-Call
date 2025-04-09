import math
import json
import socket
import os

#関数の定義

# floor(double x): 10 進数 x を最も近い整数に切り捨て、その結果を整数で返す。
def floor(x):
    return math.floor(x)

#nroot(int n, int x): 方程式 rn = x における、r の値を計算する。
def nroot(n, x):
    return x / n

#reverse(string s): 文字列 s を入力として受け取り、入力文字列の逆である新しい文字列を返す。
def reverse(s):
    return s[::-1]

#validAnagram(string str1, string str2): 2 つの文字列を入力として受け取り、
# 2 つの入力文字列が互いにアナグラムであるかどうかを示すブール値を返す。
def validAnagram(str1, str2):
    return sorted(str1) == sorted(str2)

#sort(string[] strArr): 文字列の配列を入力として受け取り、その配列をソートして、ソート後の文字列の配列を返す。
def arrySort(arry):
    arry2 = arry.sort()
    return arry2

#5つの関数を辞書化する
rpc_functions = {"floor": floor, "nroot": nroot, "reverse": reverse, "validAnagram": validAnagram, "arrySort": arrySort }
#jsonファイルの"method"を関数、"params"を引数とする

#以下サーバとしての処理

#UNIXソケットをストリームモードで作成する
sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)

socket_path = "/tmp/my_socket"

# 以前の接続が残っていた場合に備えて、サーバアドレスをアンリンク（削除）します
try:
    os.unlink(socket_path)
# サーバアドレスが存在しない場合、例外を無視します
except FileNotFoundError:
    pass
print('Starting up on {}'.format(socket_path))

#サーバアドレスにソケットをバインドする（接続する）
sock.bind(socket_path)

# ソケットが接続要求を待機
sock.listen(1)

print(f"Listening on {socket_path}")



#jsonファイルを受け取る処理
with open("data.json", "r", encoding="utf-8") as f:
    data = json.load(f)
print(data) #受け取ったjsonファイルを表示する。
#型の確認（関数に対応する型かどうか）
#受け取ったjsonファイルの"method"を確認し、引き渡し5つの関数のいずれかを返す
answer =  rpc_functions[data["method"]](*data ["params"])
print(answer)
#結果として、resultを作成する処理
result_data = {
    "result":answer,
    "id": data["id"]
}

with open("result.json", "w", encoding="utf-8") as f:
    json.dump(result_data, f, indent=4)
#resultをクライアントに返す処理