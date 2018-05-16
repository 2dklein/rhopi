import numpy as np
import matplotlib.pyplot as plt
import ephem as e, random as rn, time

# Create mock tick layout from data collected at RHO
# Set linear model params
# Expand to a full coordinate sys
# Query values from coordsys
# Show conversions

# Maximal value is 4294967295 (from hex FFFFFFFF to int)



def linear(x, y):
    m, b = np.polyfit(x, y, 1)  # Create linear best fit from data if needed
    return m, b


def tick_call(offset, cal, obj):
    # Where does the scope need to be pointed in order to see the given object?
    rr = -102.133333333  # Conversions found from prelim testing and linear best fit
    dd = -204.671666667  # [tick/degree]

    rrad = rr*(180./np.pi)  # Rate conversion to ticks/rads
    drad = dd*(180./np.pi)  # [ticks/rad]
    # print rrad, drad

    # Object ha - normalize to degrees from hours, convert to ticks
    ha = float(obj[0])
    dec = float(obj[1])

    # Find difference between aligned star and desired object
    hdiff = float(cal[0])-float(obj[0])
    ddiff = float(cal[1])-float(obj[1])

    # Find out what that diff is in ticks and add offset. This is where the telescope should be pointed to see obj
    ht_pos = hdiff * rrad + offset[0]
    dt_pos = ddiff * drad + offset[1]

    print 'HA [deg]:', ha, 'DEC:', dec
    print ht_pos, dt_pos



    ha_pos = (obj[0] * int(rr)) + (rr * (rn.random()-rn.random()) / 20) - offset[0]  # step * scope rate * [tick/deg] + 10% gaussian jitter
    dec_pos = (obj[1] * int(dd)) + (dd * (rn.random()-rn.random()) / 20) - offset[1]


ha = e.hours('21:08:00')  # Ephem returned HA during align
de = e.degrees('-11:14:18')  # Ephem DEC " "

# Massage data - hour angle goes from -12 to 11:59:59
if float(ha) > np.pi:
    ha = e.hours(ha - 2 * np.pi)  # Angle remains the same, but now goes from -12h to 12h

obj = [ha, de]
offset = [-3400, 120]
cal = [e.hours('0:48:30'), e.degrees('10:54:03')]

tick_call(offset, cal, obj)

# def tickspace(offset, timer, rate):

    # new_tick = int(randtick*randsign*100000)

    # ii = 1
    # rpath, dpath = [], []
    # while ii < timer:  # $timer is passed into the function to account for how long the telescope 'moves'
        # time.sleep(1)
        # ii += 1
        # rpath.append(ha_pos), dpath.append(dec_pos)
    # rpath, dpath are the coords the scope passes through

    # Linspace creates a set of equally spaced divisions on each arcminute for a full circle
    # ha = np.linspace(-1000000, 1000000, num=21600, endpoint=False)  # 24 hours * 15 deg/hr * 60 min/deg = 21600 [arcminutes]
    # dec = np.linspace(-10800, 10800, num=21600, endpoint=False)  # 360 deg * 60 min/deg = 21600 [arcminutes]
    # print ha, ha[5]-ha[4]
    # HA will have an offset from zenith (0). Similarly, the tickspace has an offset from 0.
    # Tickspace has a fixed position but we don't know how far off the scope is from the tickspace origin.
    # Aligning sets this offset
    # Align star will be Arcturus with HA: -2h08m00s and DEC: -11`14'18"
    # 1296000 = 60 * 60 * 360

    # return rpath, dpath  # Return the coords the scope passed through as it moved



# rp, dp = tickspace([-3400, 120], 10, [1, 1])

# print rp, dp
# rp, dp are the encoders returning tick values given an offset, time steps, and rate [arcsec/sec]
# Analyze the ticks returned and return telescope position over time
# First coordinate of rp, dp is the aligned position.
# sm, sb = linear(rp, dp)  # Confirm the random noise still gives linear results
# print 'Slope of ra/dec:', sm/2
# bg = [-10000, 10000]





# print ha, e.hours(ha+e.hours('-24:00:00')), e.degrees(ha)  # Practice with subtracting hours, degrees


# Determine offset
# Tick request returned [-3400, 120]
# Offset is then ha - zenith = tick - zero, dec - eq = tick - zero









# plt.plot(rp, dp, 'b.')
# plt.plot(bg, [x*sm + sb for x in bg], 'r:')
# plt.show()




# ra = [(-15, 687), (-30, 2222), (-45, 3770), (-30, 2213), (-15, 687), (0, 4294966468)]
# dec = [(90, 727), (100, 4294966001), (110, 4294963909), (120, 4294961877), (110, 4294963947), (100, 4294965986), (90, 732), (80, 2780), (70, 4815)]
#
# rx, ry = zip(*ra)
# rx, ry = list(rx), list(ry)
# for ii in range(len(ry)):
#     if ry[ii] > 2000000:
#         ry[ii] = ry[ii] - 4294967295
# dx, dy = zip(*dec)
# dx, dy = list(dx), list(dy)
# for ii in range(len(dy)):
#     if dy[ii] > 2000000:
#         dy[ii] = dy[ii] - 4294967295
#
# rm, rb = linear(rx, ry)
# dm, db = linear(dx, dy)
#
# # print rm, dm
#
# ra_tick = 1459
# ra_deg = (ra_tick-rb)/rm
# # print ra_deg
# ra_rad = e.degrees(str(ra_deg))
# # print ephem.hours(ra_rad), repr(ra_rad)

