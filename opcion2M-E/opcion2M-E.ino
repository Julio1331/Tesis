#include <ESP8266WiFi.h>

//const char* ssid = "MovistarFibra-4176B2_ext";
//const char* password = "valeruchi123";
const char* ssid = "motoe6";
const char* password = "julio1518";
int ModbusTCP_port = 502;

//////// Required for Modbus TCP / IP /// Requerido para Modbus TCP/IP /////////
#define maxInputRegister 20
//#define maxHoldingRegister 20
#define maxHoldingRegister 20// si aca pongo 10000 y en el arreglo de flotantes y[]tambien, no se puede compilar, exede la memoria con 8000 solo queda el 20% de la memoria dinamica

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
unsigned int MBHoldingRegister[maxHoldingRegister];//original, unsigned e int son de 2bytes
//int MBHoldingRegister[maxHoldingRegister];
//float MBHoldingRegister[maxHoldingRegister];//no fue necesario usarlo

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
float t = 0, tfin = 0.1, tpass = 0.001, aux, f = 100;
int amp = 5, ind = 0;
void loop() {
  //funcion a devolver en este caso va a ser una funcion seno de prueba
   
  MBHoldingRegister[0] = 0; //bandera para inicio y fin de lectura desde pc

  // Check if a client has connected // Modbus TCP/IP 
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

      Serial.println("PASO CONTROL");
      // por cada loop del programa se realiza un calculo y su correspondiente transmision
      // por cada vuelta se escribe la bandera para que la pc siga leyendo junto con
      // los 5 datos de interes a transmitir
      // se les aplica un offset para convertir los valores negativos en positivos y 
      // tambien para convertir los reales en enteros y así no tener que modificar la 
      // transmision del codigo 
      if (t <= tfin) // este condicional se intento con un while pero no funciono
      {
        //señales a transmitir 
        MBHoldingRegister[0] = 1; //comienza procesamiento, es la bandera "funcionando"
        MBHoldingRegister[1] = ((amp * sin(2 * PI * f * t - 2.094))+5)*1000;
        MBHoldingRegister[2] = ((amp * sin(2 * PI * f * t))+5)*1000;
        MBHoldingRegister[3] = ((amp * sin(2 * PI * f * t + 2.094))+5)*1000;
        MBHoldingRegister[4] = ((amp * cos(2 * PI * f * t))+5)*1000;
        MBHoldingRegister[5] = MBHoldingRegister[2]+MBHoldingRegister[4];
        //
        Serial.print("tamaño arreglo y tiempo:  ");
        Serial.print(ind);
        Serial.println(t);
        ind++;
        t = t+tpass;
        Serial.print("paso por if: ");
        Serial.print(MBHoldingRegister[2]);
        Serial.print(" anterior ");
        Serial.print(MBHoldingRegister[1]);
      }else{//una vez terminado se coloca la bandera en cero para avisar 
        MBHoldingRegister[0] = 0;
        Serial.print("tamaño arreglo en el else: ");
        Serial.println(ind);
        Serial.print("tiempo en el else: ");
        Serial.println(t);
      }

      
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
