//UNIVERSIDAD DEL VALLE DE GUATEMALA
//CRISTIAN ANIBAL CATU RIERA 20295
//TRABAJO DE GRADUACIÓN - PLATAFORMAS DE APRENDIZAJE: PENDULO INVERTIDO

#include <TMC2130Stepper.h>
#include <AccelStepper.h>
#include <AS5600.h>
#include "STM32TimerInterrupt.h"
#include "STM32_ISR_Timer.h"
#include <ArduinoJson.h>  // Librería para trabajar con JSON

// Definición de pines

#define DIR_PIN   7
#define STEP_PIN  5
#define MISO_PIN  12
#define CS_PIN    10
#define SCK_PIN   13
#define MOSI_PIN  11
#define EN_PIN    4
int switch1 = 9;
int switch2 = 8;


// Crear objeto del driver TMC2130
TMC2130Stepper driver = TMC2130Stepper(EN_PIN, DIR_PIN, STEP_PIN, CS_PIN);

// Crear objeto de AccelStepper
AccelStepper stepper = AccelStepper(stepper.DRIVER, STEP_PIN, DIR_PIN);


//VARIABLES MOTOR STEPPER Y PENDULO
int vel_max2 = 32000;
int vel_max = 32000;
int aceleracion = 150000;
int corriente = 800;
int microsteps = 16;
float offset2 = 284;

//VARIABLES MUESTREO Y TIMER
int sensorInterval = 1;
int sensorInterval2 = 70;
int t_stepper = 2 ;
int modo =1;

// Variables para el controlador PID
float Kp = 1500; // Ganancia proporcional
float Ki = 5; // Ganancia integral
float Kd = 5; // Ganancia derivativa
float setpoint = 0.0; // El ángulo deseado del péndulo (vertical)

// Variables para el controlador VARIABLES DE ESTADO
float K1 = 2000; // Ganancia proporcional
float K2 = 20; // Ganancia integral
float K3 = 80; // Ganancia derivativa
float K4 = 0.4; // Ganancia derivativa


//Variables inicializadas
float previous_error = 0.0;
float integral = 0.0;
unsigned long last_time = 0;
unsigned long last_time1 = 0;
unsigned long previousSensorMillis = 0; 
unsigned long previousSensorMillis2 = 0; 

// Variables para desplazamiento del carro
float previousAngle1 = 0;
float previous_distance = 0;
float totalAngle1 = 0;
float initialAngle1 = 0;  // Nueva variable para el ángulo inicial
const float pulleyRadius = 12.7; // Radio de la polea en mm
float distance = 0;
float v_lineal = 0;
float delta_time1 = 0;
float angulo1 = 0;
float angulo2 = 0;
float angulo3 = 0;
float v_angular2 = 0;
bool datosRecibidos = false;
String inputString = "";
int direccion = 0;
float error = 0;
int encendido1 = 0;
int encendido2 = 0;
int punto = 0;
float output = 0;
float speed = 0.0;
float speed1 = 0.0;


// Definir el tamaño del buffer para el objeto JSON
StaticJsonDocument<200> jsonBuffer;

// Crear una segunda instancia de Wire para el segundo bus I2C
TwoWire Wire2; // Instancia del segundo bus I2C

AS5600 as5600_1;   // Primera instancia del sensor
AS5600 as5600_2(&Wire2);   // Segunda instancia del sensor utilizando Wire2

// -------------- TIMER PARA MOTOR STEPPER ----------------------
// Init STM32 timer TIM1
STM32Timer ITimer(TIM1);
// Init STM32 timer TIM1
STM32Timer ITimer2(TIM2);
// Init STM32_ISR_Timer
STM32_ISR_Timer ISR_Timer;

//TIMER 1
void runStepper()
{
  stepper.run();
}

