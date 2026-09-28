"""Vertical PNG stitcher — zero dependencies (stdlib only).

Usage:
    python stitch_png.py output.png input1.png input2.png [input3.png ...]

Concatenates same-width PNG images top-to-bottom into a single PNG.
Supports 8-bit RGB / RGBA non-interlaced PNGs (the format produced by
browser screenshots).
"""

import struct
import sys
import zlib

COLOR_CHANNELS = {2: 3, 6: 4}


def read_png(path):
    with open(path, "rb") as f:
        data = f.read()
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError(f"{path}: not a PNG file")
    pos = 8
    width = height = bit_depth = color_type = interlace = None
    idat = bytearray()
    while pos < len(data):
        (length,) = struct.unpack(">I", data[pos:pos + 4])
        ctype = data[pos + 4:pos + 8]
        body = data[pos + 8:pos + 8 + length]
        if ctype == b"IHDR":
            width, height, bit_depth, color_type, _, _, interlace = struct.unpack(
                ">IIBBBBB", body)
        elif ctype == b"IDAT":
            idat.extend(body)
        elif ctype == b"IEND":
            break
        pos += 12 + length
    if bit_depth != 8 or color_type not in COLOR_CHANNELS or interlace != 0:
        raise ValueError(
            f"{path}: unsupported PNG (bit_depth={bit_depth}, "
            f"color_type={color_type}, interlace={interlace})")
    channels = COLOR_CHANNELS[color_type]
    stride = width * channels
    raw = zlib.decompress(bytes(idat))
    rows = []
    prev = bytearray(stride)
    off = 0
    for _ in range(height):
        ftype = raw[off]
        line = bytearray(raw[off + 1:off + 1 + stride])
        off += 1 + stride
        if ftype == 1:  # Sub
            for i in range(channels, stride):
                line[i] = (line[i] + line[i - channels]) & 0xFF
        elif ftype == 2:  # Up
            for i in range(stride):
                line[i] = (line[i] + prev[i]) & 0xFF
        elif ftype == 3:  # Average
            for i in range(stride):
                left = line[i - channels] if i >= channels else 0
                line[i] = (line[i] + ((left + prev[i]) >> 1)) & 0xFF
        elif ftype == 4:  # Paeth
            for i in range(stride):
                a = line[i - channels] if i >= channels else 0
                b = prev[i]
                c = prev[i - channels] if i >= channels else 0
                p = a + b - c
                pa, pb, pc = abs(p - a), abs(p - b), abs(p - c)
                pred = a if (pa <= pb and pa <= pc) else (b if pb <= pc else c)
                line[i] = (line[i] + pred) & 0xFF
        elif ftype != 0:
            raise ValueError(f"{path}: unknown filter type {ftype}")
        rows.append(bytes(line))
        prev = line
    return width, color_type, rows


def write_png(path, width, color_type, rows):
    channels = COLOR_CHANNELS[color_type]
    raw = bytearray()
    for row in rows:
        raw.append(0)
        raw.extend(row)
    compressed = zlib.compress(bytes(raw), 6)

    def chunk(ctype, body):
        return (struct.pack(">I", len(body)) + ctype + body
                + struct.pack(">I", zlib.crc32(ctype + body) & 0xFFFFFFFF))

    ihdr = struct.pack(">IIBBBBB", width, len(rows), 8, color_type, 0, 0, 0)
    with open(path, "wb") as f:
        f.write(b"\x89PNG\r\n\x1a\n")
        f.write(chunk(b"IHDR", ihdr))
        f.write(chunk(b"IDAT", compressed))
        f.write(chunk(b"IEND", b""))
    return len(rows)


def main():
    if len(sys.argv) < 4:
        sys.exit(__doc__)
    out_path = sys.argv[1]
    inputs = sys.argv[2:]
    width = color_type = None
    all_rows = []
    for p in inputs:
        w, ct, rows = read_png(p)
        if width is None:
            width, color_type = w, ct
        elif w != width or ct != color_type:
            raise ValueError(
                f"{p}: size/format mismatch ({w}px wide, type {ct}); "
                f"expected {width}px wide, type {color_type}")
        all_rows.extend(rows)
    total = write_png(out_path, width, color_type, all_rows)
    print(f"OK: {out_path}  {width}x{total}px  from {len(inputs)} band(s)")


if __name__ == "__main__":
    main()
