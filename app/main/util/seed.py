from ..model.language import Language
from .. import db


languages = ['Hungarian', 'German', 'Portugese']


def seed_languages():
    for _language in languages:
        language = Language(name=_language)
        db.session.add(language)
    
    db.session.commit()



