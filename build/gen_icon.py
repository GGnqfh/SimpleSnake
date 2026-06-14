#!/usr/bin/env python3
"""
Icon generator for SimpleSnake
Creates icons for all platforms: macOS (.icns), Windows (.ico), Linux (.png)
"""

import struct
import zlib
import os
import sys

def create_png(width, height, pixels):
    """Create a PNG file from RGBA pixel data (list of (r,g,b,a) tuples)."""
    def write_chunk(chunk_type, data):
        chunk = chunk_type + data
        return struct.pack('>I', len(data)) + chunk + struct.pack('>I', zlib.crc32(chunk) & 0xffffffff)

    raw_data = b''
    for y in range(height):
        raw_data += b'\x00'  # filter byte
        for x in range(width):
            r, g, b, a = pixels[y * width + x]
            raw_data += struct.pack('BBBB', r, g, b, a)

    compressed = zlib.compress(raw_data)

    png = b'\x89PNG\r\n\x1a\n'
    png += write_chunk(b'IHDR', struct.pack('>IIBBBBB', width, height, 8, 6, 0, 0, 0))
    png += write_chunk(b'IDAT', compressed)
    png += write_chunk(b'IEND', b'')
    return png


def create_icon_pixels(size):
    """Create snake icon pixels for a given size."""
    pixels = []
    cx, cy = size // 2, size // 2
    r = size * 0.4
    
    for y in range(size):
        for x in range(size):
            dx, dy = x - cx, y - cy
            dist = (dx*dx + dy*dy) ** 0.5

            # Background: transparent
            if dist > r:
                pixels.append((0, 0, 0, 0))
                continue

            # Snake head
            head_dist = ((x - cx)**2 + (y - cy - r*0.2)**2) ** 0.5
            body_angle = ((x - cx + r*0.3)**2 + (y - cy - r*0.1)**2) ** 0.5

            if head_dist < r * 0.45:
                # Snake head - bright green
                g = int(200 + 55 * (1 - head_dist / (r * 0.45)))
                pixels.append((60, g, 60, 255))
            elif body_angle < r * 0.35:
                # Snake body - medium green
                t = body_angle / (r * 0.35)
                g = int(180 * (1 - t) + 100 * t)
                pixels.append((40, g, 40, 255))
            elif dist < r * 0.85:
                # Body curve - darker green
                g = int(160 - dist / r * 60)
                pixels.append((30, g, 30, 255))
            else:
                pixels.append((0, 0, 0, 0))
    
    return pixels


def create_ico(png_data_list):
    """Create Windows ICO file from list of PNG data."""
    # ICO header
    header = struct.pack('<HHH', 0, 1, len(png_data_list))
    
    # Calculate offsets
    offset = 6 + 16 * len(png_data_list)
    entries = b''
    image_data = b''
    
    for i, (png_data, width, height) in enumerate(png_data_list):
        # ICO directory entry
        w = 0 if width >= 256 else width
        h = 0 if height >= 256 else height
        entry = struct.pack('<BBBBHHII', 
                          w, h, 0, 0, 1, 32, len(png_data), offset)
        entries += entry
        image_data += png_data
        offset += len(png_data)
    
    return header + entries + image_data


def create_icns(png_files):
    """Create macOS ICNS file from PNG files using iconutil."""
    iconset = '/tmp/SimpleSnake.iconset'
    os.makedirs(iconset, exist_ok=True)
    
    for png_path in png_files:
        size_str = os.path.basename(png_path).replace('icon_', '').replace('.png', '')
        s = int(size_str)
        
        # Standard resolution
        dst = os.path.join(iconset, f'icon_{s}x{s}.png')
        os.system(f'cp "{png_path}" "{dst}"')
        
        # HiDPI (2x) if applicable
        if s * 2 <= 1024:
            dst2 = os.path.join(iconset, f'icon_{s//2}x{s//2}@2x.png' if s > 16 else f'icon_{s}x{s}@2x.png')
            os.system(f'cp "{png_path}" "{dst2}"')
    
    return iconset


def main():
    build_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Create PNG icons at different sizes
    sizes = [16, 32, 64, 128, 256, 512]
    png_paths = []
    png_data_list = []
    
    print("Creating PNG icons...")
    for s in sizes:
        pixels = create_icon_pixels(s)
        png_data = create_png(s, s, pixels)
        png_paths.append(f'/tmp/icon_{s}.png')
        
        with open(png_paths[-1], 'wb') as f:
            f.write(png_data)
        
        png_data_list.append((png_data, s, s))
        print(f"  Created {s}x{s} PNG")
    
    # Create Windows ICO
    print("\nCreating Windows ICO...")
    ico_data = create_ico(png_data_list)
    ico_path = os.path.join(build_dir, 'icon.ico')
    with open(ico_path, 'wb') as f:
        f.write(ico_data)
    print(f"  Created {ico_path}")
    
    # Create Linux PNG (256x256)
    print("\nCreating Linux PNG...")
    png_256_path = os.path.join(build_dir, 'icon.png')
    os.system(f'cp /tmp/icon_256.png "{png_256_path}"')
    print(f"  Created {png_256_path}")
    
    # Create macOS ICNS
    print("\nCreating macOS ICNS...")
    iconset = create_icns(png_paths)
    icns_path = os.path.join(build_dir, 'icon.icns')
    os.system(f'iconutil -c icns "{iconset}" -o "{icns_path}" 2>&1')
    print(f"  Created {icns_path}")
    
    print("\nIcon generation complete!")
    print(f"  - icon.ico: Windows icon")
    print(f"  - icon.png: Linux icon")  
    print(f"  - icon.icns: macOS icon")


if __name__ == '__main__':
    main()
