#!/bin/bash

# This script generates all the necessary icons for the PWA from the SVG source
# Requires ImageMagick to be installed: sudo apt-get install imagemagick

# Source SVG file
SVG_SOURCE="icon-512x512.svg"

# Generate PNG icons for PWA
convert -background none -size 72x72 $SVG_SOURCE icon-72x72.png
convert -background none -size 96x96 $SVG_SOURCE icon-96x96.png
convert -background none -size 128x128 $SVG_SOURCE icon-128x128.png
convert -background none -size 144x144 $SVG_SOURCE icon-144x144.png
convert -background none -size 152x152 $SVG_SOURCE icon-152x152.png
convert -background none -size 192x192 $SVG_SOURCE icon-192x192.png
convert -background none -size 384x384 $SVG_SOURCE icon-384x384.png
convert -background none -size 512x512 $SVG_SOURCE icon-512x512.png

# Generate Apple-specific icons
convert -background none -size 76x76 $SVG_SOURCE apple-icon-76x76.png
convert -background none -size 120x120 $SVG_SOURCE apple-icon-120x120.png
convert -background none -size 152x152 $SVG_SOURCE apple-icon-152x152.png
convert -background none -size 180x180 $SVG_SOURCE apple-icon-180x180.png

# Generate badge icon
convert -background none -size 72x72 $SVG_SOURCE badge-72x72.png

echo "All icons generated successfully!"
