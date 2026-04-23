export default {
  app: { name: 'Library Management System', admin: 'Admin', reader: 'Reader', language: 'Language' },
  common: {
    search: 'Search', reset: 'Reset', add: 'Add', edit: 'Edit', delete: 'Delete', detail: 'Detail',
    save: 'Save', cancel: 'Cancel', confirm: 'Confirm', actions: 'Actions', status: 'Status',
    success: 'Success', failed: 'Failed', deleteConfirm: 'Are you sure you want to delete this item?',
    empty: 'No data', all: 'All', submit: 'Submit', back: 'Back', upload: 'Upload',
    enabled: 'Active', disabled: 'Disabled', available: 'Available', unavailable: 'Disabled',
    borrowed: 'Borrowed', returned: 'Returned', overdue: 'Overdue'
  },
  login: { title: 'Graduation Library Management System', subtitle: 'Library Management System', username: 'Username', password: 'Password', button: 'Login', demo: 'Admin: admin / admin123; Reader: user1 / 123456' },
  menu: { dashboard: 'Dashboard', books: 'Books', categories: 'Categories', users: 'Users', borrow: 'Borrow Records', myBorrow: 'My Borrowing', profile: 'Profile' },
  dashboard: {
    title: 'Dashboard', bookTotal: 'Books', availableTotal: 'Available Stock', borrowedTotal: 'Borrowed', userTotal: 'Users',
    currentBorrow: 'Current Borrows', recordTotal: 'Records', recent: 'Recent Records', category: 'Category Distribution', trend: 'Borrow Trend',
    recommended: 'Recommended Books', newBooks: 'New Books', myCurrent: 'My Current Borrowing', reminders: 'Reminders'
  },
  book: {
    title: 'Book Management', isbn: 'ISBN', titleZh: 'Chinese Title', titleEn: 'English Title', author: 'Author', publisher: 'Publisher',
    publishDate: 'Publish Date', category: 'Category', cover: 'Cover', descZh: 'Chinese Description', descEn: 'English Description',
    totalStock: 'Total Stock', availableStock: 'Available Stock', location: 'Location', borrow: 'Borrow', keyword: 'Title / ISBN / Author'
  },
  category: { title: 'Category Management', nameZh: 'Chinese Name', nameEn: 'English Name', description: 'Description', sortOrder: 'Sort' },
  user: { title: 'User Management', username: 'Username', realName: 'Real Name', role: 'Role', phone: 'Phone', email: 'Email', password: 'Password', resetPassword: 'Reset Password' },
  borrow: { title: 'Borrow Management', myTitle: 'My Borrowing', borrower: 'Borrower', book: 'Book', borrowDate: 'Borrow Date', dueDate: 'Due Date', returnDate: 'Return Date', returnBook: 'Return', remark: 'Remark' },
  profile: { title: 'Profile', basic: 'Basic Info', password: 'Change Password', oldPassword: 'Old Password', newPassword: 'New Password' },
  validate: { required: 'Required', passwordLength: 'Password must be at least 6 characters' },
  notFound: { title: 'Page Not Found', backHome: 'Back Home' }
}

