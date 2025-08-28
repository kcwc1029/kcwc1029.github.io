from max30102 import MAX30102
from utime import ticks_ms, ticks_diff


class IIR_filter(object):
    def __init__(self, alpha):
        self.old_value = 0
        self.alpha = alpha

    def step(self, value):
        value = (self.old_value*self.alpha
                 + value*(1 - self.alpha))
        self.old_value = value
        return value


class AC_extractor(object):
    def __init__(self):
        self.max_ac = 0
        self.min_ac = 0

        self.ac = 0

        self.cycle_time_mark = ticks_ms()
        self.get_time_mark = ticks_ms()

        self.is_down_period = False

    def update(self, value_nodc):
        if value_nodc > 0:
            if self.max_ac != 0 and self.min_ac != 0:
                self.is_down_period = False
                time_intval = ticks_diff(ticks_ms(), self.cycle_time_mark)
                if 2000 > time_intval > 270:
                    self.ac = self.max_ac - self.min_ac
                    self.get_time_mark = ticks_ms()
                self.max_ac = 0
                self.min_ac = 0
                
                self.cycle_time_mark = ticks_ms()
            else:
                if value_nodc > self.max_ac:
                    self.max_ac = value_nodc
        elif value_nodc < 0 and self.max_ac != 0:
            self.is_down_period = True
            if value_nodc < self.min_ac:
                self.min_ac = value_nodc

    def reset_ac(self):
        self.ac = 0


class HR_calculator(object):
    def __init__(self, target_n_beats=5):
        self.target_n_beats = target_n_beats
        self.n_beats = 0

        self.heart_rate = 0.0

        self.tot_intval = 0

        self.beat_time_mark = ticks_ms()

        self.is_beating = False

    def update(self, is_beating):
        if self.is_beating == False and is_beating == True:
            rr_intval = ticks_diff(ticks_ms(), self.beat_time_mark)
            if 2000 > rr_intval > 270:
                self.n_beats += 1
                self.tot_intval += rr_intval
                if self.n_beats == self.target_n_beats:
                    tot_intval = self.tot_intval/1000
                    self.heart_rate = self.target_n_beats/(tot_intval/60)
                    self.tot_intval = 0
                    self.n_beats = 0
            else:
                self.tot_intval = 0
                self.n_beats = 0

            self.beat_time_mark = ticks_ms()
        self.is_beating = is_beating

    def get_heart_rate(self):
        return self.heart_rate


class Pulse_oximeter(object):
    def __init__(self, sensor):
        sensor.set_led_mode(2)
        self.sensor = sensor

        self.raw_ir = 0
        self.raw_red = 0

        self.spo2 = 0
        self.heart_rate = 0

        self.is_beating = False
        self.is_available = False

        self.ac_extractor_ir = AC_extractor()
        self.ac_extractor_red = AC_extractor()

        self.dc_remover_ir = IIR_filter(0.99)
        self.dc_remover_red = IIR_filter(0.99)

        self.hr_calculator = HR_calculator()

    def update(self):
        self.spo2 = 0
        self.sensor.check()
        if (self.sensor.available()):
            self.is_available = True
            self.raw_ir = self.sensor.pop_ir_from_storage()
            self.raw_red = self.sensor.pop_red_from_storage()

            ir_dc = self.dc_remover_ir.step(self.raw_ir)
            red_dc = self.dc_remover_red.step(self.raw_red)

            ir_nodc = self.raw_ir - ir_dc
            red_nodc = self.raw_red - red_dc

            self.ac_extractor_ir.update(ir_nodc)
            self.ac_extractor_red.update(red_nodc)

            ir_ac = self.ac_extractor_ir.ac
            red_ac = self.ac_extractor_red.ac

            time_mark_ir = self.ac_extractor_ir.get_time_mark
            time_mark_red = self.ac_extractor_red.get_time_mark

            self.is_beating = self.ac_extractor_red.is_down_period

            self.hr_calculator.update(self.is_beating)
            self.heart_rate = self.hr_calculator.get_heart_rate()

            ir_red_intval = abs(ticks_diff(time_mark_ir, time_mark_red))
            if ir_ac > 0 and red_ac > 0:
                if ir_red_intval < 100:
                    ratio = (red_ac/red_dc)/(ir_ac/ir_dc)
                    self.spo2 = -45.060*ratio**2 + 30.354*ratio + 94.845
                
                self.ac_extractor_ir.reset_ac()
                self.ac_extractor_red.reset_ac()
        else:
            self.is_available = False

    def available(self):
        return self.is_available

    def get_spo2(self):
        return self.spo2

    def get_raw_ir(self):
        return self.raw_ir

    def get_raw_red(self):
        return self.raw_red

    def get_heart_rate(self):
        return self.heart_rate