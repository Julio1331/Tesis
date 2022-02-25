#include <ESP8266WiFi.h>

//const char* ssid = "MovistarFibra-4176B2_ext";
//const char* password = "valeruchi123";
const char* ssid = "motoe6";
const char* password = "julio1518";
int ModbusTCP_port = 502;

//////// Required for Modbus TCP / IP /// Requerido para Modbus TCP/IP /////////
#define maxInputRegister 20
//#define maxHoldingRegister 20
#define maxHoldingRegister 3000// si aca pongo 10000 y en el arreglo de flotantes y[]tambien, no se puede compilar, exede la memoria con 8000 solo queda el 20% de la memoria dinamica

#define MB_FC_NONE 0
#define MB_FC_READ_REGISTERS 3 //implemented
#define MB_FC_WRITE_REGISTER 6 //implemented
#define MB_FC_WRITE_MULTIPLE_REGISTERS 16 //implemented
//
// MODBUS Error Codes
//
#define MB_EC_NONE 0
#define MB_EC_ILLEGAL_FUNCTION 1
#define MB_EC_ILLEGAL_DATA_ADDRESS 2
#define MB_EC_ILLEGAL_DATA_VALUE 3
#define MB_EC_SLAVE_DEVICE_FAILURE 4
//
// MODBUS MBAP offsets
//
#define MB_TCP_TID 0
#define MB_TCP_PID 2
#define MB_TCP_LEN 4
#define MB_TCP_UID 6
#define MB_TCP_FUNC 7
#define MB_TCP_REGISTER_START 8
#define MB_TCP_REGISTER_NUMBER 10

byte ByteArray[260];
//unsigned int MBHoldingRegister[maxHoldingRegister];//original
int MBHoldingRegister[maxHoldingRegister];
//float MBHoldingRegister[maxHoldingRegister];

//////////////////////////////////////////////////////////////////////////

WiFiServer MBServer(ModbusTCP_port);

