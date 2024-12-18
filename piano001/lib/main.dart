import 'package:flutter/material.dart';
import 'package:flutter_piano_pro/flutter_piano_pro.dart';
import 'package:flutter_piano_pro/note_model.dart';
import 'package:flutter_piano_pro/note_names.dart';
import 'package:flutter_midi_pro/flutter_midi_pro.dart';
import 'package:flutter_blue_plus/flutter_blue_plus.dart';
import 'dart:io';
import 'dart:convert';

void main() {
  WidgetsFlutterBinding.ensureInitialized();
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});
  @override
  Widget build(BuildContext context) {
    return const MaterialApp(
      title: 'Piano Demo',
      home: MidiPlayerScreen(),
    );
  }
}

class MidiPlayerScreen extends StatefulWidget {
  const MidiPlayerScreen({super.key});

  @override
  State<MidiPlayerScreen> createState() => _MidiPlayerScreenState();
}

class _MidiPlayerScreenState extends State<MidiPlayerScreen> {

  late MidiPro midiPro;
  late int soundfontId;
  Map<int, NoteModel> pointerAndNote = {};
  Map<int, Color> buttonColors = {
    0: Colors.white,
    1: Colors.black,
  };
  String infoText = '';

  BluetoothDevice? device;
  BluetoothCharacteristic? characteristic;

  @override
  void initState() {
    super.initState();
    midiPro = MidiPro();
    loadSoundFont();
    startBLE();
  }

  void loadSoundFont() async {
    // MIDIのサウンドフォントを読み込んでセットする
    soundfontId = await midiPro.loadSoundfont(
      path: "assets/sf2/Timbres_of_Heaven_XGM_4.00_G.sf2",
      //path: "assets/sf2/UprightPianoKW-small-20190703.sf2",
      //path: "assets/sf2/SGM-V2.01.sf2",
      bank:0, program: 0);
    await midiPro.selectInstrument(
      sfId: soundfontId, channel: 0, bank: 0, program: 0);
  }

  void startBLE() async {

    // Bluetoothがサポートされていることを確認
    if (await FlutterBluePlus.isSupported == false) {
      infoText += 'BLE not supported';
      return;
    }
    // Androidの場合のみBluetoothをONにする処理
    if (Platform.isAndroid) {
        await FlutterBluePlus.turnOn();
    }

    // Bluetoothが有効でパーミッションが許可されるまで待機
    await FlutterBluePlus.adapterState
      .where((val) => val == BluetoothAdapterState.on)
      .first;

    // スキャン開始
    await FlutterBluePlus.startScan(
      withNames:["RD_TOHO"],  // デバイス名で探す
      timeout: const Duration(seconds:15)
    );

    infoText += '(1)';

    FlutterBluePlus.onScanResults.listen((results) {
        if (results.isNotEmpty) {
            ScanResult r = results.last;
            device = r.device;
            infoText += 'deviceをセット ';
        }
      },
      onError: (e) {
        infoText += e.toString();
        return;
      }
    );

    do {
      await Future.delayed(const Duration(seconds: 1));
    } while (device == null);

    infoText += '(2)';

    // cleanup: cancel subscription when scanning stops
    //FlutterBluePlus.cancelWhenScanComplete(subscription);

    // wait for scanning to stop
    //await FlutterBluePlus.isScanning.where((val) => val == false).first;

/*
    // デバイスを取得
    device = FlutterBluePlus.connectedDevices.first;
    try {
      // 接続されたデバイスを取得
      List<BluetoothDevice> connectedDevices = FlutterBluePlus.connectedDevices;
      
      if (connectedDevices.isNotEmpty) {
        device = connectedDevices.first;
        //print('デバイスが接続されました: ${device!.advName}');
        infoText += 'デバイスが接続されました: ${device!.advName}';
      } else {
        //print('接続されたデバイスがありません');
        infoText += '接続されたデバイスがありません';
        return;
      }
    } catch (e) {
      //print('デバイスの初期化中にエラーが発生しました: $e');
      infoText += 'デバイスの初期化中にエラーが発生しました: $e';
      return;
    }
*/

    //////////////////////
    // BLEデバイスに接続
    //////////////////////

/*
    // listen for disconnection
    var subscription2 = device!.connectionState.listen((BluetoothConnectionState state) async {
        if (state == BluetoothConnectionState.disconnected) {
            // 1. typically, start a periodic timer that tries to 
            //    reconnect, or just call connect() again right now
            // 2. you must always re-discover services after disconnection!
            //print("${device.disconnectReason?.code} ${device.disconnectReason?.description}");
        }
    });

    // cleanup: cancel subscription when disconnected
    //   - [delayed] This option is only meant for `connectionState` subscriptions.  
    //     When `true`, we cancel after a small delay. This ensures the `connectionState` 
    //     listener receives the `disconnected` event.
    //   - [next] if true, the the stream will be canceled only on the *next* disconnection,
    //     not the current disconnection. This is useful if you setup your subscriptions
    //     before you connect.
    device!.cancelWhenDisconnected(subscription2, delayed:true, next:true);
*/

    if (device == null) {
      infoText += 'device取得できていません ';
      return;
    }

    try {
      // デバイスに接続
      await device!.connect();
      infoText = 'connectされました';
    } catch (e) {
      infoText = 'connectでエラーが発生しました: $e';
      return;
    }

    infoText += '(3)';

    try {
      // サービスを取得
      List<BluetoothService> services = await device!.discoverServices();
      for (BluetoothService service in services) {
        for (BluetoothCharacteristic chara in service.characteristics) {
          if (chara.properties.write) {
            characteristic = chara;
            //if (characteristic != null) break;
            break;
          }
        }
        if (characteristic != null) {
          infoText += 'characteristicをセット ';
          break;
        }
      }
    } catch (e) {
      infoText += 'discoverServicesでエラー発生: $e';
    }

    infoText += '(4)';

    do {
      await Future.delayed(const Duration(seconds: 1));
    } while (characteristic == null);

    if (characteristic == null) {
      infoText += 'characteristicを取得できません ';
      return;
    }

    infoText += '(5)';

    // cancel to prevent duplicate listeners
    //subscription.cancel();

    return;
  }

