class PID():
    myP = 1.0
    myD = 1.0
    myI = 1.0

    gyro = 0.0
    acc = 0.0

    lastGyro = 0.0
    lastAcc = 0.0

    def set_PID(self,P,I,D):
        myP = P;
        myI = I;
        myD = D;

    def process(self, acc, gyro):
        lastGyro = gyro
        dGyro = gyro - lastGyro

        lastAcc = acc
        dAcc = acc - lastAcc

        return myP * acc + myD * gyro
