class PID():
    myP = 1.0
    myD = 1.0
    myI = 1.0

    gyro = 0.0
    acc = 0.0

    lastGyro = 0.0
    lastAcc = 0.0

    def set_PID(self,P,I,D):
        self.myP = P;
        self.myI = I;
        self.myD = D;

    def process(self, acc, gyro):
        self.lastGyro = gyro
        self.dGyro = gyro - self.lastGyro

        self.lastAcc = acc
        self.dAcc = acc - self.lastAcc

        return self.myP * acc + self.myD * gyro
