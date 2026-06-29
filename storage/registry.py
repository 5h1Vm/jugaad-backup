from .local import LocalStorage
from .usb import USBStorage

PROVIDERS = [

    LocalStorage,

    USBStorage,

]