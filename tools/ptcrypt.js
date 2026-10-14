// Packet Tracer .pkt/.pka codec (scheme documented by the pka2xml project):
// file = obf1( Twofish-EAX( obf3( be32(len) || zlib(xml) ) ) ), key 0x89*16, iv 0x10*16
const zlib = require('zlib');
const tf = require('twofish').twofish();
const KEY = new Array(16).fill(137), IV = new Array(16).fill(16);
const ecb = (blocks) => Buffer.from(tf.encrypt(KEY, Array.from(blocks)));
const xor = (a, b) => { const o = Buffer.alloc(16); for (let i = 0; i < 16; i++) o[i] = a[i] ^ b[i]; return o; };
function dbl(b) { const o = Buffer.alloc(16); let c = 0; for (let i = 15; i >= 0; i--) { const v = (b[i] << 1) | c; o[i] = v & 0xff; c = b[i] >> 7; } if (b[0] & 0x80) o[15] ^= 0x87; return o; }
function cmac(msg) {
  const L = ecb(Buffer.alloc(16)), K1 = dbl(L), K2 = dbl(K1);
  const n = Math.max(1, Math.ceil(msg.length / 16)); const full = msg.length > 0 && msg.length % 16 === 0;
  let x = Buffer.alloc(16);
  for (let i = 0; i < n - 1; i++) x = ecb(xor(x, msg.subarray(i * 16, i * 16 + 16)));
  let last = Buffer.alloc(16); const tail = msg.subarray((n - 1) * 16);
  if (full) last = xor(tail, K1); else { tail.copy(last); last[tail.length] = 0x80; last = xor(last, K2); }
  return ecb(xor(x, last));
}
const omac = (t, m) => { const p = Buffer.alloc(16); p[15] = t; return cmac(Buffer.concat([p, m])); };
function ctr(n0, data) {
  const nb = Math.ceil(data.length / 16), ctrs = Buffer.alloc(nb * 16), c = Buffer.from(n0);
  for (let i = 0; i < nb; i++) { c.copy(ctrs, i * 16); for (let j = 15; j >= 0; j--) { c[j] = (c[j] + 1) & 0xff; if (c[j]) break; } }
  const ks = ecb(ctrs), o = Buffer.alloc(data.length); for (let i = 0; i < data.length; i++) o[i] = data[i] ^ ks[i]; return o;
}
function eaxEncrypt(pt) { const N = omac(0, Buffer.from(IV)), H = omac(1, Buffer.alloc(0)); const ct = ctr(N, pt); const tag = xor(xor(N, H), omac(2, ct)); return Buffer.concat([ct, tag]); }
function eaxDecrypt(buf) { const ct = buf.subarray(0, buf.length - 16), tag = buf.subarray(buf.length - 16); const N = omac(0, Buffer.from(IV)), H = omac(1, Buffer.alloc(0)); const exp = xor(xor(N, H), omac(2, ct)); if (!exp.equals(tag)) throw new Error('EAX tag mismatch'); return ctr(N, ct); }
function decode(file) {
  const L = file.length, p = Buffer.alloc(L);
  for (let i = 0; i < L; i++) p[i] = file[L - 1 - i] ^ ((L - i * L) & 0xff);
  const o = eaxDecrypt(p); for (let i = 0; i < o.length; i++) o[i] ^= (o.length - i) & 0xff;
  return zlib.inflateSync(o.subarray(4));
}
function encode(xml) {
  const z = zlib.deflateSync(xml, { level: 9 }); const h = Buffer.alloc(4); h.writeUInt32BE(xml.length);
  const o = Buffer.concat([h, z]); for (let i = 0; i < o.length; i++) o[i] ^= (o.length - i) & 0xff;
  const p = eaxEncrypt(o), L = p.length, f = Buffer.alloc(L);
  for (let i = 0; i < L; i++) f[L - 1 - i] = p[i] ^ ((L - i * L) & 0xff);
  return f;
}
module.exports = { decode, encode, ecb };
if (require.main === module) {
  const fs = require('fs'); const [, , mode, inp, out] = process.argv;
  if (mode === 'test') { console.log(ecb(Buffer.alloc(16)).toString('hex').toUpperCase()); return; }
  fs.writeFileSync(out, mode === 'd' ? decode(fs.readFileSync(inp)) : encode(fs.readFileSync(inp)));
}
