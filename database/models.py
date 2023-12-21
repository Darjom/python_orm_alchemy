from sqlalchemy import DateTime
from sqlalchemy import create_engine, Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base 


Base = declarative_base()


class Usern(Base):
    __tablename__ = 'usern'
    id_usern = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    password = Column(String)
    roles = Column(String)
    sessions = relationship('Session', back_populates='user')


class Session(Base):
    __tablename__ = 'sesion'
    id_session = Column(Integer, primary_key=True)
    id_usern = Column(Integer, ForeignKey('usern.id_usern'))
    pid = Column(Integer)
    activo = Column(Boolean)
    user = relationship('Usern', back_populates='sessions')


class Educador(Base):
    __tablename__ = "educador"
    id_educador = Column(Integer, primary_key=True, autoincrement=True)
    profesion = Column(String)
    especialidad = Column(String)

class Estudiante(Base):
    __tablename__ = "estudiante"

    id_estudiante = Column(Integer, primary_key=True, autoincrement=True)
    codigo = Column(Integer)  
    carrera = Column(String)


class Grupo(Base):
    __tablename__ = "grupo"

    id_grupo = Column(Integer, primary_key=True,autoincrement=True)
    nombre_grupo = Column(String(250))
    id_tipo_grupo = Column(String(250))
    fecha_creacion = Column(DateTime)


class Materia(Base):
    __tablename__ = "materia"

    id_materia = Column(Integer, primary_key=True)
    nombre_materia = Column(String(250))
    descripcion = Column(String(250))


class Tipo_grupo(Base):
    __tablename__ = "tipo_grupo"

    id_tipo_grupo = Column(Integer, primary_key=True)
    nombre_tipo_grupo = Column(String(250))


class Educador_grupo(Base):
    __tablename__ = "educador_grupo"

    id_educador = Column(Integer, ForeignKey("educador.id_educador"), primary_key=True)
    id_grupo = Column(Integer, ForeignKey("grupo.id_grupo"), primary_key=True)


class Estudiante_grupo(Base):
    __tablename__ = "estudiante_grupo"

    id_estudiante = Column(Integer, ForeignKey("estudiante.id_estudiante"), primary_key=True)
    id_grupo = Column(Integer, ForeignKey("grupo.id_grupo"), primary_key=True)

