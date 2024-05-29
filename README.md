1. 環境 \
下記パッケージが必要です
```
sudo apt-get install python3-dev python3-pip python3-smbus i2c-tools
```
\
2. セットアップ \
以下のリポジトリをクローンして使用するpythonにインストールしてください
```
git clone https://github.com/pimoroni/VL53L0X-python.git
```
`VL53L0X-python/`で以下のコマンドを実行してインストールできます
```
sudo python3 setup.py install
```
\
3. トラブルシューティング \
エラーが出た場合、以下のコマンドでインストールされているディレクトリを調べられます
```
python3 -m site
```
`VL53L0X`がない場合下記コマンドで手動でインストールしてください
```
ls /usr/local/lib/python3.9/dist-packages/VL53L0X-1.0.4-py3.9-linux-aarch64.egg
```
```
sudo cp /usr/local/lib/python3.9/dist-packages/VL53L0X-1.0.4-py3.9-linux-aarch64.egg/vl53l0x_python.cpython-39-arm-linux-gnueabihf.so /usr/local/lib/python3.9/dist-packages/
```
