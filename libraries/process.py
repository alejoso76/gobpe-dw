from libraries.common import log_message, capture_page_screenshot, browser
from config import OUTPUT_FOLDER, tabs_dict
from libraries.gobpe.gobpe import GobPe

class Process:
    def __init__(self):
        log_message("Initialization")
        prefs = {
            "profile.default_content_setting_values.notifications": 2,
            "profile.default_content_settings.popups": 0,
            "directory_upgrade": True,
            "download.default_directory": OUTPUT_FOLDER,
            "plugins.always_open_pdf_externally": True,
            "download.prompt_for_download": False
        }
        
        browser.open_available_browser(
            preferences=prefs)
        browser.set_window_size(1920, 1080)
        browser.maximize_browser_window()

        gobpe = GobPe(browser)
        tabs_dict['GobPe'] = len(tabs_dict)
        gobpe.access_gobpe()
        self.gobpe = gobpe


    def start(self):
        self.gobpe.go_to_estado_peruano()
        self.gobpe.go_to_organismos_autonomos()
        self.gobpe.go_to_onpe()
        self.gobpe.get_category()
        self.gobpe.click_category()
        self.gobpe.click_informes_publicaciones()
        self.gobpe.filter_date()
        self.gobpe.get_files_to_download()
        self.gobpe.download_files()
        self.gobpe.create_pages_excel_and_txt()


    def finish(self):
        log_message("DW Process Finished")
        # Good practice: close browser manually
        browser.close_browser()
