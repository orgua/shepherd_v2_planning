export PRU_CGT=/usr/share/ti/cgt-pru
export PRU_SUPPORT=/usr/share/ti/pru-software-support-package-5.4.0
cd /opt/shepherd/software/firmware/
sudo make clean
sudo chown -R hans ./
make
  
  
  
export PRU_CGT=/opt/shepherd/software/firmware/_cgt233
export PRU_SUPPORT=/opt/shepherd/software/firmware/_pssp57g
env
 
PRU Compiler Tips and Tricks - TI training
https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=&cad=rja&uact=8&ved=2ahUKEwjfxqHLxMDrAhXF-aQKHTYkBG8QFjAAegQIAxAB&url=https%3A%2F%2Ftraining.ti.com%2Fsites%2Fdefault%2Ffiles%2Fdocs%2FPRU_Compiler_Tips_slides_0.pdf&usg=AOvVaw1uQ4ONzIjcw8d5noGsYoa_