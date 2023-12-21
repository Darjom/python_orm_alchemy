from sqlalchemy.orm import sessionmaker
from sqlalchemy import func
from sqlalchemy.orm import joinedload
from .models import Base, Usern, Session, Estudiante, Educador, Grupo, Materia, Estudiante_grupo, Educador_grupo
from sqlalchemy import create_engine

class DatabaseManager:
    def __init__(self, db_url):
        # Create an Engine object instead of using the URL directly
        self.engine = create_engine(db_url)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)

    def insert_user(self, username, password):
        session = self.Session()
        new_user = Usern(username=username, password=password, roles=' ')
        session.add(new_user)
        session.commit()
        session.close()

    def get_user_id(self, username):
        session = self.Session()
        user = session.query(Usern).filter_by(username=username).first()
        session.close()
        return user.id_usern if user else None

    def verify_credentials(self, username, password):
        session = self.Session()
        user = session.query(Usern).filter_by(username=username, password=password).first()
        session.close()
        return user is not None

    def generate_pid(self):
        session = self.Session()
        new_pid = session.query(func.pg_backend_pid()).scalar()
        session.close()
        return new_pid

    def get_user_pid(self, username):
        session = self.Session()
        user = session.query(Usern).filter_by(username=username).first()
        if user:
            session_info = session.query(Session).filter_by(id_usern=user.id_usern).first()
            session.close()
            return session_info.pid if session_info else None
        session.close()
        return None

    def obtener_apellidos_nombres(self, id_usuario):
        session = self.Session()
        user = session.query(Usern).filter_by(id_usern=id_usuario).first()
        session.close()
        return (user.apellido, user.nombre) if user else None

    def update_user(self, user_id, new_username, new_password, new_name, new_lastname):
        session = self.Session()
        user = session.query(Usern).filter_by(id_usern=user_id).first()
        if user:
            user.username = new_username
            user.password = new_password
            user.nombre = new_name
            user.apellido = new_lastname
            session.commit()
        session.close()

    def delete_session(self, username):
        session = self.Session()
        user = session.query(Usern).filter_by(username=username).first()
        if user:
            session.query(Session).filter_by(id_usern=user.id_usern).delete()
            session.commit()
        session.close()

    def insert_session(self, username, pid):
        session = self.Session()
        user = session.query(Usern).filter_by(username=username).first()
        if user:
            new_session = Session(id_usern=user.id_usern, pid=pid, activo=True)
            session.add(new_session)
            session.commit()
        session.close()
        

    def listaUi(self, user_id):
        session = self.Session()
        user = (
            session.query(Usern.id_usern)
            .join(Usern.roles)
            .join(Session, Usern.sessions)
            .filter(Usern.id_usern == user_id)
        ).all()
        session.close()
        return [u.id_usern for u in user]

    def get_student_groups(self, student_id):
        session = self.Session()
        groups = (
            session.query(Grupo.nombre_grupo, Materia.nombre_materia)
            .join(Materia, Grupo.materia)
            .join(Estudiante_grupo, Grupo.estudiantes)
            .filter(Estudiante_grupo.id_estudiante == student_id)
        ).all()
        session.close()
        return groups

    def register_user_as_student(self, user_id, codigoEst):
        session = self.Session()
        new_student = Estudiante(id_estudiante=user_id, codigo=codigoEst, carrera='')
        session.add(new_student)
        session.commit()
        session.close()

    def register_user_as_teacher(self, user_id):
        session = self.Session()
        new_teacher = Educador(id_educador=user_id, profesion='', especialidad='')
        session.add(new_teacher)
        session.commit()
        session.close()

    def get_educador_grupos(self, educador_id):
        session = self.Session()
        grupos = (
            session.query(Grupo.nombre_grupo, Materia.nombre_materia)
            .join(Educador_grupo, Grupo.educadores)
            .join(Materia, Grupo.materia)
            .filter(Educador_grupo.id_educador == educador_id)
        ).all()
        session.close()
        return grupos


    def get_materia_id(self, nombre_materia):
        materia = self.session.query(Materia.id_materia).filter_by(nombre_materia=nombre_materia).first()
        return materia.id_materia if materia else None

    def agregar_estudiante_a_grupo(self, user_id, materia_id):
        grupo = (
            self.session.query(Grupo.id_grupo)
            .filter_by(id_materia=materia_id)
            .options(joinedload(Grupo.estudiantes))
            .first()
        )
        if grupo:
            grupo.estudiantes.append(Estudiante(id_estudiante=user_id))
            self.session.commit()
            return grupo.id_grupo
        else:
            return None

    def insertar_materia(self, nombre_materia):
        new_materia = Materia(nombre_materia=nombre_materia, descripcion='')
        self.session.add(new_materia)
        self.session.commit()

    def obtener_todas_las_materias(self):
        materias = self.session.query(Materia.id_materia, Materia.nombre_materia).all()
        return materias

    def close_connection(self):
        self.Session.close()

