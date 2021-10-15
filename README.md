# build-container-image-kube
build-container-image-kube は、エッジコンピューティング環境において、特定のエッジ端末でコンテナイメージをビルドするためのマイクロサービスです。  
たとえば コンテナデプロイメントシステムでは、本マイクロサービスは、デプロイ元のエッジ端末からデプロイ先のエッジ端末にデプロイするときに、デプロイ元のエッジ端末からデプロイ先のエッジ端末にコンテナイメージをプルする機能として利用されます。

### 動作環境 ###
* OS : Linux OS  
* CPU: ARM/AMD/Intel  
* Kubernetes  
* AION  

※ コンテナデプロイメントシステムにおける マイクロサービスのイメージビルドにあたっては、Base Imageのビルド、docker-private-repositoryへのPushが必要です。

### セットアップ ###

[1] マウントされた該当ストレージ領域におけるhome/端末名/Runtimeのディレクトリで、本マイクロサービスをクローンする

[2] 本マイクロサービスがクローンされているディレクトリ直下で、下記コマンドを実行し、イメージをビルドする。

```
$ sh docker-build.sh
```