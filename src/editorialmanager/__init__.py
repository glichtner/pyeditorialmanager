from typing import Dict
import requests
import re
from bs4 import BeautifulSoup
import html5lib  # used by beautifulsoup, but imported here to raise error if not installed
import pandas as pd

from editorialmanager.version import version as __version__


class Journal:
    """
    Python interface for querying the editorialmanager journal submission system.
    """

    """
    Strings used to identify if the login was successful or failed
    """
    TEXT_LOGIN_SUCCESS = "parent.location.href = 'Default.aspx?pg=AuthorMainMenu.aspx'"
    TEXT_LOGIN_FAILED = "top.location.href = 'Default.aspx?pg=login.asp%3floginError"

    """
    Editorial manager base URL
    """
    BASE_URL = "https://www.editorialmanager.com/"

    def __init__(self, name: str, username: str, password: str) -> None:
        """

        :param name: Name of the journal, derived directly from the editorial manager URL
        :param username: Username for journal login
        :param password: Password for journal login
        """
        self._journal = name.lower()
        self._base_url = self._build_url()
        self._session = requests.Session()
        self.login(username, password)

    def _build_url(self):
        """
        Return the base URL of the journal
        """
        return self.BASE_URL + self._journal.lower() + "/"

    def _get_url(self, name: str, params: Dict = None) -> requests.models.Response:
        """
        Send a GET request to the journal.

        :param name: Script basename (usually ends with .asp or .aspx)
        :param params: query string parameters
        :return: Response object
        """
        return self._session.get(self._base_url + name, params=params)

    def login(self, username: str, password: str) -> bool:
        """
        Login to journal using supplied credentials.

        :param username: Username for journal login
        :param password: Password for journal login
        :return: True if login was sucessful, False otherwise
        """
        auth = {"username": username, "password": password}

        r = self._session.post(self._base_url + "LoginAction.ashx", data=auth)

        if self.TEXT_LOGIN_SUCCESS in r.text:
            return True
        elif self.TEXT_LOGIN_FAILED in r.text:
            raise Exception("Login failed")
        else:
            raise Exception(
                "Couldn't find login success nor failure information in response"
            )

        return False

    @staticmethod
    def _convert_date_columns(df: pd.DataFrame) -> None:
        """
        Converts the "date" columns in the dataframe to pandas date format (in place).

        :param df: DataFrame
        :return: None
        """
        for c in df.columns:
            if "date" not in c.lower():
                continue
            df[c] = pd.to_datetime(df[c])

    def _read_tabular_page(self, name: str, page: int = 1) -> pd.DataFrame:
        """
        Reads a page from editorialmanager with the content in tabular format (e.g. pending submissions table)

        :param name: Script basename (usually ends with .asp or .aspx)
        :param page: Page number to read
        :return: Table from website as pandas DataFrame
        """
        r = self._get_url(name, params={"currentPage": page})
        soup = BeautifulSoup(r.text, "html5lib")

        table = soup.find("table", id="datatable", class_="datatable")

        columns = table.find_all("th")
        columns = [c.text.strip() for c in columns]

        rows = []
        for row in table.find("tbody").find_all("tr"):
            cells = row.find_all("td")
            cells = [c.text.strip() for c in cells]
            rows.append(cells)

        df = pd.DataFrame(rows, columns=columns)
        df = df.drop("Action", axis=1)

        self._convert_date_columns(df)

        return df

    def overview(self) -> pd.DataFrame:
        """
        Get the overview of submissions per type/category from the main menu

        :return: Overview table
        """
        r = self._get_url("AuthorMainMenu.aspx")

        soup = BeautifulSoup(r.text, "html.parser")

        items = soup.find_all("fieldset", id="tableContainer")

        assert len(items) == 3, "Expected three fieldsets on author main menu"

        entries = []
        for item in items:
            matches = re.findall(r">([^<]+)</[^>]+>\xa0+\((\d+)\)", item.decode())
            for match in matches:
                entries.append(
                    {
                        "name": match[0].strip(),
                        "count": int(match[1]),
                        "type": item.find("legend").text,
                    }
                )

        return pd.DataFrame(entries)

    def pending_submissions(self) -> pd.DataFrame:
        """
        Get information about currently pending submissions.

        :return: Pending submissions information (status etc.)
        """
        return self._read_tabular_page("auth_pendSubmissions.asp")

    def completed_submissions(self) -> pd.DataFrame:
        """
        Get information about completed submissions.

        :return: Completed submissions information (status etc.)
        """
        return self._read_tabular_page("auth_compSubmissions.asp")
