#! /bin/bash

cd data/movies/

mkdir -p {1,2,3,4,5,6,7,8,9,10}

for i in 0/*; do
   output=${i%.*}
   output=${output/0\/}

   # Change format to ntsc-vcd
   ffmpeg -y -i $i -target ntsc-vcd 1/$output.mpeg

   # Change format to high quality (variable bitrate) webm
   ffmpeg -y -i $i -c:v libvpx -qmin 0 -qmax 50 -crf 5 -b:v 1M -c:a libvorbis \
      2/$output.webm

   # Change format to lousy quality webm
   ffmpeg -y -i $i -c:v libvpx -qmin 50 -qmax 63 -crf 60 -b:v 1M -c:a libvorbis \
      3/$output.webm

   # Change format to mkv/H.264
   ffmpeg -y -i $i -c:v libx264 -preset slow -crf 22 -c:a copy 4/$output.mkv

   # Change format to film fps svcd low bitrate
   ffmpeg -y -i $i -target film-svcd -b:v 64k 5/$output.mpeg

   # Resize to 160x
   ffmpeg -y -i $i -filter:v scale=160:-1 -c:a copy 6/$output.mpeg

   # Resize to 320x
   ffmpeg -y -i $i -filter:v scale=320:-1 -c:a copy 7/$output.mpeg

   # Recode to 360p video at 250 kbit/s
   ffmpeg -y -i $i -vcodec libx264 -vprofile baseline -preset slow -b:v 250k \
          -maxrate 250k -bufsize 500k -vf scale=-1:360 -threads 0 \
          -acodec libvo_aacenc -ab 96k 8/$output.avi

   # Cut 5s in beginning of file
   ffmpeg -y -i $i -ss 5.00 -c copy 9/${i/0\/}

   # Cut 10s in beginning of file
   ffmpeg -y -i $i -ss 10.00 -c copy 10/${i/0\/}
done
