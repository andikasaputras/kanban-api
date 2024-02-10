import logging
from logging.handlers import RotatingFileHandler
import os


def init_logging(app):
    if not os.getenv('ENV') == 'test':
        # Ensure log folder exists
        log_folder = os.path.join(os.path.dirname(app.root_path), 'logs')
        os.makedirs(log_folder, exist_ok=True)

        # Set up rotating file handler
        log_file = os.path.join(log_folder, 'app.log')
        # 10KB per file, 10 files max
        file_handler = RotatingFileHandler(
            log_file, maxBytes=10240, backupCount=10)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s '
            '[in %(pathname)s:%(lineno)d]'))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)

        # Set up console handler
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(logging.INFO)
        app.logger.addHandler(stream_handler)

        app.logger.setLevel(logging.INFO)
        app.logger.info('Application startup')
