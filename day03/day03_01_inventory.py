from datetime import datetime

from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker


engine = create_engine("sqlite:///device_inventory.db")
Base = declarative_base()
Session = sessionmaker(bind=engine)


class Device(Base):
    __tablename__ = "devices"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(64), index=True, nullable=False)
    type = Column(String(32), nullable=False)
    version = Column(String(64))
    location = Column(String(64))
    create_time = Column(DateTime, default=datetime.now)

    def __repr__(self):
        return (f"Device(设备名称: {self.name} | 类型: {self.type} | 版本: {self.version} "
                f"| 位置: {self.location} | 入库时间: {self.create_time})")


device_list = [
    {'name': 'R1', 'type': 'router', 'version': 'IOS XE 17.14', 'location': 'Beijing-IDC-A'},
    {'name': 'R2', 'type': 'router', 'version': 'IOS XE 17.14', 'location': 'Shanghai-IDC-B'},
    {'name': 'SW1', 'type': 'switch', 'version': 'IOS 15.2', 'location': 'Beijing-IDC-A'},
    {'name': 'SW2', 'type': 'switch', 'version': 'IOS 15.2', 'location': 'Shanghai-IDC-B'},
    {'name': 'FW1', 'type': 'firewall', 'version': 'ASA 9.16', 'location': 'Beijing-IDC-A'},
    {'name': 'FW2', 'type': 'firewall', 'version': 'FTD 7.2', 'location': 'Shenzhen-IDC-C'},
]


def init_db(session):
    Base.metadata.create_all(engine)
    if session.query(Device).count() == 0:
        for device in device_list:
            session.add(Device(**device))
        session.commit()
        print("数据库初始化完成, 已写入 {} 条设备记录".format(len(device_list)))


def print_devices(devices):
    if not devices:
        print("没有找到符合条件的设备")
    for device in devices:
        print(device)


MENU = """
请选择查询方式:
输入 1: 查询所有设备
输入 2: 根据设备名称查询
输入 3: 根据设备类型查询
输入 4: 根据机房位置查询
输入 0: 退出"""


def main():
    session = Session()
    init_db(session)

    while True:
        print(MENU)
        choice = input("请输入查询选项: ").strip()

        if choice == "1":
            print_devices(session.query(Device).all())

        elif choice == "2":
            name = input("请输入设备名称: ").strip()
            print_devices(session.query(Device).filter_by(name=name).all())

        elif choice == "3":
            device_type = input("请输入设备类型 (router/switch/firewall) : ").strip()
            print_devices(session.query(Device).filter_by(type=device_type).all())

        elif choice == "4":
            keyword = input("请输入机房位置关键词: ").strip()
            print_devices(session.query(Device).filter(Device.location.like(f"%{keyword}%")).all())

        elif choice == "0":
            print("退出程序")
            break

        else:
            print("输入错误, 请输入 0-4")

    session.close()


if __name__ == "__main__":
    main()
