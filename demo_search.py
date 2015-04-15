from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy, BaseQuery
from sqlalchemy_searchable import SearchQueryMixin
from sqlalchemy_utils.types import TSVectorType
from sqlalchemy_searchable import make_searchable

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = (
    'postgres://TylerPort:butter1919@localhost/search'
)
#app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'notreallyasecret'
db = SQLAlchemy(app)
make_searchable()


class ArticleQuery(BaseQuery, SearchQueryMixin):
    pass


class Article(db.Model):
    query_class = ArticleQuery
    __tablename__ = 'article'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Unicode(255))
    content = db.Column(db.UnicodeText)
    search_vector = db.Column(TSVectorType('name', 'content'))

db.configure_mappers()

db.Model.metadata.create_all(db.session.connection())

a = Article(name=u'finland', content=u'finland')
db.session.add(a)
db.session.commit()

print Article.query.search(u'finland').limit(5).all()

#db.Model.metadata.drop_all(db.session.connection())
#db.session.commit()


