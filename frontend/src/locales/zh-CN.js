export default {
  app: { name: '图书管理系统', admin: '管理员', reader: '读者', language: '语言' },
  common: {
    search: '搜索', reset: '重置', add: '新增', edit: '编辑', delete: '删除', detail: '详情',
    save: '保存', cancel: '取消', confirm: '确认', actions: '操作', status: '状态',
    success: '操作成功', failed: '操作失败', deleteConfirm: '确认删除该数据吗？',
    empty: '暂无数据', all: '全部', submit: '提交', back: '返回', upload: '上传',
    enabled: '正常', disabled: '禁用', available: '上架', unavailable: '下架',
    borrowed: '借阅中', returned: '已归还', overdue: '已逾期'
  },
  login: { title: '毕业设计图书管理系统', subtitle: 'Library Management System', username: '用户名', password: '密码', button: '登录', demo: '管理员：admin / admin123；读者：user1 / 123456' },
  menu: { dashboard: '首页', books: '图书管理', categories: '分类管理', users: '用户管理', borrow: '借阅管理', myBorrow: '我的借阅', profile: '个人中心' },
  dashboard: {
    title: '系统首页', bookTotal: '图书总数', availableTotal: '可借库存', borrowedTotal: '已借出', userTotal: '用户总数',
    currentBorrow: '当前借阅', recordTotal: '借阅记录', recent: '最近借阅', category: '分类分布', trend: '借阅趋势',
    recommended: '推荐图书', newBooks: '新上架图书', myCurrent: '我的当前借阅', reminders: '借阅提醒'
  },
  book: {
    title: '图书管理', isbn: 'ISBN', titleZh: '中文书名', titleEn: '英文书名', author: '作者', publisher: '出版社',
    publishDate: '出版日期', category: '分类', cover: '封面', descZh: '中文简介', descEn: '英文简介',
    totalStock: '总库存', availableStock: '可借库存', location: '馆藏位置', borrow: '借阅图书', keyword: '书名 / ISBN / 作者'
  },
  category: { title: '分类管理', nameZh: '中文名称', nameEn: '英文名称', description: '描述', sortOrder: '排序' },
  user: { title: '用户管理', username: '用户名', realName: '姓名', role: '角色', phone: '手机号', email: '邮箱', password: '密码', resetPassword: '重置密码' },
  borrow: { title: '借阅管理', myTitle: '我的借阅', borrower: '借阅人', book: '图书', borrowDate: '借阅日期', dueDate: '应还日期', returnDate: '归还日期', returnBook: '归还', remark: '备注' },
  profile: { title: '个人中心', basic: '基础信息', password: '修改密码', oldPassword: '原密码', newPassword: '新密码' },
  validate: { required: '该字段不能为空', passwordLength: '密码至少 6 位' },
  notFound: { title: '页面不存在', backHome: '返回首页' }
}

