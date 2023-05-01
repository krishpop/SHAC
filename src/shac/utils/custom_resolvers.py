from omegaconf import OmegaConf

OmegaConf.register_new_resolver("resolve_default", lambda default, arg: default if arg in ["", None] else arg)

OmegaConf.register_new_resolver("eval", eval)