  bool isPlaying = false;
  NoteModel stopNote = const NoteModel(name: "//", noteIndex: 0, octave: 0, isFlat: false);

  void _playNote(NoteModel? note) {
    if (note!.name != "//") {
      midiPro.playNote(sfId: soundfontId, channel: 0,
          key: note.midiNoteNumber, velocity: 96); // 127では音割れするので96
    }

    String text = '';

    // BLEでデバイスに送信
    if (device == null) {
      infoText += 'deviceがnullです';
    }
    else if (characteristic == null) {
      infoText += 'characteristicがnullです';
    }
    else {
      text = note.name + (note.octave+1).toString();
      if (note.isFlat) {
        if      (note.name == 'D') { text = 'C'; }
        else if (note.name == 'E') { text = 'D'; }
        else if (note.name == 'G') { text = 'F'; }
        else if (note.name == 'A') { text = 'G'; }
        else if (note.name == 'B') { text = 'A'; }
        else { text = note.name; }
        text += (note.octave+1).toString();
        text += '#';
      }
      List<int> textBytes = utf8.encode(text);
      characteristic!.write(textBytes, withoutResponse: true);
      infoText += "$text ";
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Piano Demo'),
      ),
      body: Column(
        mainAxisSize: MainAxisSize.min,
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          TextField(
            decoration: const InputDecoration(
              border: OutlineInputBorder(),
            ),
            //controller: TextEditingController(text: 'Text to send'),
            controller: TextEditingController(text: infoText),
          ),
          PianoPro(
            blackWidthRatio: 1.3,
            buttonColors: buttonColors,
            expand: true,
            firstNoteIndex: 3, // 左端Fから
            firstOctave: 3,
            noteCount: 15, // 白鍵の数
            noteType: NoteType.english, // A〜G
            //whiteHeight: 200,
            showNames: false,
            showOctave: false,
            onTapDown: (note, tapId) {
              if (note == null) return;
              isPlaying = true;
              setState(() => pointerAndNote[tapId] = note);
              _playNote(note);
            },
            onTapUpdate: (note, tapId) {
              if (note == null) return;
              isPlaying = true;
              if (pointerAndNote[tapId] == note) return;
              setState(() => pointerAndNote[tapId] = note);
              _playNote(note);
            },
            onTapUp: (tapId) {
              isPlaying = false;
              setState(() => pointerAndNote.remove(tapId));
              _playNote(stopNote);
            },
          ),
        ],
      )
    );
  }
}


//  // showOkDialog()の使い方
//  ElevatedButton(
//    child: const Text('確認ダイアログを表示'),
//    onPressed: () async {
//      await showOkDialog(context, 'ほんまにええのんか？');
//    },
//  ),

Future showOkDialog(BuildContext context, String title, [String content='']){
  return showDialog(
    context: context,
    barrierDismissible: false,
    builder: (BuildContext dialogContext) {
      return AlertDialog(
        title: Text(title),
        content: Text(content),
        actions: <Widget>[
          ElevatedButton(
            child: const Text("OK"), //確認
            onPressed: () {
              Navigator.pop(dialogContext);
            },
          ),
        ],
      );
    },
  );
}
