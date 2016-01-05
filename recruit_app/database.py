"""Database module, including the SQLAlchemy database object and DB-related
utilities.
"""
from sqlalchemy.orm import relationship
import datetime

from .extensions import db
from .compat import basestring

# Alias common SQLAlchemy names
Column = db.Column

class CRUDMixin(object):
    """Mixin that adds convenience methods for CRUD (create, read, update, delete)
    operations.
    """

    @classmethod
    def create(cls, **kwargs):
        """Create a new record and save it the database."""
        instance = cls(**kwargs)
        return instance.save()

    def update(self, commit=True, **kwargs):
        """Update specific fields of a record."""
        for attr, value in kwargs.iteritems():
            setattr(self, attr, value)
        return commit and self.save() or self

    def save(self, commit=True):
        """Save the record."""
        db.session.add(self)
        if commit:
            try:
                db.session.commit()
            except:
                db.session.rollback()
                raise
        return self

    def delete(self, commit=True):
        """Remove the record from the database."""
        db.session.delete(self)
        if commit:
            try:
                return db.session.commit()
            except:
                db.session.rollback()
                raise
                
        return False


class Model(CRUDMixin, db.Model):
    """Base model class that includes CRUD convenience methods."""
    __abstract__ = True


# From Mike Bayer's "Building the app" talk
# https://speakerdeck.com/zzzeek/building-the-app
class SurrogatePK(object):
    """A mixin that adds a surrogate integer 'primary key' column named
    ``id`` to any declarative-mapped class.
    """
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)

    @classmethod
    def get_by_id(cls, id):
        if any(
            (isinstance(id, basestring) and id.isdigit(),
             isinstance(id, (int, float))),
        ):
            return cls.query.get(int(id))
        return None


class TimeMixin(object):
    """A mixin that adds a creation and update time columns named
    ``created_time`` and ``last_update_time`` to any declarative-mapped class.
    """
    __table_args__ = {'extend_existing': True}

    created_time = Column(db.DateTime(), default=datetime.datetime.utcnow)
    last_update_time = Column(db.DateTime(), default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)


def ReferenceCol(tablename, nullable=True, pk_name='id', **kwargs):
    """Column that adds primary key foreign key reference.

    Usage: ::

        category_id = ReferenceCol('category')
        category = relationship('Category', backref='categories')
    """
    return db.Column(
        db.ForeignKey("{0}.{1}".format(tablename, pk_name)),
        nullable=nullable, **kwargs)