//TIMER2 2
void readAngle()
{  
  // ----------------- LECTURA MOTOR -----------------------
  //---------------------------------------------------------
  angulo3 = as5600_1.rawAngle() * AS5600_RAW_TO_DEGREES;
  float v_angular1 = as5600_1.getAngularSpeed(AS5600_MODE_DEGREES);
  float deltaAngle1 = angulo3 - previousAngle1;
  if (deltaAngle1 > 180.0) {
      deltaAngle1 -= 360.0;
  } else if (deltaAngle1 < -180.0) {
      deltaAngle1 += 360.0;
  }
  totalAngle1 += deltaAngle1;
  previousAngle1 = angulo3;
  distance = (totalAngle1 / 360.0) * (2 * PI * pulleyRadius);
  v_lineal = (v_angular1 / 360.0) * (2 * PI * pulleyRadius);  


  //----------------- LECTURA PENDULO -----------------------------
  //----------------------------------------------------------------
    angulo1 = as5600_2.rawAngle() * AS5600_RAW_TO_DEGREES;
    v_angular2 = as5600_2.getAngularSpeed(AS5600_MODE_DEGREES);
    angulo2 = angulo1 - offset2;
    // Ajustar el ángulo para que esté en el rango -180° a 180°
    if (angulo2 > 180.0) {
      angulo2 -= 360.0;
    } else if (angulo2 <= -180.0) {
      angulo2 += 360.0;
    }
}

void setup() {
  //-------------------- INICIALIZACION MOTOR ---------------------------
    // Inicializar SPI y Serial
    SPI.begin();
    Serial.begin(115200);
    while (!Serial);
    Serial.println("Iniciando...");

    // Configurar pines
    pinMode(CS_PIN, OUTPUT);
    digitalWrite(CS_PIN, HIGH);

    // Inicializar driver TMC2130
    driver.begin();
    driver.rms_current(corriente);    // Establecer corriente del motor a 600mA
    driver.stealthChop(0);      // Activar modo silencioso
    driver.stealth_autoscale(0);
    driver.microsteps(microsteps);      // Establecer microsteps a 16

    driver.sg_stall_value(0);         // Umbral de stallGuard, ajustar según necesidad

    // Configurar stepper
    stepper.setMaxSpeed(vel_max);  // Velocidad máxima inicial (ajustable)
    stepper.setAcceleration(aceleracion); // Aceleración
    stepper.setEnablePin(EN_PIN);
    stepper.setPinsInverted(false, false, true);
    stepper.enableOutputs();

    //-------------- INICIALIZACION AS5600 ---------------
    Serial.println(__FILE__);
    Serial.print("AS5600_LIB_VERSION: ");
    Serial.println(AS5600_LIB_VERSION);

    Wire.setSDA(14);  // pin SDA //BLANCO
    Wire.setSCL(15);  // pin SCL //NARANJA
    Wire.begin();

    Wire2.setSDA(PB3);  // pin SDA para el segundo bus // BLANCO
    Wire2.setSCL(PB10);  // pin SCL para el segundo bus // NARANJA
    Wire2.begin();

    // Inicialización del primer sensor
    as5600_1.begin(4);  // set direction pin.
    as5600_1.setDirection(AS5600_CLOCK_WISE);  // default, just be explicit.

    // Leer el ángulo inicial y guardarlo
    initialAngle1 = as5600_1.rawAngle() * AS5600_RAW_TO_DEGREES;
    previousAngle1 = initialAngle1;

    // Inicialización del segundo sensor
    as5600_2.begin(5);  // dirección diferente en el segundo bus I2C
    as5600_2.setDirection(AS5600_CLOCK_WISE);  // default, just be explicit.
    // ------------------ INICIALIZACION TIMER -------------------
    ITimer.attachInterruptInterval(20000, readAngle);
    ITimer2.attachInterruptInterval(t_stepper, runStepper);
    
    //Configurar las prioridades de las interrupciones
    NVIC_SetPriority(TIM1_CC_IRQn, 1);
    NVIC_SetPriority(TIM2_IRQn, 0);

    // Habilitar las interrupciones en el NVIC
    NVIC_EnableIRQ(TIM1_CC_IRQn);
    NVIC_EnableIRQ(TIM2_IRQn);

    // ------------------ FINALES DE CARRERA -------------------

    pinMode(switch1, INPUT_PULLUP);
    pinMode(switch2, INPUT_PULLUP);
}

