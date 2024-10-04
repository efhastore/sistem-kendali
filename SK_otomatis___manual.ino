// Pin dan variabel
int sensorPin = A0;  // Pin analog untuk LM35 (sensor suhu)
int ledPin = 13;      // Pin digital untuk LED
String mode = "manual";  // Mode awal: manual (untuk kontrol LED)

// Fungsi setup() dijalankan sekali saat perangkat dinyalakan
void setup() {
  pinMode(ledPin, OUTPUT);  // Mengatur pin LED sebagai output
  Serial.begin(9600);       // Memulai komunikasi serial pada baud rate 9600
  
  // Mengirim pesan ke Serial Monitor untuk memberitahu mode awal
  Serial.println("Mode awal: manual");
  Serial.println("Ketik 'mode manual' atau 'mode otomatis' untuk mengganti mode.");
  Serial.println("Untuk kontrol manual, ketik 'ON' untuk menyalakan LED dan 'OFF' untuk mematikannya.");
}

// Fungsi loop() dijalankan berulang kali
void loop() {
  
  // Memeriksa apakah ada data yang tersedia di Serial
  if (Serial.available() > 0) {
    String input = Serial.readString();  // Membaca input dari Serial
    input.trim(); // Menghilangkan spasi atau karakter tak terlihat di awal dan akhir

    // Memeriksa jika input adalah perintah untuk mengubah mode
    if (input == "mode otomatis") {
      mode = "otomatis";  // Mengubah mode ke otomatis
      Serial.println("Mode diubah ke: otomatis");
    } 
    else if (input == "mode manual") {
      mode = "manual";    // Mengubah mode ke manual
      Serial.println("Mode diubah ke: manual");
    } 

    // Perintah dari Manual akan menjalankan program ini
    else if (mode == "manual") {
      // Mode manual: kontrol LED via Serial Monitor
      if (input == "ON") {
        digitalWrite(ledPin, HIGH);  // Menghidupkan LED
        Serial.println("LED: ON (manual)");  // Mengirimkan status LED ke Serial Monitor
      } 
      else if (input == "OFF") {
        digitalWrite(ledPin, LOW);   // Mematikan LED
        Serial.println("LED: OFF (manual)");  // Mengirimkan status LED ke Serial Monitor
      }
      else {
        Serial.println("Perintah tidak dikenal. Ketik 'ON' atau 'OFF'.");  // Pesan untuk input yang tidak valid
      }
    }
  }

  // Mode otomatis: kontrol LED berdasarkan sensor
  if (mode == "otomatis") {
    int nilaiAnalog = analogRead(sensorPin);  // Membaca nilai analog dari LM35
    float tegangan = nilaiAnalog * (5.0 / 1023.0);  // Menghitung tegangan dari nilai analog
    float lux2 = map(tegangan, 0, 5.0, 0, 1000); // Memetakan tegangan ke nilai lux (0-1000)

    Serial.print("ADC = ");  // Mengirimkan teks "ADC = " ke Serial Monitor
    Serial.println(tegangan); // Mengirimkan nilai tegangan ke Serial Monitor
    Serial.print("Lux = ");   // Mengirimkan teks "Lux = " ke Serial Monitor
    Serial.println(lux2);     // Mengirimkan nilai lux ke Serial Monitor

    // Logika kontrol otomatis berdasarkan nilai lux
    if (lux2 > 500) {
      digitalWrite(ledPin, HIGH);    // Menyalakan LED jika lux lebih dari 500
      Serial.println("LED: ON (otomatis)");  // Mengirimkan status LED ke Serial Monitor
    } 
    else if (lux2 <= 500) {
      digitalWrite(ledPin, LOW);     // Mematikan LED jika lux kurang dari atau sama dengan 500
      Serial.println("LED: OFF (otomatis)"); // Mengirimkan status LED ke Serial Monitor
    }
    
    delay(500);  // Delay 500 ms untuk pembacaan sensor agar tidak terlalu cepat
  }
}
