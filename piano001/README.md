# interior

A new Flutter project.

## Getting Started

This project is a starting point for a Flutter application.

A few resources to get you started if this is your first Flutter project:

- [Lab: Write your first Flutter app](https://docs.flutter.dev/get-started/codelab)
- [Cookbook: Useful Flutter samples](https://docs.flutter.dev/cookbook)

For help getting started with Flutter development, view the
[online documentation](https://docs.flutter.dev/), which offers tutorials,
samples, guidance on mobile development, and a full API reference.



# famicha

FamiCha (Family Chat)


## Libraries

使っているライブラリ。それぞれクラウド側の設定が必要。

### Firebase

- https://console.firebase.google.com/?hl=ja
- Android用設定ファイル
    - android/app/google-services.json （ダウンロードしたもの。アクセスキーを含む）
    - android/build.gradle
    - android/app/build.gradle
- iOS用設定ファイル
    - ios/Google-Service-Info.plist
    （これはXcodeプロジェクトのRunner/Google-Service-Info.plist にインストールされる）

### Firebase / Cloud Firestore

- FirebaseコンソールからFirestore Databaseを選択
- 初期状態はテストモード（30日間有効）になっているので注意

### Firebase / Authentication

- FirebaseコンソールからをAuthentication選択
- サンプルコード https://pub.dev/packages/firebase_auth/example
- GitHub https://github.com/firebase/flutterfire/tree/master/packages/firebase_auth/firebase_auth/example/lib
- Google認証は、
    - Firebase →「ユーザーと権限」に famichahelp@gmail.com を登録。
    - 新アカウントでFirebaseに入ってサポートメールを変更する。その後の作業はこのアカウント下で行う。
    - Authentication → Sign-in method → 新しいプロバイダを追加 → Googleを追加
    - SHA1 フィンガープリントを追加するが、デバッグ用のものを使う。最終的にはリリース用に差し替える必要がある。

別名: androiddebugkey
作成日: 2021/07/30
エントリ・タイプ: PrivateKeyEntry
証明書チェーンの長さ: 1
証明書[1]:
所有者: C=US, O=Android, CN=Android Debug
発行者: C=US, O=Android, CN=Android Debug
シリアル番号: 1
有効期間の開始日: Fri Jul 30 15:43:29 JST 2021 終了日: Sun Jul 23 15:43:29 JST 2051
証明書のフィンガプリント:
	 MD5:  F0:3E:02:37:CF:ED:B4:51:A8:23:07:67:41:DA:D0:15:BF:7F:26:47
	 SHA1: F0:3B:7C:46:B9:8E:93:61:8F:2B:4A:70:73:8A:68:61:5A:6D:76:5F:C7:93:CA:BB:DC:68:3D:6D:80:CF:3E:C8
	 SHA256: SHA1withRSA (弱)
署名アルゴリズム名: 2048ビットRSA鍵
サブジェクト公開鍵アルゴリズム: 1
バージョン: {10}

Warning:
証明書 uses the SHA1withRSA signature algorithm which is considered a security risk. This algorithm will be disabled in a future update.


### GCP / Google Maps for Flutter

APIキーを入手するには、Googleにログインしてクレジットカード登録が必要。
ただし手動で有料アカウントに変更しない限り課金されることはない。

参考 https://zuma-lab.com/posts/flutter-google-maps-with-location

- https://mapsplatform.google.com/?hl=ja
- Android用 API Key
    - android/app/src/main/AndroidManifest.xml
- iOS用 API Key
    - ios/Runner/AppDelegate.swift
    - ios/Runner/Info.plist

### Google AdMob

- https://admob.google.com/home/
- アプリリリース後に再設定が必要。
- Android用 API Key
    - android/app/src/main/AndroidManifest.xml
- iOS用 API Key
    - ios/Runner/Info.plist

## Files

開発のため意識しておくべきファイル。

- README.md - このファイル
- pubspec.yaml - 環境設定
- l10n.yaml - 多言語対応の設定

- lib - ソースコード
- lib/assets/icon.png - アプリアイコン
- lib/l10n/app_en.arb - 英語メッセージ
- lib/l10n/app_ja.arb - 日本語メッセージ

- android/app/build.gradle - 「注意:詳細は、-Xlint:uncheckedオプションを指定して再コンパイルしてください。」のエラー対策
- android/app/src/main/kotlin/jp/ee3/famicha/famicha/MainActivity.kt - 自動生成されたファイル？

- ios/Podfile - podコマンドのエラー対策
- ios/MLKitVision.podspec.json
- ios/MLKitCommon.podspec.json

## Release

本番リリース時の注意事項

- Googleリリース
- main.dart で、releaseForApple を false に設定
- print()を削除する
- ページングサイズ_pagingSize、invisibleItemsThresholdを再確認
- Firebaseの料金プランを確定。Blazeは無償枠を使い果たしたら課金される。
  Sparkは無償枠消費後サービス停止される。過去には固定性のプランもあったようなので調査が必要。
- Firestoreのセキュリティ設定
- Cloud Storageのセキュリティ設定
- Google認証のフィンガープリントを本番用に変更。
- Google Map のAPIキーを制限する
- AdMobが本番用の設定になっているか？

https://gakogako.com/flutter_android_release/ を参照
- keystoreファイルを作る
  keytool -genkey -v -keystore ./key.jks -keyalg RSA -keysize 2048 -validity 10000 -alias key
  パスワード: famicha_u4BJsjcA
  国コード: JP
  よろしいですか: はい
  作成された key.jks は android/app に配置する。
- android/key.properties を作る
- リリースビルド
  flutter build appbundle
- 改版するときはflutterVersionCodeの変更が必要
    android/app/build.gradle - flutterVersionCodeを編集する
- Google Play Console の 設定 > アプリの署名 に表示される SHA-1 および SHA-256 のフィンガープリントを、
   Firebaseのプロジェクトの設定 > SHA証明書フィンガープリントにコピーする

- Appleリリース
https://zenn.dev/moutend/articles/feebf0120dce6e6426fa
https://docs.flutter.dev/deployment/ios
- main.dart で、releaseForApple を true に設定
- pubspec.yaml のバージョン名を更新・確認
- リリースビルド
    flutter build ipa
- Transporterでアップロードする
    /Users/ma/AndroidStudioProjects/famicha/build/ios/ipa/FamiCha.ipa

## ToDo

- 利用規約（プライバシーポリシー含む）の文面をサポートサイトに作成（日本語）
- 利用規約（プライバシーポリシー含む）の文面をサポートサイトに作成（英語）

<次バージョン>
- 表示するメッセージの時間範囲の設定、ロケーションの限定、言語での限定
- Apple ID でサインイン（iOS用リリースでは、Google認証だけの実装では拒否される）
- 本番環境とは別に開発環境を作る
- 管理用のスペシャルバージョンを作る
- ブレークポイントの使い方を調べる
- Google Map お気に入りのインポート＆エクスポート
- 通知機能を実装する
    - users/{uid}/notificationの機能をやめる
    - Apple Developer Program が必要なのでiOSは後回し
    - 通知があったら自動で表示する(ファミリー招待含む)
    - 通知がなかったら何も表示しない


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

