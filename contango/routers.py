class DataRouter:
    """Router to handle requests to data tables in contango_data.db

    Two primary tables of interest used for front end consumption:
    1. fct_futures_daily
    2. fct_etf_daily
    """
    route_app_labels = {'contango_data',}

    def db_for_read(self, model, **hints):
        """Sends read requests for contango_data models to contango_data.db"""
        if model._meta.app_label in self.route_app_labels:
            return 'contango_data_db'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        """Allow relationships involving models from contango_data"""
        if (
            obj1._meta.app_label in self.route_app_labels or
            obj2._meta.app_label in self.route_app_labels
        ):
           return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Make sure the auth and contenttypes apps only appear in the
        'auth_db' database.
        """
        if app_label in self.route_app_labels:
            return db == 'contango_data_db'
        return None
