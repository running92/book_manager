export function dateText(value) {
  if (!value) return '-'
  return String(value).slice(0, 10)
}

export function localBookTitle(book, locale) {
  if (!book) return '-'
  return locale === 'en-US' ? book.title_en : book.title_zh
}

export function localCategoryName(category, locale) {
  if (!category) return '-'
  return locale === 'en-US' ? category.name_en : category.name_zh
}

