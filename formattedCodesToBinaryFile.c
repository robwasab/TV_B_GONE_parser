#include <stdio.h>
#include <stdint.h>
#include <string.h>

struct Head
{
   uint32_t preamble;
   uint16_t regVal;
   uint16_t  div;
   uint16_t  numCodes;
}__attribute__((packed));

int main(int argNum, char * args[]) {
   int i;
   for (i = 0; i < argNum; i++) {
      printf("arg %d: %s\n", i, args[i]);
   }
   if (argNum != 2) {
      printf("exact filename of file in this directory as argument please\n");
      return;
   }
   char * fileName = args[1];
   FILE * file = fopen(fileName, "r");
   FILE * out = fopen("SD", "w");
   FILE * outHuman = fopen("SD_readable.txt", "w");
   
   if (!file) {
      printf("Couldn't Open %s\n", fileName);
      return;
   }
   
   printf("Opened %s\n", fileName);
   
   char string[20] = {0}, identifier[20] = {0};
   int bytesRead, regVal, div, num;
   
   do {

      bytesRead = fscanf(file, "%s %s\n", identifier, string);
      if (!strcmp(identifier, "NAME:")) 
      {
         fscanf(file, "%s %d\n", identifier, &regVal);
         if (!strcmp(identifier, "REG_VAL:"))
         {
            fscanf(file, "%s %d\n", identifier, &div);
            if (!strcmp(identifier, "DIV:"))
            {
               fscanf(file, "%s %d\n", identifier, &num);
               if (!strcmp(identifier, "NUM:"))
               {
                  //got a good code
                  struct Head head;
                  head.preamble = 0xffffffff;
                  head.regVal = regVal;
                  head.div = div;
                  head.numCodes = num;
                  fwrite(&head, sizeof(head), 1, out);
                  fprintf(outHuman, "0x%04X\n0x%04X\n0x%04X\n\n", head.regVal, head.div, head.numCodes);
                  int on, off;
                  uint16_t foo, bar;
                  do 
                  {
                     fscanf(file, "%d %d", &on, &off);
                     
                     foo = (uint16_t) on;
                     bar = (uint16_t) off;
                     
                     fprintf(outHuman, "%d -> 0x%04X   %d -> 0x%04X\n", on, foo, off, bar);
                     fwrite(&foo, sizeof(foo), 1, out);
                     fwrite(&bar, sizeof(bar), 1, out);

                  } while (off != 0);
               }
            }
         }
      }
   } while (bytesRead != EOF);
   printf("done!\n");
   fclose(file);
   fclose(out);
   fclose(outHuman);
   
  
}

