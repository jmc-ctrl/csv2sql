#include <stdio.h>

// Reads file and saves it as a char array in memory.
char readFile (char filename[]){
    FILE *filepointer = fopen(filename, "r"); // Open csv file for reading.

    // Error handling for invalid file
    if (filepointer == NULL){
        return 1; // Return 1 for error.
    }

    

    char fileData[3000];
    fgets(fileData, sizeof(fileData), filepointer); // sizeof function tells C what the size of the array is.
    
    fclose(filepointer); // Closes file.

    return *fileData;
}


int main(){

    const char testFileName[] = "test_file.csv";
    char fileData = readFile( "test_file.csv");
    printf("%d",fileData);
    return 0;
}