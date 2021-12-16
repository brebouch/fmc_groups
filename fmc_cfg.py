import fmc_api

cfg = {
    'server': "https://192.168.99.24",
    'username': "apiuser",
    'password': "Cisco123"
}

fmc = fmc_api.FMC(cfg['server'], cfg['username'], cfg['password'])
fmc.authentication()