void loop() {
  // --------------------- RECIBIMIENTO DE DATOS ---------------------
  recibirDatos();
  if (datosRecibidos) {
    StaticJsonDocument<200> doc;
    DeserializationError error = deserializeJson(doc, inputString);
    if (doc.containsKey("modo")) {
      modo = doc["modo"];
    }
    if (doc.containsKey("offset")) {
      offset2 = doc["offset"];
    }
    if (doc.containsKey("t_muestreo")) {
      sensorInterval = doc["t_muestreo"];
    }

    switch(modo){
      case 1: {
        if (doc.containsKey("motor")) {
          speed1 = doc["motor"];
        }
        if (doc.containsKey("microstep")) {
          microsteps = doc["microstep"];
          driver.microsteps(microsteps);
        }
        if (doc.containsKey("velocidad_maxima")) {
          vel_max = doc["velocidad_maxima"];
        }
        if (doc.containsKey("aceleracion")) {
          aceleracion = doc["aceleracion"];
          stepper.setAcceleration(aceleracion);
        }
        if (doc.containsKey("amperaje")) {
          corriente = doc["amperaje"];
          driver.rms_current(corriente);
        }
        if (doc.containsKey("reiniciar")) {
          int reinicio = doc["reiniciar"];
          if (reinicio == 1) {
            totalAngle1 = 0;
            distance = 0;
          }
        }
        if (doc.containsKey("direccion")) {
          direccion = doc["direccion"];
        }
        break;
      }
      case 2: {
        if (doc.containsKey("kp")) {
          Kp = doc["kp"];
        }
        if (doc.containsKey("ki")) {
          Ki = doc["ki"];
        }
        if (doc.containsKey("kd")) {
          Kd = doc["kd"];
        }
        if (doc.containsKey("encendido1")) {
          encendido1 = doc["encendido1"];
        }
        if (doc.containsKey("stepper")) {
          t_stepper = doc["stepper"];
          ITimer2.attachInterruptInterval(t_stepper, runStepper);
        }
        if (doc.containsKey("direccion")) {
          direccion = doc["direccion"];
        }

        break;
      }
      case 3: {
        if (doc.containsKey("k1")) {
          K1 = doc["k1"];
        }
        if (doc.containsKey("k2")) {
          K2 = doc["k2"];
        }
        if (doc.containsKey("k3")) {
          K3 = doc["k3"];
        }
        if (doc.containsKey("k4")) {
          K4 = doc["k4"];
        }
        if (doc.containsKey("encendido2")) {
          encendido2 = doc["encendido2"];
        }
        if (doc.containsKey("punto")) {
          punto = doc["punto"];
        }
        if (doc.containsKey("direccion")) {
          direccion = doc["direccion"];
        }
        break;
      }
    }
    inputString = "";  // Limpiar la cadena para los siguientes datos
    datosRecibidos = false;
  }
// -------------------- STALL GUARD VALUE ---------------------
  //int stall_value = driver.sg_result();
  int lectura_switch1 = digitalRead(switch1);  // Lee el estado del pin (HIGH o LOW)
  int lectura_switch2 = digitalRead(switch2);

  unsigned long currentMillis2 = millis();
  if (currentMillis2 - previousSensorMillis2 >= sensorInterval2) {
    previousSensorMillis2 = currentMillis2;
    //-------------------- MANDAR DATOS JSON -----------------------------------
    JsonObject root = jsonBuffer.to<JsonObject>();
    root["d1"] = String(angulo2,4);
    root["d2"] = int(v_angular2);
    root["d3"] = int(distance);
    root["d4"] = int(v_lineal);
    root["d5"] = String(angulo1,3);
  
    // Convertir el objeto JSON a una cadena
    String jsonString;
    serializeJson(root, jsonString);
    
    // Enviar la cadena JSON por el puerto serie
    Serial.println(jsonString);
  }

  // ----------------------------- EMPIEZA CONTROLADOR ----------------------------------
  unsigned long currentMillis = millis();
  if (currentMillis - previousSensorMillis >= sensorInterval) {
    previousSensorMillis = currentMillis;
    
    switch(modo){
    // -------------- MODO PRUEBA MOTOR ------------
      case 1: {
        if (speed1 > vel_max) speed1 = vel_max;
        if (speed1 < -vel_max) speed1 = -vel_max;
        // Establecer la velocidad y dirección
        if (speed1 >= 0) {
            if (lectura_switch1 == 1) {
            stepper.setMaxSpeed(0);
          } else if (lectura_switch1 == 0) {  
            stepper.setMaxSpeed(speed1);
            stepper.moveTo(-1000000); // Mover hacia atrás
          }
        } else {
          if (lectura_switch2 == 1) {
            stepper.setMaxSpeed(0);
          } else if (lectura_switch2 == 0) {  
            stepper.setMaxSpeed(-speed1);
            stepper.moveTo(1000000); // Mover hacia atrás
          }
        }
        break;
      }

      case 2:{
        // ----------------- Controlador PID---------------------------
        if (encendido1 == 1){
          if (direccion == 0){
            error =  -angulo2;
          }
          else if (direccion == 1){
            error = angulo2;
          }    
          integral += error;
          float derivative = (error - previous_error);
          //output = (Kp * error * + Ki * integral *sensorInterval/1000 + Kd * derivative/(sensorInterval/1000))*3.1415*2/360;
          speed = Kp * error+ Ki * integral + Kd * derivative;
          previous_error = error;
          // Limitar el rango de la salida del PID
          if (speed > vel_max) speed = vel_max;
          if (speed < -vel_max) speed = -vel_max;
          // Establecer la velocidad y dirección
          if (speed >= 0) {
              if (lectura_switch1 == 1) {
              stepper.setMaxSpeed(0);
            } else if (lectura_switch1 == 0) {  
              stepper.setMaxSpeed(speed);
              stepper.moveTo(-1000000); // Mover hacia atrás
            }
          } else {
            if (lectura_switch2 == 1) {
              stepper.setMaxSpeed(0);
            } else if (lectura_switch2 == 0) {  
              stepper.setMaxSpeed(-speed);
              stepper.moveTo(1000000); // Mover hacia atrás
            }
          }
        }
        else{
          stepper.setMaxSpeed(0);
          integral = 0;
        }
        break;
      }

      case 3:{
        
        // ----------------- Controlador Variables de estado---------------------------
        if (encendido2 == 1){

          if (direccion == 0){
            output = - K1*angulo2 - K2*v_angular2 - K3*(distance-punto) - K4*v_lineal ;
          }
          else if (direccion == 1){
            output = K1*angulo2 + K2*v_angular2 - K3*(distance-punto) - K4*v_lineal ;
          }

          speed = output;
          // Limitar el rango de la salida del PID
          if (speed > vel_max) speed = vel_max;
          if (speed < -vel_max) speed = -vel_max;
          // Establecer la velocidad y dirección
          if (speed >= 0) {
              if (lectura_switch1 == 1) {
              stepper.setMaxSpeed(0);
            } else if (lectura_switch1 == 0) {  
              stepper.setMaxSpeed(speed);
              stepper.moveTo(-1000000); // Mover hacia atrás
            }
          } else {
            if (lectura_switch2 == 1) {
              stepper.setMaxSpeed(0);
            } else if (lectura_switch2 == 0) {  
              stepper.setMaxSpeed(-speed);
              stepper.moveTo(1000000); // Mover hacia atrás
            }
          }
        }
        else{
          stepper.setMaxSpeed(0);
        }

        break;
      }





    }

    /*
    // ------------------ MANDAR DATOS -----------------------------
    JsonObject root = jsonBuffer.to<JsonObject>();
    root["d1"] = angulo1;
    root["d2"] = v_angular1;
    root["d3"] = angulo2;
    root["d4"] = v_angular2;

    // Convertir el objeto JSON a una cadena
    String jsonString;
    serializeJson(root, jsonString);
    
    // Enviar la cadena JSON por el puerto serie
    Serial.println(jsonString);
    */
  }

    // ---------------------------------------- TERMINA MILLIS -----------------------------------------------------------------------------
}




void recibirDatos() {
  while (Serial.available()) {
    char inChar = (char)Serial.read();
    inputString += inChar;
    if (inChar == '\n') {  // Asume que el JSON termina con un salto de línea
      datosRecibidos = true;
    }
  }
}
