from abc import ABC, abstractmethod
from typing import Literal, Any, Optional


class AbcManageDB(ABC):
    #   USER MANAGEMENT

    @abstractmethod
    def create_user(self, nickname: str, redirect_ely: int = 1, need_exist: bool = True) -> Any:
        """
        Creates a user record. If need_exist=True, checks if user already exists.
        """

    @abstractmethod
    def record_exists(self, table_name: str, column_name: str, value: Any) -> bool:
        """
        Checks if specific value exists in the given table/column.
        """

    @abstractmethod
    def nickname_exists_ely(self, nickname: Optional[str] = None,
                            redirect_nickname: Optional[str] = None) -> Any:
        """
        Checks if nickname or redirect nickname exists in ely.
        """

    @abstractmethod
    def set_redirected_nickname_ely(self, nickname: str, redirect_nickname: Optional[str]) -> bool:
        """
        Sets redirect nickname for Ely.
        """

    @abstractmethod
    def toggle_redirect(self, nickname: str, toggle: Literal[0, 1]) -> bool:
        """
        Enables or disables Ely redirect.
        """

    @abstractmethod
    def redirect_state(self, nickname: str) -> int:
        """
        Returns redirect state (0 or 1).
        """

    @abstractmethod
    def set_skin_id(self, nickname: str, skin_id: str) -> bool:
        """
        Sets skin ID for a user.
        """

    #   SKIN MANAGEMENT

    @abstractmethod
    def get_sign_skin(self, nickname: str, skin_image: bytes) -> Any:
        """
        Loads or generates signed texture data.
        """

    #   REMOVE / VIEW / QUERY

    @abstractmethod
    def remove_row(
        self,
        table_name: Literal["user_data", "skin_data"],
        skin_id: Optional[str] = None,
        user_id: Optional[str] = None,
        nickname: Optional[str] = None,
    ) -> bool:
        """
        Removes record based on provided fields.
        """

    @abstractmethod
    def view_on_db(
        self,
        table_name: Literal["user_data", "skin_data"],
        nickname: Optional[str] = None,
        user_id: Optional[str] = None,
        skin_id: Optional[str] = None
    ) -> list[dict]:
        """
        Returns database rows in list[dict].
        """

    #   REDIRECT LOGIC

    @abstractmethod
    def what_redirect_of(
        self,
        nickname: str,
        return_system: Literal["skin_system", "ely"] | str = "auto"
    ) -> dict:
        """
        Returns dictionary describing which system handles the nickname.
        """

    #   EXTERNAL / PROXY

    @abstractmethod
    def proxy_from_ely(self, **kwargs) -> dict:
        """
        Fetches skin data via Ely proxy.
        """

    @abstractmethod
    def return_texture_data_for_system(self, **kwargs) -> dict:
        """
        Returns full texture data formatted for skin system.
        """
