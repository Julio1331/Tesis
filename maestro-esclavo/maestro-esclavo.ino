//link del tutorial https://www.youtube.com/watch?v=KfxvCSsvWWc&ab_channel=Roboticoss
#include <ESP8266WiFi.h>
#include <ModbusTCPSlave.h>
#include <Ticker.h>

byte ip[]   ={192, 168, 1, 150};
byte gateway[]={192,168,1,1};
byte subnet[]={255,255,255,0}; 


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
