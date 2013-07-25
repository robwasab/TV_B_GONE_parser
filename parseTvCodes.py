#!/usr/bin/python

import sys
import re

def freqToTimerValue(freq):
   div = 1
   F_CPU = 8000000
   TBCCR0 = 0
   
   while 1:
      TBCCR0 = F_CPU / (2 * freq * div) - 1
      if (TBCCR0 > 0xffff):
          div *= 2
          if (div > 8):
             print 'Impossible frequency value: ', freq
             sys.exit(1)
          continue
      break
   
   timerFreq = 4000000.0 /( (TBCCR0 + 1) * div);
      
   #print 'INPUT: ', str(freq), ' OUTPUT: ',  str(timerFreq)  
   return (int(TBCCR0), div)
      
def main():
   args = sys.argv[1:]
   
   if not args:
      print 'usage: [--tv b gone file]'
      sys.exit(1)
      
   fileName = args[0];
   print 'opening ', fileName
   
   f = open(fileName, 'r')
   
   text = f.read()
   f.close()
      
   #Make a dictionary of codes with their names as the key
   #have a tuple of two (,), the first arg being the Frequency and the second a list of on/off times
   
   powerCodes = {}
   
   matches = re.findall(r'const struct powercode ([\w\d]+) PROGMEM[\s=\n\r {]+freq_to_timerval\(\s*(\d+)\s*\)[\d\w\.\n\r, /]+{([{}\s*\d+\s*,\s*\d+]+)}', text)
   if matches:
      for match in matches:
         powerCodeName = match[0]
         freq = match[1]
         codes = match[2]
         
         #print 'POWER CODE: ', powerCodeName  
         #print 'FREQUENCY: ', freq
         #CODES is a raw string of all the text containing the on off codes, it needs to be parsed
         #print 'CODES: \n', codes
         
         onOffs = re.findall(r'{\s*(\d+)\s*,\s*(\d+)\s*}',codes)
         info = (freq, onOffs)
         powerCodes[powerCodeName] = info       

   out = open ('PYTHON_FORMATTED.txt', 'w')
   # '$' indicates start immediately followed by its name
   #     underneath is the 16-bit TBCCR0 value
   #     underneath is the Timer B division value 
   #     followed by how many on/off code pairs          
   #     the rest are codes
   maxCodes = 0;
   
   for key in powerCodes:
      out.write('NAME: ' + key + '\n')
      
      freq = int(powerCodes[key][0])
      timerValues = freqToTimerValue(freq)
      TBCCR0 = timerValues[0]
      div = timerValues[1]
      out.write('REG_VAL: ' + str(TBCCR0) + '\n')
      out.write('DIV: ' + str(div) + '\n')
      
      codes = powerCodes[key][1]
      out.write('NUM: ' + str(len(codes)) + '\n')
      if maxCodes < len(codes):
         maxCodes = len(codes)
      
      #if the last code isn't zero, error!
      if (codes[-1][1] != '0'):
         print 'ERROR! in ', key
      
      for onOff in codes:
         out.write(onOff[0] + ' ' + onOff[1] + '\n')
   
   print 'Maximum number of codes: ', maxCodes         
   return     
   
if __name__ == '__main__':
  main()
