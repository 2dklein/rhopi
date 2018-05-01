import ephem as ep
import numpy as np


def get_ra(zero, tick):
    tick_to_degree = 103.
    count = tick - zero
    deg = (count/tick_to_degree)*np.pi/180
    ra = ep.degrees(deg)
    return ra


def get_dec(zero, tick):
    tick_to_degree = 206.
    count = tick - zero
    deg = (count/tick_to_degree)*np.pi/180
    dec = ep.degrees(deg)
    return dec


def align_polaris(ra_ticks, dec_ticks):
    rho = ep.Observer()
    rho.lon, rho.lat = '-82.586203', '29.400249'
    pol = ep.star('Polaris')
    altair = ep.star('Altair')
    altair.compute(rho)
    pol.compute(rho)
    # print "Polaris:", pol.ra, pol.dec
    # print altair.name, altair.ra, altair.dec
    # print "Rho Sidereal Time:", rho.sidereal_time()
    zero = pol.ra
    # ra_offset, dec_offset = pull_ra(), pull_dec()

    # print "Post-align RA:", get_ra(4000, 3066)

    # return zero_ra, zero_dec



align_polaris(27265, 239864)
