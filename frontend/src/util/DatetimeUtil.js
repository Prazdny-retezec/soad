export function combineDateTime(date, time) {
  if (!date || !time) return null;

  const [hours, minutes] = time.split(':').map(Number);

  const d = new Date(date);
  d.setHours(hours);
  d.setMinutes(minutes);
  d.setSeconds(0);
  d.setMilliseconds(0);

  const year = d.getFullYear();
  const month = String(d.getMonth() + 1).padStart(2, '0');
  const day = String(d.getDate()).padStart(2, '0');
  const h = String(d.getHours()).padStart(2, '0');
  const m = String(d.getMinutes()).padStart(2, '0');
  const s = String(d.getSeconds()).padStart(2, '0');

  return `${year}-${month}-${day}T${h}:${m}:${s}`;
}