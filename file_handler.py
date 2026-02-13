import os

class FileHandler:
    encoding = 'utf-8'  # Public class variable (can be modified directly)
    
    @staticmethod
    def is_file_valid(file_path):
        """Check whether the given file path exists and is a file."""
        return os.path.isfile(file_path)
    
    @staticmethod
    def read_file(file_path, encoding=None):
        """
        Read file content using the specified encoding
        (or the default class encoding).
        """
        used_encoding = encoding if encoding is not None else FileHandler.encoding
        with open(file_path, 'r', encoding=used_encoding) as f:
            return f.read()
    
    @staticmethod
    def write_file(file_path, content, prefix='', encoding=None):
        """
        Write content to a file with an optional filename prefix.

        :param file_path: Path to the target file.
        :param content: Content to write (string).
        :param prefix: Optional prefix added to the filename.
        :param encoding: File encoding (defaults to class encoding).
        :return: Final saved file path.
        """
        used_encoding = encoding if encoding is not None else FileHandler.encoding
        
        if prefix:
            dirname = os.path.dirname(file_path)
            basename = prefix + os.path.basename(file_path)
            file_path = os.path.join(dirname, basename)
        
        with open(file_path, 'w', encoding=used_encoding) as f:
            f.write(content)
        
        return file_path
