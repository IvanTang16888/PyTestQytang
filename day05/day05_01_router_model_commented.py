# ============================================================
# Day05 任務 1：用 SQLAlchemy ORM 建立「設定備份表」router_config
#
# 功能：
#   1. 定義 RouterConfig 模型 → SQLite 裡的 router_config 表（每採集一次新增一行）
#   2. 直接執行時：印出表結構、索引、主鍵，並「試寫一筆」檢查 id 與 record_time
#      是否自動產生，最後 rollback 撤銷，不留下測試資料
#
# 被任務 2 import 時：只會建表 + 提供 RouterConfig、Session，不會跑下面的測試
#
# 注意：create_all 只會「建立不存在的表」，不會修改已存在的表。
#       改了欄位定義要重建時 → 先把 router_config.db 改名備份，再重跑本程式
# ============================================================

import datetime      # 用 datetime.datetime.now 當作 record_time 的預設值
from sqlalchemy import create_engine , inspect , Column , Integer , String , DateTime
# create_engine：連線資料庫；inspect：讀取表結構（欄位、索引、主鍵）
# Column：定義欄位；Integer / String / DateTime：欄位型別
from sqlalchemy.orm import declarative_base , sessionmaker
# declarative_base：ORM 類別的基底；sessionmaker：產生 Session（工作階段）

# sqlite:///router_config.db → 3 個斜線 = 相對路徑，db 檔建在「執行指令時所在的目錄」
# check_same_thread=False → 允許不同執行緒使用同一個連線（SQLite 預設不允許）
engine = create_engine('sqlite:///router_config.db' , connect_args={'check_same_thread': False})

Base = declarative_base()                # 所有模型都繼承它
Session = sessionmaker(bind=engine)      # Session() 就會得到一個綁定此資料庫的 session

class RouterConfig(Base):
    """路由器配置备份模型：每采集一次新增一行。"""
    __tablename__ = 'router_config'      # 對應的資料表名稱

    # ---------- 待完成 1：依表結構定義 5 個欄位 ----------
    # 寫法：欄位名 = Column(型別, 約束...)   ← 型別放在 Column( ) 小括號裡的第一個
    #
    # 主鍵、自動遞增：新增資料時不用給 id，資料庫自動編 1, 2, 3...
    id = Column( Integer,primary_key=True,autoincrement=True)
    # 路由器 IP：最長 64 字、不可空、建索引（index=True → 依 IP 查詢比較快，
    # 索引名稱會自動叫 ix_router_config_router_ip）
    router_ip = Column(String(64),nullable=False,index=True)
    # 整份設定正文（show run 從 hostname 到 end）
    router_config = Column(String(99999),nullable=False)
    # SHA256 摘要（64 個 16 進位字元，預留 500 很寬裕）
    config_hash = Column(String(500),nullable=False)
    # 寫入時間：default 給「函式本身」，不加括號 → 每次寫入時才呼叫，取當下時間
    #   加了括號 datetime.datetime.now() → 變成程式啟動那一刻的固定時間（錯誤）
    #   沒寫 nullable → 預設 nullable=True（預期輸出也是 True）
    record_time = Column(DateTime,default=datetime.datetime.now)



    # print(物件) 時顯示的格式
    def __repr__(self):
        return (f"{self.__class__.__name__}("
                f"路由器IP地址: {self.router_ip} | "
                f"配置Hash: {self.config_hash} | "
                f"紀錄時間: {self.record_time})")

# 依照上面的模型建表；checkfirst=True → 表已存在就跳過
# 放在 if __name__ 外面 → 被任務 2 import 時也會確保表存在
Base.metadata.create_all(engine,checkfirst=True)

if __name__ == '__main__':
    # inspect：直接從資料庫讀出「實際」建好的表結構，用來驗證欄位有沒有寫對
    inspector = inspect(engine)
    print('router_config 表結構: ')
    for column in inspector.get_columns('router_config'):
        # :<14 / :<16 → 靠左對齊並補空白到 14 / 16 個字寬，讓輸出排整齊
        print(f"  {column['name']:<14}{str(column['type']):<16}nullable={column['nullable']}")
    for index in inspector.get_indexes('router_config'):
        print(f"  索引 {index['name']} -> {index['column_names']}")

    print('  主键 ->', inspector.get_pk_constraint('router_config')['constrained_columns'])
    # 测试自动生成的值，不把测试记录留在正式备份表里。
    with Session() as session:                  # with：區塊結束自動關閉 session
        started = datetime.datetime.now()       # 記下測試開始時間，用來檢查 record_time
        # 故意不給 id 和 record_time → 看它們會不會自動產生
        record = RouterConfig(router_ip='test',router_config='test',config_hash='test')
        session.add(record)
        # flush：把 INSERT 先送到資料庫（所以拿得到 id），但「還沒 commit」
        session.flush()
        # 檢查：id 是整數、record_time 有值、而且不早於測試開始時間
        if not isinstance(record.id,int) or record.record_time is None or record.record_time < started:
            raise ValueError('检查自动ID与record_time的default设置')
        print(f'自动生成: id={record.id} , record_time={record.record_time}')
        print('自动ID和写入时间:通过')
        # rollback：撤銷還沒 commit 的變更 → 測試資料不會留在正式表裡
        session.rollback()  # 测试结束撤销这一行
