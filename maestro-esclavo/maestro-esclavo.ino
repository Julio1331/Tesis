#include <ESP8266WiFi.h>
#include <ModbusTCPSlave.h>
#include <Ticker.h>

//#include <Servo.h>
//Servo myservo;
////serial communication
//String inputString = "";
//boolean isReceive = false;
////servo angle
//int angulo = 0;

byte ip[]   ={192, 168, 1, 150};
byte gateway[]={192,168,1,1};
byte subnet[]={255,255,255,0}; 
String Network = "MovistarFibra-4176B2_ext";
String Password = "valeruchi123";

Ticker Sample;
ModbusTCPSlave Mb;

void setup(){
  Serial.begin(9600);
  Mb.begin("MovistarFibra-4176B2_ext", "valeruchi123", ip, gateway, subnet);
  while (WiFi.status() != WL_CONNECTED){
    delay(500); 
  }
  Sample.attach_ms(100,Task);
  
//  myservo.attach(7);// salida servo
}

void loop(){
  Mb.Run();
  //Serial.println(angulo);
}
void Task(){
  //angulo = Mb.MBHoldingRegister[0];
  Serial.println(Mb.MBHoldingRegister[0]);
}
