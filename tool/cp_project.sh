echo ================ Tools process ================
echo ... copies files ...
cd ../project
cp *.py /media/dorian/PYBFLASH
cp *.txt /media/dorian/PYBFLASH

echo ... umount the board ...
sync /media/dorian/PYBFLASH
sudo umount /media/dorian/PYBFLASH
