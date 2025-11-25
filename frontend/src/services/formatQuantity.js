// src/services/formatQuantity.js
export function formatQuantity(qty) {
  if (typeof qty !== 'number' || isNaN(qty)) return '0'
  if (qty % 1 === 0) return qty.toString()

  const whole = Math.floor(qty)
  const fraction = qty - whole
  const map = {
    0.25: '¼', 0.333: '⅓', 0.5: '½', 0.666: '⅔', 0.75: '¾'
  }
  const closest = Object.keys(map).reduce((a, b) =>
    Math.abs(parseFloat(b) - fraction) < Math.abs(parseFloat(a) - fraction) ? b : a
  )
  return whole ? `${whole} ${map[closest]}` : map[closest]
}