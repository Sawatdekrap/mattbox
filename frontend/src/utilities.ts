const camelToSnake = (text: string): string =>
  text.replace(/([A-Z])/g, function ($1) {
    return "_" + $1.toLowerCase();
  });

export const toSnakeKeys = (obj: any): any => {
  if (typeof obj != "object") return obj;

  let newObj: Record<string, any> = {};
  Object.keys(obj).forEach((key) => {
    const newKey = camelToSnake(key);
    newObj[newKey] = toSnakeKeys(obj[key]);
  });

  return newObj;
};
