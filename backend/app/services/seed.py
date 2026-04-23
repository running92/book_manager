from datetime import date, timedelta

from app.models import Book, BorrowRecord, Category, User
from extensions import db


def seed_demo_data(force=False):
    if User.query.first() and not force:
        return

    db.session.query(BorrowRecord).delete()
    db.session.query(Book).delete()
    db.session.query(Category).delete()
    db.session.query(User).delete()

    admin = User(username="admin", real_name="系统管理员", role="admin", phone="13800000000", email="admin@example.com")
    admin.set_password("admin123")
    reader = User(username="user1", real_name="张三", role="reader", phone="13900000001", email="user1@example.com")
    reader.set_password("123456")
    reader2 = User(username="user2", real_name="李四", role="reader", phone="13900000002", email="user2@example.com")
    reader2.set_password("123456")
    db.session.add_all([admin, reader, reader2])

    categories = [
        Category(name_zh="计算机", name_en="Computer Science", description="编程、网络与数据库", sort_order=1),
        Category(name_zh="文学", name_en="Literature", description="小说、散文与诗歌", sort_order=2),
        Category(name_zh="经济管理", name_en="Economics & Management", description="经济学与管理学", sort_order=3),
        Category(name_zh="历史", name_en="History", description="历史与文化", sort_order=4),
        Category(name_zh="外语", name_en="Languages", description="语言学习资料", sort_order=5),
        Category(name_zh="艺术", name_en="Arts", description="艺术设计与审美", sort_order=6),
    ]
    db.session.add_all(categories)
    db.session.flush()

    books = [
        Book(isbn="9787115428028", title_zh="Python 编程：从入门到实践", title_en="Python Crash Course", author="Eric Matthes", publisher="人民邮电出版社", publish_date="2023-01", category_id=categories[0].id, description_zh="适合 Python 初学者的实践教程。", description_en="A practical Python tutorial for beginners.", total_stock=5, available_stock=4, location="A1-01"),
        Book(isbn="9787115521644", title_zh="深入理解计算机系统", title_en="Computer Systems: A Programmer's Perspective", author="Randal E. Bryant", publisher="机械工业出版社", publish_date="2022-06", category_id=categories[0].id, description_zh="系统学习计算机底层原理。", description_en="Computer systems from a programmer's perspective.", total_stock=3, available_stock=3, location="A1-02"),
        Book(isbn="9787111213826", title_zh="算法导论", title_en="Introduction to Algorithms", author="Thomas H. Cormen", publisher="机械工业出版社", publish_date="2021-05", category_id=categories[0].id, description_zh="经典算法教材。", description_en="A classic textbook on algorithms.", total_stock=4, available_stock=4, location="A1-03"),
        Book(isbn="9787020002207", title_zh="红楼梦", title_en="Dream of the Red Chamber", author="曹雪芹", publisher="人民文学出版社", publish_date="2020-10", category_id=categories[1].id, description_zh="中国古典文学名著。", description_en="A masterpiece of classical Chinese literature.", total_stock=6, available_stock=5, location="B2-01"),
        Book(isbn="9787020008728", title_zh="围城", title_en="Fortress Besieged", author="钱锺书", publisher="人民文学出版社", publish_date="2019-08", category_id=categories[1].id, description_zh="现代文学经典作品。", description_en="A classic modern Chinese novel.", total_stock=4, available_stock=4, location="B2-02"),
        Book(isbn="9787508649719", title_zh="原则", title_en="Principles", author="Ray Dalio", publisher="中信出版社", publish_date="2021-11", category_id=categories[2].id, description_zh="工作与生活原则。", description_en="Principles for life and work.", total_stock=4, available_stock=3, location="C3-01"),
        Book(isbn="9787508684031", title_zh="经济学原理", title_en="Principles of Economics", author="N. Gregory Mankiw", publisher="北京大学出版社", publish_date="2022-03", category_id=categories[2].id, description_zh="经济学基础教材。", description_en="An introductory economics textbook.", total_stock=3, available_stock=3, location="C3-02"),
        Book(isbn="9787101080752", title_zh="史记", title_en="Records of the Grand Historian", author="司马迁", publisher="中华书局", publish_date="2018-12", category_id=categories[3].id, description_zh="中国纪传体通史。", description_en="A foundational Chinese historical text.", total_stock=3, available_stock=3, location="D4-01"),
        Book(isbn="9787544655486", title_zh="新概念英语", title_en="New Concept English", author="L. G. Alexander", publisher="外语教学与研究出版社", publish_date="2020-09", category_id=categories[4].id, description_zh="英语学习经典教材。", description_en="A classic English learning textbook.", total_stock=8, available_stock=8, location="E5-01"),
        Book(isbn="9787535688408", title_zh="设计中的设计", title_en="Designing Design", author="原研哉", publisher="湖南美术出版社", publish_date="2021-04", category_id=categories[5].id, description_zh="设计理念与审美思考。", description_en="Essays on design thinking and aesthetics.", total_stock=2, available_stock=2, location="F6-01"),
    ]
    db.session.add_all(books)
    db.session.flush()

    records = [
        BorrowRecord(user_id=reader.id, book_id=books[0].id, borrow_date=date.today() - timedelta(days=5), due_date=date.today() + timedelta(days=25), status="borrowed", remark="演示借阅"),
        BorrowRecord(user_id=reader.id, book_id=books[3].id, borrow_date=date.today() - timedelta(days=35), due_date=date.today() - timedelta(days=5), status="overdue", remark="逾期演示"),
        BorrowRecord(user_id=reader2.id, book_id=books[5].id, borrow_date=date.today() - timedelta(days=20), due_date=date.today() - timedelta(days=1), return_date=date.today() - timedelta(days=2), status="returned", remark="已归还演示"),
    ]
    db.session.add_all(records)
    db.session.commit()

