

class PID:
    def __init__(self, P, I, D):
        self.P = P
        self.I = I
        self.D = D

        self.setpoint, self.previous_error, self.integral = 0, 0, 0

    def setSetpoint(self, setpoint):
        self.setpoint = setpoint

    def calculateSpeed(self, input):
        error = self.setpoint - input
        self.integral += (error * 0.0333)
        derivitave = error - self.previous_error
        self.previous_error = error
        speed = self.P*error + self.I*self.integral + self.D*derivitave
        return speed
