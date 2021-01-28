from configparser import ConfigParser
cfg = ConfigParser()
cfg.read('/etc/ssh/sshd_config')
print(cfg.sections())
