# ============================================================
# 第二部分 Day02 任務 1：BGP 規劃資料的 ORM 模型（5 張表）
#
# 表的關係（FK = ForeignKey 外鍵）：
#   aiops_router ─┬─< aiops_interface      一台 router 有多個介面
#                 └── aiops_bgp            一台 router 只有 1 份 BGP（uselist=False）
#                      ├─< aiops_neighbor  一份 BGP 有多個鄰居
#                      └─< aiops_network   一份 BGP 有多個宣告前綴
#
# 資料庫：compose.yml 起的 PostgreSQL，對外只開 127.0.0.1:15435
# 這支只「定義」表，本身不執行；由 seed / query 兩支 import 使用
# ============================================================

from sqlalchemy import create_engine , Column , Integer , String , ForeignKey
from sqlalchemy.orm import declarative_base , sessionmaker , relationship

# 連線字串：資料庫種類+驅動://帳號:密碼@主機:埠/資料庫名
# 帳密、埠、DB 名稱要跟 compose.yml 的 environment / ports 一致
engine = create_engine('postgresql+psycopg2://bgpuser:Cisc0123@127.0.0.1:15435/bgpdb')

# Base = 所有表的「共同祖先」；繼承它的 class 會被登記起來，
# 之後 Base.metadata.create_all() 才知道要建哪些表
Base = declarative_base()


class Router(Base):
    __tablename__ = 'aiops_router'                                 # 資料庫裡真正的表名
    id = Column(Integer,primary_key=True,autoincrement=True)       # 主鍵，自動 1, 2, 3...
    name = Column(String(64),unique=True)                          # 設備名稱不可重複（seed 靠它判斷已存在）
    host = Column(String(64))                                      # 管理地址
    # relationship 不是資料庫欄位，是 Python 端的「捷徑」：
    #   router.interfaces → 這台的所有 Interface（list）
    interfaces = relationship('Interface')
    #   router.bgp → 這台的那 1 份 BGP；uselist=False = 回傳單一物件，不是 list
    bgp = relationship('BGP',uselist=False)


class Interface(Base):
    __tablename__ = 'aiops_interface'
    id = Column(Integer,primary_key=True,autoincrement=True)
    # 外鍵：指向 aiops_router 表的 id 欄位 → 記錄「這個介面屬於哪台」
    router_id = Column(Integer,ForeignKey('aiops_router.id'))
    name = Column(String(64))
    address = Column(String(64))
    mask = Column(String(64))
    description = Column(String(128))


class BGP(Base):
    __tablename__ = 'aiops_bgp'
    id = Column(Integer,primary_key=True,autoincrement=True)
    # unique=True：同一台 router 只能有 1 筆 BGP（資料庫層面的一對一）
    router_id = Column(Integer,ForeignKey('aiops_router.id'),unique=True)
    local_as = Column(Integer)
    # 叫 router_id_value 是為了跟上面的外鍵 router_id 分開（這個是 BGP 的 Router ID，如 10.101.1.1）
    router_id_value = Column(String(64))
    neighbors = relationship('Neighbor')     # bgp.neighbors → 鄰居 list
    networks = relationship('Network')       # bgp.networks  → 宣告前綴 list


class Neighbor(Base):
    __tablename__ = 'aiops_neighbor'
    id = Column(Integer,primary_key=True,autoincrement=True)
    bgp_id = Column(Integer,ForeignKey('aiops_bgp.id'))   # 屬於哪一份 BGP
    peer_ip = Column(String(64))
    remote_as = Column(Integer)


class Network(Base):
    __tablename__ = 'aiops_network'
    id = Column(Integer,primary_key=True,autoincrement=True)
    bgp_id = Column(Integer,ForeignKey('aiops_bgp.id'))
    prefix = Column(String(64))
    mask = Column(String(64))


# 給別支程式用的「準備好就給你 Session 工廠」：
#   1. create_all：表不存在就建立，已存在就跳過（不會刪資料）
#   2. 回傳 sessionmaker（工廠本身），呼叫端再用 Session() 開一個連線
def session_factory():
    Base.metadata.create_all(engine)
    return sessionmaker(bind=engine)
