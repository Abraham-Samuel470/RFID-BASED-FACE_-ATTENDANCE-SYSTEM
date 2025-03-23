#include <Wire.h>
#include <LiquidCrystal_I2C.h>
#include <SPI.h>
#include <MFRC522.h>
#include <RTClib.h>

#define SS_PIN 10
#define RST_PIN 9
#define BUZZER 7
#define LED 6

MFRC522 rfid(SS_PIN, RST_PIN);
RTC_DS3231 rtc;
LiquidCrystal_I2C lcd(0x27, 16, 2); // LCD with I2C

void setup() {
    Serial.begin(9600);
    SPI.begin();
    rfid.PCD_Init();
    lcd.begin(16, 2);
    lcd.backlight();
    pinMode(BUZZER, OUTPUT);
    pinMode(LED, OUTPUT);
    
    if (!rtc.begin()) {
        Serial.println("Couldn't find RTC");
        while (1);
    }
    
    lcd.setCursor(0, 0);
    lcd.print("Scan your card");
}

void loop() {
    if (!rfid.PICC_IsNewCardPresent() || !rfid.PICC_ReadCardSerial()) {
        return;
    }

    String cardID = "";
    for (byte i = 0; i < rfid.uid.size; i++) {
        cardID += String(rfid.uid.uidByte[i], HEX);
    }

    Serial.println(cardID);  // Send RFID ID to Python
    lcd.clear();
    lcd.setCursor(0, 0);
    lcd.print("Face Verify...");

    // Wait for response from Python
    while (!Serial.available());

    String response = Serial.readStringUntil('\n');
    response.trim();

    if (response != "Unauthorized") {
        lcd.clear();
        lcd.setCursor(0, 0);
        lcd.print("Welcome, " + response);
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
