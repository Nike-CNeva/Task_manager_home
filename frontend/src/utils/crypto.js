import CryptoJS from 'crypto-js';

const SECRET_KEY = import.meta.env.VITE_API_SECRET_KEY;

export function encryptToken(token) {
  return CryptoJS.AES.encrypt(token, SECRET_KEY).toString();
}

export function decryptToken(encryptedToken) {
  if (!encryptedToken) return null;
  const bytes = CryptoJS.AES.decrypt(encryptedToken, SECRET_KEY);
  try {
    return bytes.toString(CryptoJS.enc.Utf8);
  } catch {
    return null;
  }
}
export function encrypt(data) {
  return CryptoJS.AES.encrypt(JSON.stringify(data), SECRET_KEY).toString();
}

export function decrypt(ciphertext) {
  const bytes = CryptoJS.AES.decrypt(ciphertext, SECRET_KEY);
  const decryptedData = bytes.toString(CryptoJS.enc.Utf8);
  return JSON.parse(decryptedData);
}