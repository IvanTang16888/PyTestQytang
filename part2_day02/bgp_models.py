from sqlalchemy import create_engine , Column , Integer , String , ForeignKey
from sqlalchemy.orm import declarative_base , sessionmaker , relationship

engine = create_engine('postgresql+psycopg2://bgpuser:Cisc0123@127.0.0.1:15435/bgpdb')

Base = declarative_base()

class Router(Base):
    __tablename__ = 'aiops_router'
    id = Column(Integer,primary_key=True,autoincrement=True)
    name = Column(String(64),unique=True)
    host = Column(String(64))
    interfaces = relationship('Interface')
    bgp = relationship('BGP',uselist=False)

class Interface(Base):
    __tablename__ = 'aiops_interface'
    id = Column(Integer,primary_key=True,autoincrement=True)
    router_id = Column(Integer,ForeignKey('aiops_router.id'))
    name = Column(String(64))
    address = Column(String(64))
    mask = Column(String(64))
    description = Column(String(128))

class BGP(Base):
    __tablename__ = 'aiops_bgp'
    id = Column(Integer,primary_key=True,autoincrement=True)
    router_id = Column(Integer,ForeignKey('aiops_router.id'),unique=True)
    local_as = Column(Integer)
    router_id_value = Column(String(64))
    neighbors = relationship('Neighbor')
    networks = relationship('Network')

class Neighbor(Base):
    __tablename__ = 'aiops_neighbor'
    id = Column(Integer,primary_key=True,autoincrement=True)
    bgp_id = Column(Integer,ForeignKey('aiops_bgp.id'))
    peer_ip = Column(String(64))
    remote_as = Column(Integer)

class Network(Base):
    __tablename__ = 'aiops_network'
    id = Column(Integer,primary_key=True,autoincrement=True)
    bgp_id = Column(Integer,ForeignKey('aiops_bgp.id'))
    prefix = Column(String(64))
    mask = Column(String(64))

def session_factory():
    Base.metadata.create_all(engine)
    return sessionmaker(bind=engine)