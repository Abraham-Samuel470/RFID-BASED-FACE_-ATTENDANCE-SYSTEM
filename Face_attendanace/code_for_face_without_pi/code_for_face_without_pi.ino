#include <Wire.h>
#include <LiquidCrystal_I2C.h>
#include <SPI.h>
#include <MFRC522.h>

#define SS_PIN 10
#define RST_PIN 9
#define BUZZER 7
#define LED 6

MFRC522 rfid(SS_PIN, RST_PIN);
LiquidCrystal_I2C lcd(0x27, 16, 2);

void setup() {
    Serial.begin(9600);
    SPI.begin();
    rfid.PCD_Init();
    lcd.begin(16, 2);
    lcd.backlight();
    
    pinMode(BUZZER, OUTPUT);
    pinMode(LED, OUTPUT);
    
    lcd.setCursor(0, 0);
    lcd.print("Scan your card");
}

void loop() {
    if (!rfid.PICC_IsNewCardPresent() || !rfid.PICC_ReadCardSerial()) {
        return;
    }

    // Convert RFID data to a string
    String cardData = "";
    for (byte i = 0; i < rfid.uid.size; i++) {
        cardData += String(rfid.uid.uidByte[i], HEX);
    }

    lcd.clear();
    lcd.setCursor(0, 0);
    lcd.print("Face Verify...");

    Serial.println(cardData); // Send RFID to Python

    while (!Serial.available()); // Wait for Python response

    String response = Serial.readStringUntil('\n');
    response.trim();

    if (response != "Unauthorized") {
        lcd.clear();
       // Split response into Name and Roll Number
      int commaIndex = response.indexOf(',');
      String name = response.substring(0, commaIndex);    // Extract name
      String rollNo = response.substring(commaIndex + 1); // Extract roll number

      lcd.setCursor(0, 0); // Top line
      lcd.print(name);      // Print name
  
      lcd.setCursor(0, 1); // Second line
      lcd.print(rollNo);    // Print roll number

        digitalWrite(LED, HIGH);
        digitalWrite(BUZZER, HIGH);
        delay(500);
        digitalWrite(BUZZER, LOW);
        delay(2000);
        digitalWrite(LED, LOW);
    } else {
        lcd.clear();
        lcd.setCursor(0, 0);
        lcd.print("Access Denied!");
        digitalWrite(BUZZER, HIGH);
        delay(1000);
        digitalWrite(BUZZER, LOW);
    }

    rfid.PICC_HaltA();
    delay(2000);
}
