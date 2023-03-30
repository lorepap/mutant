from enum import Enum

class Trace(Enum):

    att_lte_driving = 'att.lte.driving'
    att_lte_driving_2016 = 'att.lte.driving.2016'
    tm_lte_driving = 'tm.lte.driving'
    tm_lte_short = 'tm.lte.short'
    tm_umts_driving = 'tm.umts.driving'
    vz_evdo_driving = 'vz.evdo.driving'
    vz_lte_driving = 'vz.lte.driving'
    vz_lte_short = 'vz.lte.short'
    bus = 'bus'
    timessquare = 'timessquare'
    wired = 'wired'
    none = 'none'
