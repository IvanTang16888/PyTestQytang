# ============================================================
# Day03 任務 1：SQLAlchemy ORM 練習 —— 設備 Inventory（資產清單）系統
#
# 功能：
#   1. 把 6 台設備（名稱、類型、版本、機房）存進 SQLite 資料庫 device_inventory.db
#   2. 用選單查詢：全部 / 依名稱 / 依類型 / 依機房關鍵字
#   3. 只在資料表是空的時候才寫入初始資料 → 重複執行不會重複新增、入庫時間不變
#
# ORM 是什麼？
#   Object Relational Mapping（物件關聯對映）
#   → 用 Python 的「類別」代表資料表、用「物件」代表一筆資料，
#     不用自己寫 SQL 語法（SELECT / INSERT），SQLAlchemy 會幫你轉成 SQL
# ============================================================

from datetime import datetime      # 用來取得「現在時間」，當作入庫時間

# create_engine：建立資料庫連線
# Column：定義資料表的欄位；Integer / String / DateTime：欄位的資料型別
from sqlalchemy import create_engine, Column, Integer, String, DateTime
# declarative_base：產生 ORM 類別的「基底類別」
# sessionmaker：產生 Session（工作階段），所有新增 / 查詢都透過 session
from sqlalchemy.orm import declarative_base, sessionmaker


# ------------------------------------------------------------
# 1. 連線資料庫
# ------------------------------------------------------------
# "sqlite:///device_inventory.db"
#   sqlite://           → 使用 SQLite（一個檔案就是一個資料庫，不用另外裝伺服器）
#   /device_inventory.db → 檔名；3 個斜線 = 相對路徑，檔案建在「執行指令時所在的目錄」
#   檔案不存在時會自動建立
engine = create_engine("sqlite:///device_inventory.db")

# 所有 ORM 類別都要繼承這個 Base，SQLAlchemy 才知道它們對應到資料表
Base = declarative_base()

# Session 是一個「工廠」，之後呼叫 Session() 就會得到一個 session 物件
Session = sessionmaker(bind=engine)


# ------------------------------------------------------------
# 2. 定義資料表：一個類別 = 一張表，一個 Column = 一個欄位
# ------------------------------------------------------------
class Device(Base):
    __tablename__ = "devices"       # 資料表名稱（題目指定 devices）

    # primary_key=True → 主鍵；autoincrement=True → 自動遞增 1, 2, 3...
    id = Column(Integer, primary_key=True, autoincrement=True)
    # index=True → 幫 name 建立索引，依名稱查詢時比較快（題目要求）
    # nullable=False → 這個欄位不能是空值
    name = Column(String(64), index=True, nullable=False)
    type = Column(String(32), nullable=False)
    version = Column(String(64))
    location = Column(String(64))
    # default=datetime.now → 新增資料時「自動」填入當下時間
    # 注意：是 datetime.now（把函式交給 SQLAlchemy，寫入時才呼叫）
    #       不是 datetime.now()（那樣會在程式啟動時就固定成同一個時間）
    create_time = Column(DateTime, default=datetime.now)

    # __repr__：決定 print(物件) 時要印出什麼
    # 沒寫的話只會印出 <__main__.Device object at 0x7f...>，看不懂
    def __repr__(self):
        return (f"Device(设备名称: {self.name} | 类型: {self.type} | 版本: {self.version} "
                f"| 位置: {self.location} | 入库时间: {self.create_time})")


# ------------------------------------------------------------
# 3. 題目給的 6 台設備資料（列表裡放字典）
# ------------------------------------------------------------
device_list = [
    {'name': 'R1', 'type': 'router', 'version': 'IOS XE 17.14', 'location': 'Beijing-IDC-A'},
    {'name': 'R2', 'type': 'router', 'version': 'IOS XE 17.14', 'location': 'Shanghai-IDC-B'},
    {'name': 'SW1', 'type': 'switch', 'version': 'IOS 15.2', 'location': 'Beijing-IDC-A'},
    {'name': 'SW2', 'type': 'switch', 'version': 'IOS 15.2', 'location': 'Shanghai-IDC-B'},
    {'name': 'FW1', 'type': 'firewall', 'version': 'ASA 9.16', 'location': 'Beijing-IDC-A'},
    {'name': 'FW2', 'type': 'firewall', 'version': 'FTD 7.2', 'location': 'Shenzhen-IDC-C'},
]


