import logging
from core.logic import AppLogic
from ui.window import MainWindow
from config import Config


def configure_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('school_app.log'),
            logging.StreamHandler()
        ]
    )


def main():
    configure_logging()

    if not Config.MISTRAL_API_KEY:
        logging.error("Mistral API key not found in .env file")
        return

    try:
        logic = AppLogic(initial_grade=6)
        if not logic.questions:
            logging.error("Failed to load initial questions")
            return

        app = MainWindow(logic)
        app.run()
    except Exception as e:
        logging.critical(f"Application failed: {str(e)}")


if __name__ == "__main__":
    main()