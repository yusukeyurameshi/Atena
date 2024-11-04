import configparser


def writeConfigFile(iniFile, values):
    config = configparser.ConfigParser()
    config['DEFAULT'] = values
    with open(iniFile, 'w') as configfile:
        config.write(configfile)




def readConfigFile(iniFile):
    config = configparser.ConfigParser()
    config.sections()
    config.read(iniFile)
    #values = config['DEFAULT']
    #print(config.sections())
    # for key in values.items():
    #     print(key)
    return config['DEFAULT'].items()