# ------------------------------------------------------------
# 4. 初始化：建表 + 只在空表時寫入資料
# ------------------------------------------------------------
def init_db(session):
    # 依照上面所有繼承 Base 的類別建立資料表
    # 表已經存在就跳過，不會刪掉舊資料
    Base.metadata.create_all(engine)

    # query(Device).count() → 等於 SQL 的 SELECT COUNT(*) FROM devices
    # 只有 0 筆的時候才寫入 → 第二次執行就不會再寫一次（不會變 12 筆、時間也不會變）
    if session.query(Device).count() == 0:
        for device in device_list:
            # Device(**device)：** 會把字典拆開成參數
            #   等於 Device(name='R1', type='router', version='IOS XE 17.14', location='Beijing-IDC-A')
            # session.add()：先放進 session（還沒真的寫進資料庫）
            session.add(Device(**device))
        # commit()：一次真正寫進資料庫（這時 create_time 才會自動填上）
        session.commit()
        print("数据库初始化完成, 已写入 {} 条设备记录".format(len(device_list)))


# ------------------------------------------------------------
# 5. 印出查詢結果
# ------------------------------------------------------------
def print_devices(devices):
    # 空列表在 if 判斷裡等於 False → not [] 是 True
    if not devices:
        print("没有找到符合条件的设备")
    for device in devices:
        print(device)       # print 物件 → 自動呼叫上面寫的 __repr__


# 選單文字（三個引號可以寫多行）
MENU = """
请选择查询方式:
输入 1: 查询所有设备
输入 2: 根据设备名称查询
输入 3: 根据设备类型查询
输入 4: 根据机房位置查询
输入 0: 退出"""


# ------------------------------------------------------------
# 6. 主程式：選單迴圈
# ------------------------------------------------------------
def main():
    session = Session()     # 開一個 session，整個程式共用
    init_db(session)

    # while True：無限迴圈，每次查詢完會回到這裡重新顯示選單，直到輸入 0 才 break
    while True:
        print(MENU)
        # input() 拿到的一定是「字串」，所以下面跟 "1"、"2" 比（不是數字 1、2）
        # strip() 去掉不小心多打的空白
        choice = input("请输入查询选项: ").strip()

        if choice == "1":
            # .all() → 取回全部資料，結果是一個 Device 物件的列表
            # 等於 SQL：SELECT * FROM devices
            print_devices(session.query(Device).all())

        elif choice == "2":
            name = input("请输入设备名称: ").strip()
            # filter_by(欄位=值) → 精確比對（完全一樣才算）
            # 等於 SQL：SELECT * FROM devices WHERE name = 'SW1'
            print_devices(session.query(Device).filter_by(name=name).all())

        elif choice == "3":
            device_type = input("请输入设备类型 (router/switch/firewall) : ").strip()
            # 變數不取名 type，因為 type 是 Python 內建函式的名字
            # filter_by 左邊的 type 是「欄位名稱」，右邊的 device_type 是「變數」
            print_devices(session.query(Device).filter_by(type=device_type).all())

        elif choice == "4":
            keyword = input("请输入机房位置关键词: ").strip()
            # 模糊查詢要用 filter（不是 filter_by），寫法是 類別.欄位.like(...)
            # % 是萬用字元：%Beijing% = 前後是什麼都可以，只要中間有 Beijing
            # 等於 SQL：SELECT * FROM devices WHERE location LIKE '%Beijing%'
            print_devices(session.query(Device).filter(Device.location.like(f"%{keyword}%")).all())

        elif choice == "0":
            print("退出程序")
            break           # 跳出 while 迴圈

        else:
            print("输入错误, 请输入 0-4")

    session.close()         # 用完關閉 session，釋放資料庫連線


# 只有「直接執行這個檔案」時才跑 main()
# 如果被別的程式 import，就不會自動執行
if __name__ == "__main__":
    main()
