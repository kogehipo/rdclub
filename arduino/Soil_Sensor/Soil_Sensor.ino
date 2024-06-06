// RDクラブ 東邦インターナショナル
// 土壌湿度センサー
// ESP32 Dev Module
// ・LED回路
//   GND→抵抗→LED→16
// ・センサー
//   GND,VCC
//   D0→27
//   A0→26（DAC-2）

#define LED 16
#define RAIN_SENSOR_D 27
#define RAIN_SENSOR_A 26

void setup()
{
  Serial.begin(115200);

  // センサーのデジタル出力
  pinMode(RAIN_SENSOR_D, INPUT);

  // LEDをテスト点滅
  pinMode(LED, OUTPUT);
  for (int i=0; i<3; i++) {
    digitalWrite(LED, HIGH);
    delay(200);
    digitalWrite(LED, LOW);
    delay(200);
  }
}

void loop()
{
  // デジタル信号
  int D0 = digitalRead(RAIN_SENSOR_D);
  Serial.print("D=");
  Serial.print(D0);
  if (D0 == 0) digitalWrite(LED, HIGH);
  else digitalWrite(LED, LOW);

  Serial.print(" ");

  // アナログ信号
  int A0 = analogRead(RAIN_SENSOR_A);
  Serial.print("A=");
  Serial.println(A0);

  delay(500);
}
