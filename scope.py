from enc_sim import Enc  # Virtual encoders: enc_sim; actual encoders: enc
import ephem


class Scope:
    def __init__(self, obj, ra, dec):
        # Offset initialized as tuple (tick_ha, tick_dec)
        self.offset = (ra.read(), dec.read())  # Encoder values at first sync
        self.t0 = ephem.now()  # Time at first sync
        #         rho.date = t0
        obj.compute()  # Compute where you say the scope is pointing in RA, DEC
        self.star = (float(obj.ra), float(obj.dec))  # Star at first sync in radians
        self.ra = ra
        self.dec = dec
        self.data = {'Time': [self.t0],  # Timestamp of initialization
                     'Ticks': [self.offset],  # Encoder positions in ticks
                     'Scope': [self.star],  # Scope position in RA, DEC
                     'Target': [self.star],  # Starting target is also the scope position
                     'Error': [(0.0, 0.0)]}  # For future use

    def use(self, target):
        """Input: target ephem object
        Output: Updates Scope properties"""
        time = ephem.now()  # Timestamp
        target.compute()  # compute star location at time now
        ticks = (self.ra.read(), self.dec.read())  # Current encoder read
        scope = (float((ticks[0] - self.offset[0]) / self.ra.rate()) + self.star[0],
                 float((ticks[1] - self.offset[1]) / self.dec.rate()) + self.star[1])
        target = (float(target.ra), float(target.dec))  # Current position of target in HA, DEC
        error = (scope[0] - self.data['Scope'][-1][0],
                 scope[1] - self.data['Scope'][-1][1])
        self.data['Time'].append(time)
        self.data['Ticks'].append(ticks)
        self.data['Scope'].append(scope)
        self.data['Target'].append(target)
        self.data['Error'].append(error)

    def where(self):
        ticks = (self.ra.read(), self.dec.read())  # Current encoder read
        position = (float((ticks[0] - self.offset[0]) / self.ra.rate) + self.star[0],
                 float((ticks[1] - self.offset[1]) / self.dec.rate) + self.star[1])
        return (str(ephem.hours(position[0]).norm),
                str(ephem.degrees(position[1]).znorm))

    def target(self):
        target = (self.data['Target'][-1][0], self.data['Target'][-1][1])
        return (str(ephem.hours(target[0]).norm),
                str(ephem.degrees(target[1]).znorm))

    def track(self):
        scope = (ephem.hours(self.where()[0]), ephem.degrees(self.where()[1]))
        target = (ephem.hours(self.target()[0]), ephem.degrees(self.target()[1]))
        return (str(ephem.hours(target[0] - scope[0])),
                str(ephem.degrees(target[1] - scope[1])))
