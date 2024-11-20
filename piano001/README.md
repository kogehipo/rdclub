## Getting Started

This project is a starting point for a Flutter application.

A few resources to get you started if this is your first Flutter project:

- [Lab: Write your first Flutter app](https://docs.flutter.dev/get-started/codelab)
- [Cookbook: Useful Flutter samples](https://docs.flutter.dev/cookbook)

For help getting started with Flutter development, view the
[online documentation](https://docs.flutter.dev/), which offers tutorials,
samples, guidance on mobile development, and a full API reference.


# Piano

プロジェクト名 piano001


## Note

- サウンドフォントはサイズ制限のためGitHubには置かない。別途ダウンロードして配置すること。実際に使うファイルはプログラム中に書いてある。

/assets/sf2/UprightPianoKW-small-20190703.sf2
/assets/sf2/Timbres_of_Heaven_XGM_4.00_G.sf2
/assets/sf2/SGM-V2.01.sf2

## Flutterコマンド

環境の管理

- flutter --version  バージョン表示
- flutter upgrade    Flutter SDK の最新版へのアップグレード
- flutter version v1.12.13+hotfix8  任意のバージョンに変更する
- flutter doctor     インストール状態の確認

- flutter --help     ヘルプ
- flutter create --org com.example sample  プロジェクトの作成
- flutter pub        ライブラリの更新
- flutter pub deps   ライブラリの依存関係の表示
- flutter run        アプリの起動（r:ホットリロード、R:ホットリスタート）
- flutter run --release  リリースモードで実行
- flutter run --debug    デバッグモードで実行
- flutter build apk  アンドロイド実機用のビルド
- flutter build ios  iOS実機用のビルド
- flutter install  iOS実機へのインストール
- flutter pub run flutter_launcher_icons:main  アプリアイコンの組み込み

- open -a Simulator  iOSシミュレータの起動
- /Users/ma/Library/Android/sdk/emulator/emulator -list-avds  Androidエミュレータ仮想デバイスの表示
- /Users/ma/Library/Android/sdk/emulator/emulator -avd Pixel_8_API_35

