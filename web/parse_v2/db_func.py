from sqlalchemy import desc
from datetime import datetime, timedelta
from sqlalchemy.orm.exc import NoResultFound


def get_last_conrtact_date(self):
    '''
    Получение даты последнего отпарсенного контракта
    '''
    try:
        with self.app.app_context():
            a = self.Contrant_card.query.order_by(desc(self.Contrant_card.date)).first()

        return a.date
    except:
        # print('None')
        return None

def get_today(self):
    d = datetime.now()
    d = d - timedelta(
            hours = d.hour,
            minutes = d.minute,
            seconds = d.second,
            microseconds = d.microsecond)
    return d


def insert_new(self, contrant_cards):
    q_c = 0
    for contr_kwargs in contrant_cards:
        try:
            c_db = self.db.session.query(self.Contrant_card).filter_by(number = contr_kwargs['number']).one()
        except NoResultFound:
            ci = self.Contrant_card(**contr_kwargs)
            self.db.session.add(ci)
            q_c += 1
    else:
        print(f'Записано в БД {q_c}')
        self.db.session.commit()