void setup() {

  pinMode(14, OUTPUT);

  Serial.begin(9600);
  delay(100) ;
  WiFi.begin(ssid, password);
  delay(100) ;
  Serial.println(".");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  MBServer.begin();
  Serial.println("Connected ");
  Serial.print("ESP8266 Slave Modbus TCP/IP ");
  Serial.print(WiFi.localIP());
  Serial.print(":");
  Serial.println(String(ModbusTCP_port));
  Serial.println("Modbus TCP/IP Online");

}
//variables para la funcion de prueba
float t = 0, tfin = 1, tpass = 0.002, aux, f = 100;
int amp = 5, ind = 0;
void loop() {
  //funcion a devolver en este caso va a ser una funcion seno de prueba
      
  // Check if a client has connected // Modbus TCP/IP




   MBHoldingRegister[0] = 0; //finaliza procesamiento



  
  WiFiClient client = MBServer.available();
  if (!client) {
    return;
  }


  boolean flagClientConnected = 0;
  byte byteFN = MB_FC_NONE;
  int Start;
  int WordDataLength;
  int ByteDataLength;
  int MessageLength;

  // Modbus TCP/IP
  while (client.connected()) {
    if (client.available())
    {
      flagClientConnected = 1;
      int i = 0;
      while (client.available())
      {
        ByteArray[i] = client.read();//lee 260 bytes
        i++;
      }

      client.flush();

      ///////// Holding Register [0] A [9] = 10 Holding Registers Writing
      // registros donde esribe el esclavo para enviar al maestro


//      //funcion a devolver en este caso va a ser una funcion seno de prueba
//      while (t <= tfin)
//      {
//        y[ind] = amp * sin(2 * PI * f * t);
//        ind++;
//        t = t+tpass;
//      }
      //asignación a los registros
//      for (i = 0; i < ind; i++)
//      {
//        MBHoldingRegister[i] = (y[i]+5)*100;
//        if(i == 1)
//        {
//          Serial.print("entro al for: ");  
//        }
//      }
      Serial.println("PASO CONTROL");

//      while(MBHoldingRegister[6] == 0)
//      {
//        Serial.println("esperando para empezar"); 
//      }
     
      if (t <= tfin)
      {
        MBHoldingRegister[0] = 1; //comienza procesamiento
        MBHoldingRegister[1] = amp * sin(2 * PI * f * t);
        MBHoldingRegister[2] = ((amp * sin(2 * PI * f * t))+5)*1000;
        MBHoldingRegister[3] = ind;
        MBHoldingRegister[4] = t;
        MBHoldingRegister[5] = ((amp * cos(2 * PI * f * t))+5)*1000;
        ind++;
        t = t+tpass;
        Serial.print("paso por if: ");
        Serial.print(MBHoldingRegister[2]);
        Serial.print(" anterior ");
        Serial.print(MBHoldingRegister[1]);
        delay(2);
      }else{
        MBHoldingRegister[0] = 0;        
      }
      
      //MBHoldingRegister[0] = 0; //finaliza procesamiento
      
//      MBHoldingRegister[10] = random(0, 12);
//      MBHoldingRegister[1] = random(0, 12);
//      MBHoldingRegister[2] = random(0, 12);
//      MBHoldingRegister[2] = random(0, 12);
//      MBHoldingRegister[4] = 44;
//      MBHoldingRegister[5] = -55;
//      MBHoldingRegister[6] = 66;
//      MBHoldingRegister[7] = random(0, 12);
//      MBHoldingRegister[8] = random(0, 12);
//      MBHoldingRegister[9] = random(0, 12);



      ///// Holding Register [10] A [19] = 10 Holding Registers Reading
      //registros donde escribe el maestro

      int Temporal[10];

//      Temporal[0] = MBHoldingRegister[3];
//      Temporal[1] = MBHoldingRegister[11];
//      Temporal[2] = MBHoldingRegister[12];
//      Temporal[3] = MBHoldingRegister[13];
//      Temporal[4] = MBHoldingRegister[14];
//      Temporal[5] = MBHoldingRegister[15];
//      Temporal[6] = MBHoldingRegister[16];
//      Temporal[7] = MBHoldingRegister[17];
//      Temporal[8] = MBHoldingRegister[18];
//      Temporal[9] = MBHoldingRegister[19];

      /// Enable Output 14
//      digitalWrite(14, MBHoldingRegister[14] );


      //// debug

//      for (int i = 0; i < 10; i++) {
//
//        Serial.print("[");
//        Serial.print(i);
//        Serial.print("] ");
//        Serial.print(Temporal[i]);
//
//      }
//      Serial.println("");


      //// rutine Modbus TCP
      byteFN = ByteArray[MB_TCP_FUNC];
      Serial.println("******************1");
      Serial.println(ByteArray[MB_TCP_REGISTER_START]);
      Serial.println(ByteArray[MB_TCP_REGISTER_START + 1]);
      Serial.println(ByteArray[MB_TCP_REGISTER_NUMBER]);
      Serial.println(ByteArray[MB_TCP_REGISTER_NUMBER + 1]);
      Serial.println("******************2");

      Start = word(ByteArray[MB_TCP_REGISTER_START], ByteArray[MB_TCP_REGISTER_START + 1]);
      WordDataLength = word(ByteArray[MB_TCP_REGISTER_NUMBER], ByteArray[MB_TCP_REGISTER_NUMBER + 1]);

      Serial.println(Start);
      Serial.println(WordDataLength);
      Serial.println("******************3");
    }

    // Handle request

    switch (byteFN) {
      case MB_FC_NONE:
        break;

      case MB_FC_READ_REGISTERS: // 03 Read Holding Registers
        ByteDataLength = WordDataLength * 2;
        ByteArray[5] = ByteDataLength + 3; //Number of bytes after this one.
        ByteArray[8] = ByteDataLength; //Number of bytes after this one (or number of bytes of data).
        for (int i = 0; i < WordDataLength; i++)
        {
          ByteArray[ 9 + i * 2] = highByte(MBHoldingRegister[Start + i]);
          ByteArray[10 + i * 2] = lowByte(MBHoldingRegister[Start + i]);
        }
        MessageLength = ByteDataLength + 9;
        client.write((const uint8_t *)ByteArray, MessageLength);

        byteFN = MB_FC_NONE;

        break;


      case MB_FC_WRITE_REGISTER: // 06 Write Holding Register
        MBHoldingRegister[Start] = word(ByteArray[MB_TCP_REGISTER_NUMBER], ByteArray[MB_TCP_REGISTER_NUMBER + 1]);
        ByteArray[5] = 6; //Number of bytes after this one.
        MessageLength = 12;
        client.write((const uint8_t *)ByteArray, MessageLength);
        byteFN = MB_FC_NONE;
        break;

      case MB_FC_WRITE_MULTIPLE_REGISTERS: //16 Write Holding Registers
        ByteDataLength = WordDataLength * 2;
        ByteArray[5] = ByteDataLength + 3; //Number of bytes after this one.
        for (int i = 0; i < WordDataLength; i++)
        {
          MBHoldingRegister[Start + i] = word(ByteArray[ 13 + i * 2], ByteArray[14 + i * 2]);
        }
        MessageLength = 12;
        client.write((const uint8_t *)ByteArray, MessageLength);
        byteFN = MB_FC_NONE;

        break;
    }
  }
}
