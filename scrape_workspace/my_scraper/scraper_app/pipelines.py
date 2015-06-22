from sqlalchemy.orm import sessionmaker
from models import Deals, db_connect, create_deals_table


class LivingSocialPipeline(object):
    """
    Livingsocial pipeline for storing scraped items in the database"""
    def __init__(self):
        """
        Initializes database connection and sessionmaker.
        Creates deals table.
        """
        engine = db_connect()
        create_deals_table(engine)
        self.Session = sessionmaker(bind=engine)

    def process_item(self, item, spider):
        """
        Save deals in the database.
        This method is called for every item pipeline component.
        """
        session = self.Session()
        deal = Deals(**item)

        try:
            session.add(deal)  # add deal to current session
            session.commit()  # commit the session to the DB
        except:
            session.rollback()  # undo changes if anything went wrong
            raise
        finally:
            session.close()

        return item
