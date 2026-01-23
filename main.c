#include <stdio.h>

// Reads file and saves it as a char array in memory.
char readFile (char filename[]){
    FILE *filepointer; // Pointer to file itself.

    // Error handling for invalid file
    if (filepointer == NULL){
        return 1; // Return 1 for error.
    }

    filepointer = fopen(filename, "r"); // Open csv file for reading.

    char fileData[3000];
    fgets(fileData, 3000, filepointer);

    /*while(fgets(fileData, 3000, filepointer)){
        
    }*/

    return *fileData;
}


int main(){

    
    return 0;
}