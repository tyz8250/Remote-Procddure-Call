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

#無限ループでクライアントからの接続を待つ
while True:
    #クライアントからの接続を受け入れる
    connection, client_address = sock.accept()
    try:
        print("connection from", client_address)
    
    # ループの開始。サーバが新しいデータを待ち続ける。
        while True:
            data = b''
            while True:
                chunk = connection.recv(16)  # 少しずつデータを受信
                if not chunk:
                    break  # クライアントが切断された場合
                data += chunk
                try:
                    json.loads(data.decode('utf-8'))
                    break  # 有効なJSONデータが受信できた
                except json.JSONDecodeError:
                    pass  # JSONがまだ完全でない場合は受信を続ける

            if not chunk:
                break  # クライアントが切断された場合

            # JSONデータを解析
            received_data = json.loads(data.decode('utf-8'))   
            print("Received ", received_data)

            # 関数を呼び出し、結果を取得
            answer = rpc_functions[received_data["method"]](*received_data["params"])
            print(answer)

            # 結果をJSON形式でクライアントに送信
            result_data = {
                "result": answer,
                "id": received_data["id"]
            }
            response_json = json.dumps(result_data).encode('utf-8')
            connection.sendall(response_json)

    finally:
        connection.close()