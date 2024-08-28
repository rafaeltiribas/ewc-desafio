from .games import r6, sf6, cs, rocket, fc24

def get_ewc_furia_matches():
    r6.get_r6_matches()
    sf6.get_sf6_matches()
    cs.get_cs_matches()
    rocket.get_rocket_matches()
    fc24.get_fc_matches()