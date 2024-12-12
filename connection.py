class Connection:
    """
    儲存登入後連線所需的 php session id
    """
    def __init__(
            self,
            php_session_id : str,
    ):
        self._php_session_id = php_session_id

    @property
    def php_session_id(self):
        return self._php_session_id