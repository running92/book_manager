export function assetUrl(path) {
  if (!path) return ''
  if (/^(https?:)?\/\//.test(path) || path.startsWith('data:') || path.startsWith('blob:')) return path

  const assetBase = import.meta.env.VITE_ASSET_BASE_URL
  if (assetBase) return `${assetBase.replace(/\/$/, '')}${path.startsWith('/') ? path : `/${path}`}`

  const apiBase = import.meta.env.VITE_API_BASE_URL
  if (/^https?:\/\//.test(apiBase || '')) {
    const url = new URL(apiBase)
    return `${url.origin}${path.startsWith('/') ? path : `/${path}`}`
  }

  return path
}
