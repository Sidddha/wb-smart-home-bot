from .callback_datas import main_callback


class Button():
    def __init__(self):
        self.text = ""
        self.callback_data = ""
       
 
        self.get_widgets = {
            "text": "Виджеты",
            "callback_data": main_callback.new(command="get_widgets")
        }
        self.system= {
            "text": "Сведения о системе (not implemented)", 
            "callback_data": main_callback.new(command="system")
        }
        self.devices= {
            "text": "Устройства (not implemented)", 
            "callback_data": main_callback.new(command="devices")           
        }
        self.settings= {
            "text": "Настройки (not implemented)", 
            "callback_data": main_callback.new(command="settings")           
        }   
 
