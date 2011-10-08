#!/bin/bash -xue

for i in $(find -regex '.*[^(th)]\.png'); do
    convert -type palette $i -bordercolor "#CCCCCC" -border 3 -resize 25%  png8:${i%%.png}.th.png
done
