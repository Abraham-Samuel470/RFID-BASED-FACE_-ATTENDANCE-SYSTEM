# RFID-BASED FACE RECOGNITION ATTENDANCE SYSTEM

## 📌 Project Overview
This project is an **RFID and Face Recognition-based Attendance System** using **Arduino, Python, and MySQL**. It ensures **two-factor authentication** by verifying an RFID card and then matching the person's face before marking attendance.

## 🛠 Hardware Components
- **Arduino Uno** (Microcontroller)
- **RC522 RFID Module** (For scanning RFID cards)
- **16x2 LCD Display (I2C)** (To display messages)
- **Buzzer** (For access feedback)
- **LED Indicator** (Shows attendance confirmation)
- **DS3231 RTC Module** (For real-time clock data)
- **Webcam** (For face recognition)

## 🔌 Pin Connections
### **RC522 RFID Module → Arduino Uno**
| RFID Pin | Arduino Pin |
|----------|------------|
| SDA      | 10         |
| SCK      | 13         |
| MOSI     | 11         |
| MISO     | 12         |
| GND      | GND        |
| RST      | 9          |
| 3.3V     | 3.3V       |

### **LCD (I2C) → Arduino Uno**
| LCD Pin | Arduino Pin |
|---------|------------|
| VCC     | 5V         |
| GND     | GND        |
| SDA     | A4         |
| SCL     | A5         |

### **Buzzer & LED → Arduino Uno**
| Component | Arduino Pin |
|-----------|------------|
| Buzzer    | 7          |
| LED       | 6          |

### **DS3231 RTC → Arduino Uno**
| RTC Pin | Arduino Pin |
|---------|------------|
| VCC     | 5V         |
| GND     | GND        |
| SDA     | A4         |
| SCL     | A5         |


## 📦 Required Libraries
### **Arduino Libraries**
1. `Wire.h` (For I2C communication)
2. `LiquidCrystal_I2C.h` (For LCD display)
3. `SPI.h` (For RFID communication)
4. `MFRC522.h` (For RFID functionality)
5. `RTClib.h` (For RTC functionality)


### **Python Libraries**
1. `opencv-python` (For webcam access)
2. `face_recognition` (For face detection and recognition)
3. `serial` (For Arduino communication)
4. `flask` (For web integration)
5. `mysql-connector-python` (For MySQL database connection)
6. `numpy` (For image processing)

## 🚀 Setup & Installation
### **1. Install Required Arduino Libraries**
- Open Arduino IDE → Sketch → Include Library → Manage Libraries
- Search and install:
  - `LiquidCrystal_I2C`
  - `MFRC522`
  - `RTClib`


### **2. Install Required Python Packages**
Run the following command in the terminal:
```sh
pip install opencv-python face_recognition pyserial flask mysql-connector-python numpy
```

### **3. Upload Arduino Code**
1. Open `arduino_code.ino` in **Arduino IDE**.
2. Select **Board:** `Arduino Uno` and correct **Port**.
3. Click **Upload**.

### **4. Setup MySQL Database**
1. Install **XAMPP** and start **MySQL**.
2. Open **phpMyAdmin** and create a database named `attendance_db`.
3. Run the following SQL commands to create the table:
```sql
CREATE TABLE Attendance (
    id INT AUTO_INCREMENT PRIMARY KEY,
    Name VARCHAR(50),
    RFID VARCHAR(20),
    Timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### **5. Run Python Code**
```sh
python face_attendance.py
```

### **6. Start the Web Interface**
```sh
python app.py
```
Then, open **http://127.0.0.1:5000** in a web browser.

## 📝 How It Works
1. **Scan the RFID card** → Camera opens.
2. **Face recognition starts** → If face matches the cardholder, attendance is recorded.
3. **Attendance is logged into MySQL** and stored on the **Attendance Records**.
4. **Buzzer and LED indicate success or failure**.
5. **Data is viewable on the Web Dashboard**.

## 📷 Web Dashboard
- Displays real-time attendance logs.
- Uses **Bootstrap** for a clean UI.
- Accessible at `http://127.0.0.1:5000`

## ⚡ Features & Future Enhancements
✅ **Two-factor authentication** (RFID + Face Recognition)
✅ **Web dashboard for monitoring**
✅ **Multiple attempts before rejection**
✅ **Real-time timestamp recording**

🔜 **Future Enhancements:**
- **Live streaming** on the web dashboard.
- **Admin panel** for user management.
- **Cloud database integration**.
- **Support for multiple RFID readers**.

---
### 🎯 **Contributors**
👤 **Your Name**  
📧 samu2004@gmail.com  
🔗 [GitHub:Abraham-Samuel470](https://github.com/Abraham-Samuel470/)

📢 Feel free to contribute and improve the project! 🚀

