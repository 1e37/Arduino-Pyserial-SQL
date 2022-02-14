int ledPin = 13;           
int pirPin = 2;                
int pirStat = 0;  
char userInput;                 

void setup() {
 pinMode(ledPin, OUTPUT);     
 pinMode(pirPin, INPUT);     
 Serial.begin(9600);
}

void loop(){

if(Serial.available()> 0)
{
  userInput = Serial.read();
  if(userInput == 'g')
  {
pirStat = digitalRead(pirPin); 
 if (pirStat == HIGH) {            // if motion detected
   digitalWrite(ledPin, HIGH);  // turn LED ON
   Serial.println("Motion Detected");
 } 
 else {
   digitalWrite(ledPin, LOW); // turn LED OFF if we have no motion
   Serial.println("Motion End");
 }
  }
}
 
} 