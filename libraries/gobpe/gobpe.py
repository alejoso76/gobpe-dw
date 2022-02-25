from libraries.common import act_on_element, check_file_download_complete, log_message, start_finish_logs, log_message, file_system, files, pdf
from config import OUTPUT_FOLDER
from selenium.webdriver.common.keys import Keys
from datetime import datetime
import time

class GobPe:
    def __init__(self, rpa_selenium_instance) -> None:
        """Inits the class

        Args:
            rpa_selenium_instance (browser): Selenium browser
        """
        # Minimum 2 variables
        self.browser = rpa_selenium_instance
        self.gobpe_url = 'https://www.gob.pe/'
        self.category = ''
        self.files_to_download_dict_list = ''

    @start_finish_logs('Access gob.pe')
    def access_gobpe(self):
        """Access gob.pe from the browser
        """
        self.browser.go_to(self.gobpe_url)

    @start_finish_logs('Go to Estado Peruano')
    def go_to_estado_peruano(self):
        """Clicks on El Estado Peruano link
        """
        act_on_element('//a[@class="footer__link footer__link--visible text-white hover:text-white" and span[text()="El Estado Peruano"]]', 'click_element')
        # self.browser.go_to(self.gobpe_url + 'estado/')
    
    @start_finish_logs('Go to Organismos Autónomos')
    def go_to_organismos_autonomos(self):
        """Clicks on Organismos Autónomos link
        """
        act_on_element('//div[@class="power-card__title" and text()="Organismos Autónomos"]', 'click_element')
        # self.browser.go_to(self.gobpe_url + 'estado/organismos-autonomos')

    @start_finish_logs('Go to ONPE')
    def go_to_onpe(self):
        """Clicks on ONPE link
        """
        act_on_element('//a[@class="track-ga-click track-ga-click" and text()="Oficina Nacional de Procesos Electorales (ONPE)"]', 'click_element')
        # self.browser.go_to(self.gobpe_url + 'onpe')

    @start_finish_logs('Get Category from txt')
    def get_category(self):
        """Gets the category from the .txt file
        """
        file_content = file_system.read_file(
            'files/Category.txt', encoding='utf-8')
        self.category = file_content.strip()
        log_message(F'  Category is: {self.category}')

    @start_finish_logs('Click category')
    def click_category(self):
        """Clicks the category that was obtained from the. txt
        """
        act_on_element(F'//li[@class="navigator__item" and a[text()="{self.category}"]]', 'click_element')

    @start_finish_logs('Go to informes y publicaciones')
    def click_informes_publicaciones(self):
        """Clicks on Buscar informes y publicaciones link
        """
        act_on_element(F'//a[@class="btn--corona track-ga-click w-full sm:w-fit m-auto" and text()="Buscar informes y publicaciones"]', 'click_element')

    @start_finish_logs('Filter by date')
    def filter_date(self):
        """Goes to the URL that filters the search from 28-10-2021 up until today date
        """
        today = datetime.today().strftime('%d-%m-%Y')
        self.browser.go_to(self.gobpe_url + F'busquedas?contenido[]=publicaciones&desde=28-10-2021&hasta={today}&institucion[]=onpe&sheet=1&sort_by=recent')

    @start_finish_logs('Get files to download')
    def get_files_to_download(self):
        """Obtains the files to download dict from the Excel
        """
        files.open_workbook('files/Files_To_Download.xlsx')
        # This is the data from the excel
        self.files_to_download_dict_list = files.read_worksheet(name='Sheet1', header=True)
        files.close_workbook()

    @start_finish_logs('Download files')
    def download_files(self):
        """Downloads the files that match a certain condition (Download Required=Yes)
        """
        for file_to_download in self.files_to_download_dict_list:
            if file_to_download['Download Required'] == 'Yes':
                act_on_element(F'//article[@class="bg-blue-300 mt-4 p-8" and div/div[@class="col-md-9"]\
                    /div[@class="mb-2"]/h3/a[text()="{file_to_download["Name"]}"]]\
                    /div/a[@class="bg-transparent border-2 border-blue-700 font-bold py-2 px-3 text-blue-700 flex"]', 'click_element')
                check_file_download_complete('pdf')

    @start_finish_logs('Create Pages Excel and Txt')
    def create_pages_excel_and_txt(self):
        """Creates the Excel with the extracted data and creates a .txt if the # of pages > 50
        """
        pages_dict_list = []
        result_txt = ''
        files_downloaded = file_system.find_files(
            F'{OUTPUT_FOLDER}/*.pdf')

        for file_downloaded in files_downloaded:
            pdf_name = file_downloaded.name
            num_pages = len(pdf.get_text_from_pdf(file_downloaded))
            pdf_dict = {
                'File Name': pdf_name,
                'Amount of Pages': num_pages
            }
            pages_dict_list.append(pdf_dict)

            if num_pages > 50:
                result_txt = result_txt + pdf_name + '\n' + 30*'-'

        # Txt
        file_system.create_file(F'{OUTPUT_FOLDER}/Result.txt',
                                content=result_txt, encoding='utf-8', overwrite=True)

        # Excel
        files.create_workbook(path=F'{OUTPUT_FOLDER}/Results.xlsx')
        files.append_rows_to_worksheet(
            pages_dict_list,
            name='Sheet',
            header=True,
            start=None
        )
        files.save_workbook(path=None)
        files.close_workbook()