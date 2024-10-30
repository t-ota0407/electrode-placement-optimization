# Automated Electrode-Placement Optimizer

このプロジェクトでは、数値解析によって経皮電気刺激のパラメータを効率的に最適化することを目指しています。本システムは、膨大な電極配置条件に対して有限要素法による解析を行い、所望の組織を効率的に刺激する電極配置条件を調べます。

English version of the README is available [here](./README.md).

<img src="./demo.gif" alt="User interface of the optimization system" style="max-width: 80%; height: auto;">

## 特徴

* **複数部位に対応:** 上肢、下肢、頭部の経皮電気刺激の電極配置最適化に対応
* **詳細な最適化設定:** 単一組織の電流密度最大化だけでなく、他の組織の電流密度に関する条件付き最適化にも対応。後者のモードでは、詳細な制約条件の設定が可能
* **直感的で軽量なUI:** VisPyおよびPyQt5を用いて実装されたUIはGPUリソースを有効活用して描画処理を行うため軽量に動作する
* **詳細な結果の取得:** GUIでは確認しづらい詳細な結果はログを通して確認できる

## 動作環境

* Python 3.11.9
* COMSOL Multiphysics 6.0 &reg;
* COMSOL LiveLink for MATLAB &reg;

本システムは COMSOL Multiphysics &reg; および COMSOL LiveLink for MATLAB &reg; と併せて使用する。ただし、予め計算されてキャッシュされた結果のみを使用する場合は、これらを使用する必要はない。

本システムは[Windows版 Anaconda](https://www.anaconda.com/distribution/)環境でテストされています。以下のスクリプトにより検証に使用したAnaconda環境を再現できます。

```bash
cd [project root directory]/client
conda create -f env_elec_optim.yml
conda activate elecOptim
```

## データの準備
### キャッシュを使用する場合
1. キャッシュを準備する必要があります。後述する連絡先にキャッシュを使用したい旨を連絡してください。

### キャッシュを使用しない場合
1. 有限要素法のソルバーを準備する必要があります。[COMSOL Multiphysics &reg;](https://www.comsol.jp/comsol-multiphysics) および [COMSOL LiveLink for MATLAB &reg;](https://www.comsol.jp/livelink-for-matlab) を準備してください。
1. 本研究の論文を参考にして適切なモデルを作成してください。
1. 本研究の論文を参考にして適切にプログラムを修正してください。


## 使用方法
### キャッシュを使用する場合
1. `client/src/config.py` を以下のように書き換えてください。
    ```python
    USE_CACHE = True

    LOWER_LIMB_CACHE_DIR_PATH = [path to cache]
    UPPER_LIMB_CACHE_DIR_PATH = [path to cache]
    HEAD_CACHE_DIR_PATH = [path to cache]
    ```
1. 以下のコマンドを実行してシステムを起動させてください。
    ```bash
    cd client/src
    python main.py
    ```

### キャッシュを使用しない場合
1. `server/OptimizationServer.m` の変数を適切に書き換えてください。
1. COMSOL LiveLink for MATLAB &reg; を起動させた状態で、`server/OptimizationServer.m` を実行させてください。
1. client/src/config.py を以下のように書き換えてください。
    ```python
    USE_CACHE = False

    REMOTE_HOST = [remote host name]
    REMOTE_PORT = [port number]
    ```
1. 別のプロセスで、以下のコマンドを実行してシステムを起動させてください。
    ```bash
    cd client/src
    python main.py
    ```

## 補足事項

* LinuxおよびMacの環境ではテストを行っていません。
* 本リポジトリは、研究の一環で得られたプログラムの一部を公開するためのものです。研究の詳細は対応する論文をお読みください。
* 技術的な詳細情報は[こちら](./DEVELOPERS.md)を参照してください。


## リポジトリのコントリビューター

* Takashi Ota, The University of Tokyo, ota [at] cyber.t.u-tokyo.ac.jp  
* Kazuma Aoyama, The University of Tokyo (aoyama [at] vr.t.u-tokyo.ac.jp), Gunma University (aoyama [at] gunma-u.ac.jp)  

本研究の再現性確認のために必要なデータがあればメールでお問い合わせください

## ライセンス

このプロジェクトは[MITライセンス](https://en.wikipedia.org/wiki/MIT_License)のもとで提供されています。
