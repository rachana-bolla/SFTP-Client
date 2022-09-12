from ast import Try
import unittest
import SftpClient
import pysftp
from unittest.mock import patch, Mock, ANY
from SftpClient import ask

class TestAgileProject(unittest.TestCase):

    @patch('builtins.input', side_effect=['TestServerName', 'TestUser', 'help', 'seeya', 'y'])
    @patch('getpass.getpass')
    @patch.object(
        target=pysftp,
        attribute='Connection',
        autospec=True,
        return_value=Mock(
            spec=pysftp.Connection,
            __enter__=lambda self: self,
            __exit__=lambda *args: None
        )
    )
    def test_ask_help(self, mock_input, getpw, conn):
        print("Inside help")
        getpw.return_value = 'Testpwd'
        conn.close.return_value = None
        ask()

    def test_add(self):
        print("Inside add")
        self.assertAlmostEqual(SftpClient.add('7','7','7'), 777)

    def test_displayOption(self):
        print("Inside test_displayOption")
        options = ["Type help to print options"]
        for option in options:
            self.assertAlmostEqual(option, "Type help to print options")


    @patch('builtins.input', side_effect=['TestServerName', 'TestUser', 'help', 'seeya', 'y'])
    @patch('getpass.getpass')
    @patch.object(
        target=pysftp,
        attribute='Connection',
        autospec=True,
        return_value=Mock(
            spec=pysftp.Connection,
            __enter__=lambda self: self,
            __exit__=lambda *args: None
        )
    )
    def test_connection_1(self, mock_input, getpw, conn):
        print("Inside test_connection_1")
        getpw.return_value = 'Testpwd'        
        conn.return_value.isdir.return_value = True
        conn.return_value.cwd.return_value = None
        conn.close.return_value = None
        ask()

    @patch('builtins.input', side_effect=['TestServerName', 'TestUser', 'help', 'seeya', 'y'])
    @patch('getpass.getpass')
    @patch.object(
        target=pysftp,
        attribute='Connection',
        autospec=True,
        return_value=Mock(
            spec=pysftp.Connection,
            __enter__=lambda self: self,
            __exit__=lambda *args: None
        )
    )
    def test_savecon(self, mock_input, getpw, conn):
        print("Inside test_savecon")
        getpw.return_value = 'Testpwd'        
        conn.return_value.isdir.return_value = True
        conn.return_value.cwd.return_value = None
        conn.close.return_value = None
        ask()

    @patch('builtins.input', side_effect=['TestServerName', 'TestUser', 'help', 'seeya', 'y'])
    @patch('getpass.getpass')
    @patch.object(
        target=pysftp,
        attribute='Connection',
        autospec=True,
        return_value=Mock(
            spec=pysftp.Connection,
            __enter__=lambda self: self,
            __exit__=lambda *args: None
        )
    )
    def test_usesavecon(self, mock_input, getpw, conn):
        print("Inside test_usesavecon")
        getpw.return_value = 'Testpwd'        
        conn.return_value.isdir.return_value = True
        conn.return_value.cwd.return_value = None
        conn.close.return_value = None
        ask()
 
    @patch('builtins.input', side_effect=['TestServerName', 'TestUser', 'cd', 'cd', 'testDir', 'putfile','listloc', 'seeya', 'y'])
    @patch('getpass.getpass')
    @patch.object(
        target=pysftp,
        attribute='Connection',
        autospec=True,
        return_value=Mock(
            spec=pysftp.Connection,
            __enter__=lambda self: self,
            __exit__=lambda *args: None
        )
    )
    def test_putfile(self, mock_input, getpw, conn):
        print("Inside test_putfile")
        getpw.return_value = 'Testpwd'        
        conn.return_value.isdir.return_value = True
        conn.return_value.cwd.return_value = None
        conn.close.return_value = None
        ask()

    @patch('builtins.input', side_effect=['TestServerName', 'TestUser', 'cd', 'cd', 'testDir', 'listloc', 'seeya', 'y'])
    @patch('getpass.getpass')
    @patch.object(
        target=pysftp,
        attribute='Connection',
        autospec=True,
        return_value=Mock(
            spec=pysftp.Connection,
            __enter__=lambda self: self,
            __exit__=lambda *args: None
        )
    )
    def test_ask_listloc(self, mock_input, getpw, conn):
        print("Inside test_ask_listloc")
        getpw.return_value = 'Testpwd'        
        conn.return_value.isdir.return_value = True
        conn.return_value.cwd.return_value = None
        conn.close.return_value = None
        ask()

    @patch('builtins.input', side_effect=['TestServerName', 'TestUser', 'cd', 'cd', 'testDir', 'listloc', 'rename', 'seeya', 'y'])
    @patch('getpass.getpass')
    @patch.object(
        target=pysftp,
        attribute='Connection',
        autospec=True,
        return_value=Mock(
            spec=pysftp.Connection,
            __enter__=lambda self: self,
            __exit__=lambda *args: None
        )
    )
    def test_ask_rename(self, mock_input, getpw, conn):
        print("Inside test_ask_rename")
        getpw.return_value = 'Testpwd'        
        conn.return_value.isdir.return_value = True
        conn.return_value.cwd.return_value = None
        conn.close.return_value = None
        ask()

    @patch('builtins.input', side_effect=['TestServerName', 'TestUser', 'cd', 'cd', 'testDir', 'listloc', 'createdir', 'testDir','seeya', 'y'])
    @patch('getpass.getpass')
    @patch.object(
        target=pysftp,
        attribute='Connection',
        autospec=True,
        return_value=Mock(
            spec=pysftp.Connection,
            __enter__=lambda self: self,
            __exit__=lambda *args: None
        )
    )
    def test_ask_createdir(self, mock_input, getpw, conn):
        print("Inside test_ask_createdir")
        getpw.return_value = 'Testpwd'        
        conn.return_value.isdir.return_value = True
        conn.return_value.cwd.return_value = None
        conn.close.return_value = None
        ask()
    
    @patch('builtins.input', side_effect=['TestServerName', 'TestUser', 'cd', 'cd', 'testDir', 'listloc', 'createdir', 'testDir','seeya', 'y'])
    @patch('getpass.getpass')
    @patch.object(
        target=pysftp,
        attribute='Connection',
        autospec=True,
        return_value=Mock(
            spec=pysftp.Connection,
            __enter__=lambda self: self,
            __exit__=lambda *args: None
        )
    )
    def test_ask_createdir(self, mock_input, getpw, conn):
        print("Inside test_ask_createdir")
        getpw.return_value = 'Testpwd'        
        conn.return_value.isdir.return_value = True
        conn.return_value.cwd.return_value = None
        conn.close.return_value = None
        ask()

    @patch('builtins.input', side_effect=['TestServerName', 'TestUser', 'cd', 'cd', 'testDir', 'putfiles','listloc', 'seeya', 'y'])
    @patch('getpass.getpass')
    @patch.object(
        target=pysftp,
        attribute='Connection',
        autospec=True,
        return_value=Mock(
            spec=pysftp.Connection,
            __enter__=lambda self: self,
            __exit__=lambda *args: None
        )
    )
    def test_putfiles(self, mock_input, getpw, conn):
        print("Inside test_putfiles")
        getpw.return_value = 'Testpwd'        
        conn.return_value.isdir.return_value = True
        conn.return_value.cwd.return_value = None
        conn.close.return_value = None
        ask()

    @patch('builtins.input', side_effect=['TestServerName', 'TestUser', 'cd', 'cd', 'testDir', 'listloc', 'seeya', 'y'])
    @patch('getpass.getpass')
    @patch.object(
        target=pysftp,
        attribute='Connection',
        autospec=True,
        return_value=Mock(
            spec=pysftp.Connection,
            __enter__=lambda self: self,
            __exit__=lambda *args: None
        )
    )
    def test_listloc(self, mock_input, getpw, conn):
        print("Inside test_listloc")
        getpw.return_value = 'Testpwd'        
        conn.return_value.isdir.return_value = True
        conn.return_value.cwd.return_value = None
        conn.close.return_value = None
        ask()