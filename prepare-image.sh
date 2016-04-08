#! /bin/bash

cd data/image/

mkdir -p {1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25}

for i in 0/*; do
        output=${i%.*}
        output=${output/0\/}

        # convert to png simply
        convert $i 1/$output.png

        # png
        # 2. make 640x copy
        convert $i -resize 640x 2/$output.png
        # 3. make 200x copy
        convert $i -resize 200x 3/$output.png
        # 4. make 100x copy
        convert $i -resize 100x 4/$output.png

        # jpg
        # 1. make 640x copy
        convert $i -resize 640x 5/$output.jpg
        # 2. make 200x copy
        convert $i -resize 200x 6/$output.jpg
        # 3. make 100x copy
        convert $i -resize 100x 7/$output.jpg

        # jpg, low quality
        # 1. make 640x copy
        convert $i -resize 640x -quality 50 8/$output.jpg
        # 2. make 200x copy
        convert $i -resize 200x -quality 50 9/$output.jpg
        # 3. make 100x copy
        convert $i -resize 100x -quality 50 10/$output.jpg

        # indexed image
        # 1. make 640x copy
        convert $i -resize 640x png8:11/$output.png
        # 2. make 200x copy
        convert $i -resize 200x png8:12/$output.png
        # 3. make 100x copy
        convert $i -resize 100x png8:13/$output.png

        # jpg, 1px border black

        # 1. make 640x copy
        convert $i -resize 640x -shave 1x1 -bordercolor black -border 1 14/$output.jpg
        # 2. make 200x copy
        convert $i -resize 200x -shave 1x1 -bordercolor black -border 1 15/$output.jpg
        # 3. make 100x copy
        convert $i -resize 100x -shave 1x1 -bordercolor black -border 1 16/$output.jpg

        # jpg, 5px border black
        # 1. make 640x copy
        convert $i -resize 640x -shave 5x5 -bordercolor black -border 5 17/$output.jpg
        # 2. make 200x copy
        convert $i -resize 200x -shave 5x5 -bordercolor black -border 5 18/$output.jpg
        # 3. make 100x copy
        convert $i -resize 100x -shave 5x5 -bordercolor black -border 5 19/$output.jpg

        # jpg, 5px border black no shave
        # 1. make 640x copy
        convert $i -resize 640x -bordercolor black -border 5 20/$output.jpg

        # 2. make 200x copy
        convert $i -resize 200x -bordercolor black -border 5 21/$output.jpg
        # 3. make 100x copy
        convert $i -resize 100x -bordercolor black -border 5 22/$output.jpg

        # jpg, 5px shave
        # 1. make 640x copy
        convert $i -resize 640x -shave 5x5 23/$output.jpg
        # 2. make 200x copy
        convert $i -resize 200x -shave 5x5 24/$output.jpg
        # 3. make 100x copy
        convert $i -resize 100x -shave 5x5 25/$output.jpg
done
