#include <WiFi.h>
#include <HTTPClient.h>
#include "DHT.h"

#define DPIN 4
#define DTYPE DHT11
#define LED_PIN 23

DHT dht(DPIN, DTYPE);

// Pengaturan Wi-Fi
const char* ssid = "05";
const char* password = "barudak05";

// Pengaturan Firebase
const char* firebaseHost = "https://capstone-63601-default-rtdb.asia-southeast1.firebasedatabase.app"; // URL yang sudah di-update

void setup() {
  Serial.begin(9600);
  dht.begin();
  pinMode(LED_PIN, OUTPUT);

  // Koneksi ke Wi-Fi
  Serial.print("Menghubungkan ke ");
  Serial.println(ssid);
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("");
  Serial.println("WiFi terhubung");
  Serial.println("Alamat IP: ");
  Serial.println(WiFi.localIP());
}

void loop() {
  float temperatureC = dht.readTemperature(false);
  if (isnan(temperatureC)) {
    Serial.println("Gagal membaca dari sensor DHT!");
  } else {
    Serial.print("Suhu: ");
    Serial.print(temperatureC);
    Serial.println("°C");

    if (WiFi.status() == WL_CONNECTED) {
      HTTPClient http;
      String url = String(firebaseHost) + "/Temp.json"; // Endpoint yang sudah di-update
      Serial.print("Menghubungkan ke: ");
      Serial.println(url);

      http.begin(url);

      http.addHeader("Content-Type", "application/json");

      // Dapatkan timestamp Unix saat ini
      unsigned long currentMillis = millis() / 1000; // Ubah ke detik untuk timestamp Unix
      String jsonData = "{\"temperature\": " + String(temperatureC) + ", \"timestamp\": " + String(currentMillis) + "}";

      Serial.print("Mengirim data: ");
      Serial.println(jsonData);

      int httpResponseCode = http.POST(jsonData);

      if (httpResponseCode > 0) {
        String response = http.getString();
        Serial.print("Kode Respon HTTP: ");
        Serial.println(httpResponseCode);
        Serial.print("Respon: ");
        Serial.println(response);
      } else {
        Serial.print("Error saat mengirim POST: ");
        Serial.println(httpResponseCode);
        Serial.println(http.errorToString(httpResponseCode).c_str());
      }

      http.end();
    } else {
      Serial.println("WiFi tidak terhubung");
    }
  }

  digitalWrite(LED_PIN, HIGH);
  delay(100);
  digitalWrite(LED_PIN, LOW);

  delay(10000); // Delay 10 detik
}
