from project import db


class Model(db.Model):
    __abstract__ = True

    def save(self):
        db.session.add(self)
        db.session.commit()

        return self

    def update(self, props: dict):
        for key, value in props.items():
            try:
                setattr(self, key, value)
            except Exception as e:
                print("**** ERROR UPDATE {} ****".format(key), e)

        db.session.add(self)
        db.session.commit()

        return self

    def delete(self):
        db.session.delete(self)
        db.session.commit()

        return self

    def save_with_status(self, obj, obj_name):
        try:
            obj.save()
            return {
                'status': 'ok',
                obj_name: obj.json()
            }
        except Exception as e:
            db.session.rollback()
            return {
                'status': 'error',
                'exception': str(e)
            }

    @staticmethod
    def execute_query(query):
        rsp = db.engine.execute(query)
        if not rsp:
            return []
        rsp = [dict(r.items()) for r in rsp]
        return rsp
