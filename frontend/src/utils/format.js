export function formatQuantity(qty) {
  if (qty % 1 === 0) return qty.toString();
  const whole = Math.floor(qty);
  const fraction = qty - whole;
  const map = { 0.25: '¼', 0.33: '⅓', 0.5: '½', 0.66: '⅔', 0.75: '¾' };
  const closest = Object.keys(map).reduce((a, b) => 
    Math.abs(b - fraction) < Math.abs(a - fraction) ? b : a
  );
  return whole ? `${whole} ${map[closest]}` : map[closest];
}