import Tkinter as tk
import simple_ui
import ttk
import ola.RDMConstants as RDMConstants

class RDMNotebook:
  def __init__(self, root, controller, width=800, height=500, side=tk.TOP):
    """ Builds the ttk.Notebook """
    self.root = root
    self._controller = controller
    self.init_dx = width
    self.init_dy = height
    self.side = side
    self.objects = {}
    self.pid_location_dict = {}
    self._notebook = ttk.Notebook(self.root, name="nb", height=height,
                                  width=width)
    self._notebook.bind('<<NotebookTabChanged>>', self.tab_changed)
    self.populate_defaults()

  

  def populate_defaults(self):
    """ creates the default frames. """
    # create and populate the three default tabs
    self.info_tab = self.create_tab("info_tab", "Device Information")
    self._init_info()
    self.dmx_tab = self.create_tab("dmx_tab", "DMX512 Setup")
    self._init_dmx()
    self.sensor_tab = self.create_tab("sensor_tab", "Sensors")
    self._init_sensor()
    self.setting_tab = self.create_tab("setting_tab", "Power and Lamp Settings")
    self._init_setting()
    self.config_tab = self.create_tab("config_tab", "Configuration")
    self._init_config()
    self.pid_location_dict = {"PRODUCT_INFO": {"DEVICE_INFO": [0,1,2,3,4,5,6,7,
                                                              8,9], 
                                      "PRODUCT_DETAIL_ID_LIST": [10,11],
                                      "DEVICE_MODEL_DESCRIPTION": [3],
                                      "MANUFACTURER_LABEL": [12,13],
                                      "DEVICE_LABEL": [14,15],
                                      "FACTORY_DEFAULTS": [16,17],
                                      "SOFTWARE_VERSION_LABEL": [7],
                                      "BOOT_SOFTWARE_VERSION_ID": [18,19],
                                      "BOOT_SOFTWARE_VERSION_LABEL": [19]
                              },
                              "DMX512_SETUP": {"DEVICE_INFO": [0,1,2,3,4,5],
                                      "DMX_PERSONALITY": [4,5],
                                      "DMX_PERSONALITY_DESCRIPTION": [4,5,6,7,
                                                                      8,9],
                                      "DMX_START_ADDRESS": [3],
                                      "SLOT_INFO": [10,11,13],
                                      "SLOT_DESCRIPTION": [10,11,15,17,19],
                                      "DEFAULT_SLOT_VALUE": [20,22,23]
                              },
                              "SENSORS": {"SENSOR_DEFINITION": [0,1,3,5,7,9,11,
                                                                13,15],
                                      "SENSOR_VALUE": [16,17,19,21,23,25,27],
                                      "RECORD_SENSORS": []
                              },
                              "POWER_LAMP_SETTINGS": {"DEVICE_HOURS": [0,1],
                                      "LAMP_HOURS": [2,3],
                                      "LAMP_STRIKES": [4,5],
                                      "LAMP_STATE": [6,7],
                                      "LAMP_ON_MODE": [8,9],
                                      "DEVICE_POWER_CYCLES": [10,11],
                                      "POWER_STATE": [12,13]
                              },
                              "CONFIGURATION": {"LANGUAGE_CAPABILITIES": [0,1],
                                      "LANGUAGE": [0,1],
                                      "DISPLAY_INVERT": [2,3],
                                      "DISPLAY_LEVEL": [4,5],
                                      "PAN_INVERT": [6,7],
                                      "TILT_INVERT": [8,9],
                                      "PAN_TILT_SWAP": [10,11],
                                      "REAL_TIME_CLOCK": [12,13]
                              }}
    # self.factory_defaults_button.config(command = self.rdm_set(
    #                           "FACTORY_DEFAULTS", self.factory_defaults.get()))
    # self.start_address_entry.config(validatecommand = self.rdm_set(
    #                         "DMX_START_ADDRESS", self.dmx_start_address.get()))
    # self.dmx_personality_menu.config(command = self.rdm_set(
    #                             "DMX_PERSONALITY", self.dmx_personality.get()))
    # self.slot_menu.config(command = self.rdm_set(
    #                                         "SLOT_INFO",self.slot_number.get()))
    # self.sensor_def.config(command = self.rdm_get(
    #                             "SENSOR_DEFINITION", self.sensor_number.get()))
    # self.sensor_value.config(command = self.rdm_get(
    #                                   "SENSOR_VALUE", self.sensor_number.get()))
    # self.lamp_state_menu.config(command = self.rdm_set(
    #                                         "LAMP_STATE",self.lamp_state.get()))
    # self.lamp_on_mode_menu.config(command = self.rdm_set(
    #                                   "LAMP_ON_MODE", self.lamp_on_mode.get()))
    # self.device_power_cycles_menu.config(command = self.rdm_set(
    #                     "DEVICE_POWER_CYCLES", self.device_power_cycles.get()))
    # self.power_state_menu.config(command = self.rdm_set(
    #                                     "POWER_STATE", self.power_state.get()))
    # self.language_menu.config(command = self.rdm_set(
    #                                           "LANGUAGE", self.language.get()))
    # self.display_invert_menu.config(command = self.rdm_set(
    #                               "DISAPLAY_INVERT",self.display_invert.get()))
    # self.display_level_menu.config(command = self.rdm_set(
    #                                 "DISPLAY_LEVEL", self.display_level.get()))
    # self.pan_invert_button.config(command = self.rdm_set(
    #                                       "PAN_INVERT", self.pan_invert.get()))
    # self.tilt_invert_button.config(command = self.rdm_set(
    #                                     "TILT_INVERT", self.tilt_invert.get()))
    # self.pan_tilt_swap_button.config(command = self.rdm_set(
    #                                 "PAN_TILT_SWAP", self.pan_tilt_swap.get()))
    for key in self.pid_location_dict.keys():
        self._grid_info(self.objects[key])
    self._notebook.pack(side = self.side)

  def create_tab(self, tab_name, tab_label=None):
    """ Creates a tab. 

        will want to have all the options allowed by the ttk notebook widget to
        be args for this method

        Args:
          tab_name: string, cannot begin with a capital letter
          pid_list: list of strings, 
          tab_label: string that will be displayed on the tab, default set to 
            None, and tab_name will be on the tab

        Returns:
          tab: the Frame 
    """
    if tab_label is None:
        tab_label = tab_name
    tab = tk.Frame(self._notebook, name = tab_name)
    self._notebook.add(tab, text = tab_label)
    return tab

  def act_objects(self, supported_pids):
    """
    """
    # pass
    for key in self.objects.keys():
      for widget in self.objects[key]:
        widget.config(state = tk.DISABLED)
    for pid in supported_pids:
      if pid == "QUEUED_MESSAGE":
        pass
      elif pid in self.pid_location_dict["PRODUCT_INFO"].keys():
        for i in self.pid_location_dict["PRODUCT_INFO"][pid]:
          self.objects["PRODUCT_INFO"][i].config(state = tk.NORMAL)
      elif pid in self.pid_location_dict["DMX512_SETUP"].keys():
        for i in self.pid_location_dict["DMX512_SETUP"][pid]:
          self.objects["DMX512_SETUP"][i].config(state = tk.NORMAL)
      elif pid in self.pid_location_dict["SENSORS"].keys():
        for i in self.pid_location_dict["SENSORS"][pid]:
          self.objects["SENSORS"][i].config(state = tk.NORMAL)
      elif pid in self.pid_location_dict["POWER_LAMP_SETTINGS"].keys():
        for i in self.pid_location_dict["POWER_LAMP_SETTINGS"][pid]:
          self.objects["POWER_LAMP_SETTINGS"][i].config(state = tk.NORMAL)
      elif pid in self.pid_location_dict["CONFIGURATION"].keys():
        for i in self.pid_location_dict["CONFIGURATION"][pid]:
          self.objects["CONFIGURATION"][i].config(state = tk.NORMAL)

  def _init_info(self):
    """
    """
    # Text Variables:
    self.protocol_version = tk.StringVar(self.info_tab)
    self.device_model = tk.StringVar(self.info_tab)
    self.product_category = tk.StringVar(self.info_tab)
    self.software_version = tk.StringVar(self.info_tab)
    self.sub_device_count = tk.StringVar(self.info_tab)
    self.product_detail_ids = tk.StringVar(self.info_tab)
    self.manufacturer_label = tk.StringVar(self.info_tab)
    self.device_label = tk.StringVar(self.info_tab)
    self.boot_software = tk.StringVar(self.info_tab)

    # Widgets:
    self.factory_defaults = tk.BooleanVar(self.info_tab)
    self.factory_defaults_button = tk.Checkbutton(self.info_tab,
                                              variable = self.factory_defaults)
    
    self.device_label_button = tk.Button(self.info_tab, text = "Update Device Label", command = self.device_label_set)

    self.objects["PRODUCT_INFO"] = [tk.Label(self.info_tab,
                                                     text = "RDM Protocol Version"),
                            tk.Label(self.info_tab,
                                          textvariable = self.protocol_version),

                            tk.Label(self.info_tab, text = "Device Model"),
                            tk.Label(self.info_tab,
                                              textvariable = self.device_model),

                            tk.Label(self.info_tab, text = "Product Category:"),
                            tk.Label(self.info_tab,
                                          textvariable = self.product_category),

                            tk.Label(self.info_tab, text = "Software Version:"),
                            tk.Label(self.info_tab,
                                          textvariable = self.software_version),

                            tk.Label(self.info_tab, text = "Product Details:"),
                            tk.Label(self.info_tab, 
                                        textvariable = self.product_detail_ids),

                            tk.Label(self.info_tab, text = "Sub-Device Count"),
                            tk.Label(self.info_tab,
                                          textvariable = self.sub_device_count),

                            tk.Label(self.info_tab, text = "Manufacturer:"),
                            tk.Label(self.info_tab,
                                        textvariable = self.manufacturer_label),

                            tk.Label(self.info_tab, text = "Device Label:"),
                            tk.Entry(self.info_tab,
                                              textvariable = self.device_label),

                            tk.Label(self.info_tab, text = "Factory Defaults:"),
                            tk.Checkbutton(self.info_tab,
                                              variable = self.factory_defaults),

                            tk.Label(self.info_tab,
                                              text = "Boot Software Version:"),
                            tk.Label(self.info_tab,
                                              textvariable = self.boot_software),

                            self.device_label_button,
                            tk.Label(self.info_tab, text = "")
                            ]

  def _init_dmx(self):
    """
    """
    # Text Variables
    self.dmx_footprint = tk.StringVar(self.dmx_tab)
    self.dmx_start_address = tk.StringVar(self.dmx_tab)
    self.current_personality = tk.StringVar(self.dmx_tab)
    self.slot_required = tk.StringVar(self.dmx_tab)
    self.personality_name = tk.StringVar(self.dmx_tab)
    self.slot_number = tk.StringVar(self.dmx_tab)
    self.slot_name = tk.StringVar(self.dmx_tab)
    self.slot_offset = tk.StringVar(self.dmx_tab)
    self.slot_type = tk.StringVar(self.dmx_tab)
    self.slot_label_id = tk.StringVar(self.dmx_tab)
    self.default_slot_offset = tk.StringVar(self.dmx_tab)
    self.default_slot_value = tk.StringVar(self.dmx_tab)

    # Widgets
    self.start_address_entry = tk.Entry(self.dmx_tab,
                                          textvariable = self.dmx_start_address)
    self.dmx_personality_menu = tk.OptionMenu(self.dmx_tab, 
                                                self.current_personality.get(), "")
    self.slot_menu = tk.OptionMenu(self.dmx_tab, self.slot_number.get(), "")

    self.objects["DMX512_SETUP"] = [tk.Label(self.dmx_tab,
                                                      text = "DMX Footprint:"),
                                  tk.Label(self.dmx_tab,
                                            textvariable = self.dmx_footprint),

                                  tk.Label(self.dmx_tab,
                                                  text = "DMX Start Address:"),
                                  self.start_address_entry,

                                  tk.Label(self.dmx_tab,
                                                text = "Current Personality:"),
                                  self.dmx_personality_menu,

                                  tk.Label(self.dmx_tab, text = ""),
                                  tk.Label(self.dmx_tab,
                                            textvariable = self.slot_required),

                                  tk.Label(self.dmx_tab, text = ""),
                                  tk.Label(self.dmx_tab,
                                          textvariable = self.personality_name),

                                  tk.Label(self.dmx_tab, text = "Slot Info:"),
                                  self.slot_menu,

                                  tk.Label(self.dmx_tab, text = ""),
                                  tk.Label(self.dmx_tab,
                                                textvariable = self.slot_name),

                                  tk.Label(self.dmx_tab, text = ""),
                                  tk.Label(self.dmx_tab,
                                              textvariable = self.slot_offset),

                                  tk.Label(self.dmx_tab, text = ""),
                                  tk.Label(self.dmx_tab,
                                                textvariable = self.slot_type),

                                  tk.Label(self.dmx_tab, text = ""),
                                  tk.Label(self.dmx_tab,
                                            textvariable = self.slot_label_id),

                                  tk.Label(self.dmx_tab,
                                                      text = "Default Slot:"),
                                  tk.Label(self.dmx_tab,
                                    textvariable = self.default_slot_offset),

                                  tk.Label(self.dmx_tab, text = ""),
                                  tk.Label(self.dmx_tab,
                                        textvariable = self.default_slot_value)
                                  ]

  def _init_sensor(self):
    """
    """
    # Text Variable
    self.sensor_type = tk.StringVar(self.sensor_tab)
    self.sensor_unit = tk.StringVar(self.sensor_tab)
    self.sensor_prefix = tk.StringVar(self.sensor_tab)
    self.sensor_range = tk.StringVar(self.sensor_tab)
    self.normal_range = tk.StringVar(self.sensor_tab)
    self.supports_recording = tk.StringVar(self.sensor_tab)
    self.sensor_name = tk.StringVar(self.sensor_tab)
    self.sensor_number = tk.StringVar(self.sensor_tab)
    self.present_value = tk.StringVar(self.sensor_tab)
    self.lowest = tk.StringVar(self.sensor_tab)
    self.highest = tk.StringVar(self.sensor_tab)
    self.recorded = tk.StringVar(self.sensor_tab)

    # Widgets
    self.sensor_def = tk.OptionMenu(self.sensor_tab,
                                                  self.sensor_number.get(), "")
    self.sensor_value = tk.OptionMenu(self.sensor_tab,
                                                  self.sensor_number.get(), "")

    self.objects["SENSORS"] = [tk.Label(self.sensor_tab,
                                                        text = "Choose Sensor"),
                              self.sensor_def,

                              tk.Label(self.sensor_tab, text = ""),
                              tk.Label(self.sensor_tab,
                                              textvariable = self.sensor_type),

                              tk.Label(self.sensor_tab, text = ""),
                              tk.Label(self.sensor_tab,
                                              textvariable = self.sensor_unit),

                              tk.Label(self.sensor_tab, text = ""),
                              tk.Label(self.sensor_tab,
                                            textvariable = self.sensor_prefix),

                              tk.Label(self.sensor_tab, text = ""),
                              tk.Label(self.sensor_tab,
                                              textvariable = self.sensor_range),

                              tk.Label(self.sensor_tab, text = ""),
                              tk.Label(self.sensor_tab,
                                              textvariable = self.normal_range),

                              tk.Label(self.sensor_tab, text = ""),
                              tk.Label(self.sensor_tab,
                                        textvariable = self.supports_recording),

                              tk.Label(self.sensor_tab, text = ""),
                              tk.Label(self.sensor_tab,
                                              textvariable = self.sensor_name),

                              tk.Label(self.sensor_tab, text = ""),
                              self.sensor_value,

                              tk.Label(self.sensor_tab, text = ""),
                              tk.Label(self.sensor_tab,
                                            textvariable = self.sensor_number),

                              tk.Label(self.sensor_tab, text = ""),
                              tk.Label(self.sensor_tab,
                                            textvariable = self.present_value),

                              tk.Label(self.sensor_tab, text = ""),
                              tk.Label(self.sensor_tab,
                                                    textvariable = self.lowest),

                              tk.Label(self.sensor_tab, text = ""),
                              tk.Label(self.sensor_tab,
                                                  textvariable = self.highest),

                              tk.Label(self.sensor_tab, text = ""),
                              tk.Label(self.sensor_tab,
                                                  textvariable = self.recorded)
                              ]

  def _init_setting(self):
    """
    """
    self.device_hours = tk.StringVar(self.setting_tab)
    self.lamp_hours = tk.StringVar(self.setting_tab)
    self.lamp_strikes = tk.StringVar(self.setting_tab)
    self.lamp_state = tk.StringVar(self.setting_tab)
    self.lamp_on_mode = tk.StringVar(self.setting_tab)
    self.device_power_cycles = tk.StringVar(self.setting_tab)
    self.power_state = tk.StringVar(self.setting_tab)

    # Widgets
    self.lamp_state_menu = tk.OptionMenu(self.setting_tab,
                                                      self.lamp_state.get(), "")
    self.lamp_on_mode_menu = tk.OptionMenu(self.setting_tab,
                                                    self.lamp_on_mode.get(), "")
    self.power_state_menu = tk.OptionMenu(self.setting_tab,
                                                    self.power_state.get(), "")

    self.objects["POWER_LAMP_SETTINGS"] = [tk.Label(self.setting_tab,
                                                        text = "Device Hours:"),
                                          tk.Label(self.setting_tab,
                                              textvariable = self.device_hours),

                                          tk.Label(self.setting_tab,
                                                text = "Device Power Cycles:"),
                                          tk.Label(self.setting_tab, 
                                            textvariable = self.device_power_cycles),

                                          tk.Label(self.setting_tab,
                                                          text = "Lamp Hours:"),
                                          tk.Label(self.setting_tab,
                                                textvariable = self.lamp_hours),

                                          tk.Label(self.setting_tab,
                                                        text = "Lamp Strikes:"),
                                          tk.Label(self.setting_tab,
                                              textvariable = self.lamp_strikes),

                                          tk.Label(self.setting_tab,
                                                          text = "Lamp State:"),
                                          self.lamp_state_menu,

                                          tk.Label(self.setting_tab,
                                                        text = "Lamp On Mode:"),
                                          self.lamp_on_mode_menu,

                                          tk.Label(self.setting_tab,
                                                        text = "Power State:"),
                                          self.power_state_menu
                                          ]

  def _init_config(self):
    """
    """
    # Variables
    self.language = tk.StringVar(self.config_tab)
    self.display_invert = tk.StringVar(self.config_tab)
    self.display_level = tk.StringVar(self.config_tab)
    self.pan_invert = tk.BooleanVar(self.config_tab)
    self.tilt_invert = tk.BooleanVar(self.config_tab)
    self.pan_tilt_swap = tk.BooleanVar(self.config_tab)
    self.real_time_clock = tk.StringVar(self.config_tab)

    # Widgets
    self.language_menu = tk.OptionMenu(self.config_tab, self.language, "")
    self.display_invert_menu = tk.OptionMenu(self.config_tab,
                                                  self.display_invert.get(), "")
    self.display_level_menu = tk.OptionMenu(self.config_tab,
                                                  self.display_level.get(), "")
    self.pan_invert_button = tk.Checkbutton(self.config_tab,
                          variable = self.pan_invert, 
                          text = "(what it means for the\nbutton to be checked")
    self.tilt_invert_button = tk.Checkbutton(self.config_tab)
    self.pan_tilt_swap_button = tk.Checkbutton(self.config_tab)


    self.objects["CONFIGURATION"] = [tk.Label(self.config_tab,
                                                    text = "Device Language:"),
                                    self.language_menu,

                                    tk.Label(self.config_tab,
                                                      text = "Display Invert:"),
                                    self.display_invert_menu,

                                    tk.Label(self.config_tab, 
                                                      text = "Display Level:"),
                                    self.display_level_menu,

                                    tk.Label(self.config_tab,
                                                          text = "Pan Invert:"),
                                    self.pan_invert_button,

                                    tk.Label(self.config_tab,
                                                        text = "Tilt Invert:"),
                                    self.tilt_invert_button,

                                    tk.Label(self.config_tab,
                                                        text = "Pan Tilt Swap"),
                                    self.pan_tilt_swap_button,

                                    tk.Label(self.config_tab,
                                                      text = "Real Time Clock"),
                                    tk.Label(self.config_tab,
                                            textvariable = self.real_time_clock) 
                                   ]

  def _grid_info(self, obj_list):
    """
    """
    for i in range(len(obj_list)):
      if i%2 == 1:
        obj_list[i].config(width=35)
      else:
        obj_list[i].config(width=20)
    obj_list.reverse()
    for r in range((len(obj_list)+1)/2):
      for c in range(2):
        obj_list.pop().grid(row=r, column=c)

  def device_label_set(self):
    """
    """
    self._controller.SetDeviceLabel(self.device_label.get())

  def main(self):
    """ Main method for Notebook class. """
    self.root.mainloop()

  def tab_changed(self, event):
    # Note that this will be called when the program starts
    self.Update()

  def Update(self):
    index = self._notebook.index('current')
    print 'The selected tab changed to %d' % index
    if index == 0:
      self._controller.GetBasicInformation()
    elif index == 1:
      self._controller.GetDMXInformation()
    elif index == 2:
      self._controller.GetSensorsInformation()
    elif index == 3:
      self._controller.GetSettingInformation()
    elif index == 4:
      self._controller.GetConfigInformation()

  def RenderBasicInformation(self, param_dict):
    """
    """
    self.protocol_version.set("Version %d.%d" % (
                          param_dict["DEVICE_INFO"]["protocol_major"], 
                          param_dict["DEVICE_INFO"]["protocol_minor"]
                          ))
    self.device_model.set(param_dict["DEVICE_INFO"]["device_model"])
    self.device_model.set("%s (%d)" % (
                          param_dict.get("DEVICE_MODEL_DESCRIPTION", 'N/A'),
                          param_dict["DEVICE_INFO"]["device_model"]
                          ))
    index = param_dict["DEVICE_INFO"]["product_category"]
    self.product_category.set(RDMConstants.PRODUCT_CATEGORY_TO_NAME.get(index, "").replace("_"," "))
    sub_device_count = param_dict["DEVICE_INFO"]["sub_device_count"]
    # if "SOFTWARE_VERSION_LABEL" in param_dict:
    software_version = "%s (%d)" % (
                          param_dict["SOFTWARE_VERSION_LABEL"],
                          param_dict["DEVICE_INFO"]["software_version"]
                          )
    sub_device_count = param_dict["DEVICE_INFO"]["sub_device_count"]
    if "PRODUCT_DETAIL_ID_LIST" in param_dict:
      ids = param_dict["PRODUCT_DETAIL_ID_LIST"]
      names = ', '.join(RDMConstants.PRODUCT_DETAIL_IDS_TO_NAME[id] for id in ids).replace("_", " ")
      self.product_detail_ids.set(names)
    self.manufacturer_label.set(param_dict.get("MANUFACTURER_LABEL", "N/A"))
    self.device_label.set(param_dict.get("DEVICE_LABEL", "N/A"))
    self.factory_defaults.set(param_dict.get("FACTORY_DEFAULTS", "N/A"))
      # self.factory_defaults_button(Checkbutton)
    boot_software = 'N/A'
    boot_software_version = param_dict.get('BOOT_SOFTWARE_VERSION')
    boot_software_label = param_dict.get('BOOT_SOFTWARE_LABEL')
    if boot_software_version and boot_software_label:
      boot_software = '%s (%d)' % (boot_software_label, boot_software_version)
    elif boot_software_label:
      boot_software =  boot_software_label
    elif boot_software_version:
      boot_software =  boot_software_version

    self.boot_software.set(boot_software)                                                                                                                           
    return

  def RenderDMXInformation(self, param_dict):
    """
    """
    self.dmx_footprint.set(param_dict["DEVICE_INFO"]["dmx_footprint"])
    self.dmx_start_address.set(param_dict["DEVICE_INFO"]["dmx_start_address"])
    self.current_personality.set(param_dict["DEVICE_INFO"]["current_personality"])
    self.slot_required.set(param_dict.get("DMX_PERSONALITY_DESCRIPTION", {}).get("slots_required", "N/A"))
    self.personality_name.set(param_dict.get("DMX_PERSONALITY_DESCRIPTION", {}).get("name", "N/A"))
    self.slot_number.set(param_dict.get("SLOT_DESCRIPTION", {}).get("slot_number", "N/A"))
    self.slot_name.set(param_dict.get("SLOT_DESCRIPTION", {}).get("slot_name", "N/A"))
    self.slot_offset.set(param_dict.get("SLOT_INFO", {}).get("slot_offset", "N/A"))
    self.slot_type.set(param_dict.get("SLOT_INFO", {}).get("slot_type", "N/A"))
    self.slot_label_id.set(param_dict.get("SLOT_INFO", {}).get("slot_label_id", "N/A"))
    # I'm not sure how to deal with this pid...
    self.default_slot_offset.set("N/A")
    self.default_slot_value.set("N/A")
    print "DMX Rendered"

  def RenderSensorInformation(self, param_dict):
    self.sensor_type.set("Type: %s" % param_dict.get(
                                    "SENSOR_DEFINITION", {}).get("type", "N/A"))
    self.sensor_unit.set("Unit: %s" % param_dict.get(
                                    "SENSOR_DEFINITION", {}).get("unit", "N/A"))
    self.sensor_prefix.set("Prefix: %s" % param_dict.get(
                                  "SENSOR_DEFINITION", {}).get("prefix", "N/A"))
    self.sensor_range.set("Range: %s - %s" % (
              param_dict.get("SENSOR_DEFINITION", {}).get("range_min", "N/A"), 
              param_dict.get("SENSOR_DEFINITION", {}).get("range_max", "N/A")))
    self.normal_range.set("Normal Range: %s - %s" % (
              param_dict.get("SENSOR_DEFINITION", {}).get("normal_min", "N/A"), 
              param_dict.get("SENSOR_DEFINITION", {}).get("normal_max", "N/A")))
    self.supports_recording.set("Supports Recording: %s" % param_dict.get(
                      "SENSOR_DEFINITION", {}).get("supports_recording", "N/A"))
    self.sensor_name.set("Name: %s" % param_dict.get(
                                  "SENSOR_DEFINITION", {}).get("name", "N/A"))
    self.sensor_number.set("Sensor Number: %s" % param_dict.get(
                          "SENSOR_VALUE", {}).get("sensor_number", "N/A"))
    self.present_value.set("Present Value: %s" % param_dict.get(
                          "SENSOR_VALUE", {}).get("present_value", "N/A"))
    self.lowest.set("Lowest Value: %s" % param_dict.get(
                          "SENSOR_VALUE", {}).get("lowest", "N/A"))
    self.highest.set("Hightest Value: %s" % param_dict.get(
                          "SENSOR_VALUE", {}).get("highest", "N/A"))
    self.recorded.set("Recorded Value: %s" % param_dict.get(
                          "SENSOR_VALUE", {}).get("sensor_number", "N/A"))

  def RenderSettingInformation(self, param_dict):
    print "PARAM_DICT: %s" % param_dict
    self.device_hours.set(param_dict.get('DEVICE_HOURS', 'N/A'))
    self.lamp_hours.set(param_dict.get('LAMP_HOURS', 'N/A'))
    self.device_power_cycles.set(param_dict.get("DEVICE_POWER_CYCLES", "N/A"))
    self.lamp_strikes.set(param_dict.get('LAMP_STRIKES', 'N/A'))
    print "rendered"
    # if "LAMP_STATE" in param_dict:
    #   self.lamp_state = tk.StringVar(self.setting_tab)
    # if "LAMP_ON_MODE" in param_dict:
    #   self.lamp_on_mode = tk.StringVar(self.setting_tab)

    # if "POWER_STATE" in param_dict:
    #   self.power_state = tk.StringVar(self.setting_tab)

if __name__ == "__main__":
  ui = simple_ui.DisplayApp()

  master = tk.Frame(root, name="master", width = 200, heigh = 200)
  master.pack(fill=tk.BOTH) # fill both sides of the parent

  root.title("EZ") # title for top-level window

  nb = RDMNotebook(master, ui)
  nb.main()
