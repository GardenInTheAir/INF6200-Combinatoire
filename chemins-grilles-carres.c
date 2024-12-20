/*
 * This program creates a graph in a SVG file format of a path given as an argument.
 *
 */

#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h> 
#include <ctype.h>

// The maximum permited chemin
#define MAX_WIDTH 40

// The usage string
#define USAGE "NAME\n\
    %s - draw a Motzkin path\n\
\n\
SYNOPSIS\n\
    %s STEPS\n\
\n\
DESCRIPTION\n\
    Draws the Motzkin path described by STEPS\n\
    The allowed steps are\n\
      r or R for a (1,0) step\n\
      u or U for a (0,1) step\n\
      d or D for a (1,-1) step\n"

// The SVG file basic structure to fill dinamicaly with our graph infos
#define svgHeader "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n\
		<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"%d\" height=\"%d\">\n\
		<g transform=\"scale(1,1)\">\n"
#define svgFooter "</g></svg>\n"
#define svgGridLines "<line x1=\"%d\" y1=\"%d\" x2=\"%d\" y2=\"%d\" stroke=\"black\" \
		stroke-dasharray=\"5,5\" />\n"
#define svgDots "<circle cx=\"%d\" cy=\"%d\" r=\"4\" fill=\"blue\" />\n"
#define svgLines "<line x1=\"%d\" y1=\"%d\" x2=\"%d\" y2=\"%d\" stroke=\"red\" stroke-width=\"5\" />\n"


// A Motzkin step
enum step {
  // Moving right (east) (1,0)
  RIGHT,
  // Moving up (north) (0,1)
  UP,
  // Moving down (south-east) (1,-1)
  DOWN
};

// A Motzkin path
struct motzkin_path {
  // The width of the Motzkin path
  unsigned int width;
  // The height of the Motzkin path
  unsigned int height;
  // The steps
  enum step steps[MAX_WIDTH];
};

/*
 * @brief show error message for wrong argument number
 *
 */
void showErrorArgNumber () {
  	fprintf(stderr, "error: wrong number of arguments\n");
	fprintf(stderr, USAGE, "./mzk", "./mzk");
};

/*
 * @brief show error message for path longer than the path length limit
 *
 */
void showErrorPathLength () {
	fprintf(stderr, "error: the path cannot be wider than 40\n");
	fprintf(stderr, USAGE, "./mzk", "./mzk");
};

/*
 * @brief show error message for an unrecognized step
 *
 */
void showErrorWithInvalideStep(char c) {
	fprintf(stderr, "error: unrecognized step %c\n", c);
	fprintf(stderr, USAGE, "./mzk", "./mzk");
};

/*
 * @brief show error message for line going below the segment of (0,0) and (width,0)
 *
 */
void showErrorBelowHorizAxis() {
	fprintf(stderr, "error: the path cannot go below the horizontal axis\n");
	fprintf(stderr, USAGE, "./mzk", "./mzk");
};

/*
 * @brief show error message for line not ending at (n,0)
 *
 */
void showErrorEndAboveHorizAxis() {
	fprintf(stderr, "error: the path cannot end above the horizontal axis\n");
	fprintf(stderr, USAGE, "./mzk", "./mzk");
};

/*
 * @brief show error message for line not ending at (n,n)
 *
 */
void showErrorEndNotAtNN() {
	fprintf(stderr, "error: the path should end at (n,n)\n");
	fprintf(stderr, USAGE, "./mzk", "./mzk");
};

/*
 * @brief check if the right number of arguments is given to the program
 * @param int argc number of arguments
 * @return boolean true if right number, else is false
 *
 */
bool numberArgOk (int argc) {
	if (argc == 2) {
		return true;
	} else {
		return false;
	};
};

/*
 * @brief check if the path has a valid length
 * @param unsigned int length path length
 * @return boolean true if valid length, else is false
 *
 */
bool lengthPathOk (unsigned int length) {
	if (length <= 40 && length >= 1) {
		return true;
	} else {
		return false;
	};
};

/*
 * @brief define the height of the path
 * @param unsigned int length path length
 * @return int height
 *
 */
int definePathHeight (unsigned int length) {
	return (unsigned int) (length / 2.0);
};

/*
 * @brief define the width of the path
 * @param unsigned int length path length
 * @return int width
 *
 */
int definePathWidth (unsigned int length) {
	return (unsigned int) (length / 2.0);
};


/*
 * @brief fill up the path steps of a struct motzkin_path with a given path
 * @param struct motzkin_path *path is our path structure we want to fill
 * @param char * chemin the string of the given path that will fill our path steps
 *
 */
void fillPathSteps (struct motzkin_path *path, char *chemin) {
	for (unsigned int i = 0; i < path->width; i++) {
		switch (tolower(chemin[i])) {
			case 'u': path->steps[i] = UP; break;
			case 'r': path->steps[i] = RIGHT; break;
			case 'd': path->steps[i] = DOWN; break;
		};
	};
};

/*
 * @brief find the first encountered invalid step
 * @param char * chemin the string of steps where we look for the invalid step
 * @return char checkedChar the char of the invalid step. if no invalid steps found 
 * 		in the string, it returns '\0'
 *
 */
char invalidPathInput(char *chemin) {
	char checkedChar = '\0';
	for (int i = 0; i < (int) strlen(chemin); i++) {
		if (tolower(chemin[i]) != 'u' && tolower(chemin[i]) != 'd' && tolower(chemin[i]) != 'r') {
			checkedChar = chemin[i];
			break;
		};
	};
	return checkedChar;
};

/*
 * @brief verify if the position of a point on the y axis is below 0
 * @param int y the point's position on the y axis
 * @return boolean true if point is below 0, else is false
 *
 */
bool verifyLineBelowYZero(int y){
	if (y < 0) {
		return true;
	};
	return false;
};

/*
 * @brief verify if the path ends at (n,n)
 * @param int x final x-coordinate
 * @param int y final y-coordinate
 * @param struct motzkin_path *path the Motzkin path
 * @return boolean true if path ends correctly, else is false
 *
 */
 bool verifyEndAtNN(unsigned int x, unsigned int y, struct motzkin_path *path) {
 	return (x == path->width*100 && y == path->width*100);
 }

/*
 * @brief draw the grid lines for x and y axis for the background of the graph
 * @param struct motzkin_path *path is the path that we're going to draw in the graph
 *
 */
void drawGridLinesBG (struct motzkin_path *path) {
	// draw horizontal gridlines
	for (unsigned int y = 0; y <= path->height*100; y += 100) {
		printf(svgGridLines, 0, y, (path->width/2)*100, y);
	};
	
	// draw vertical gridlines
	for (unsigned int x = 0; x <= (path->width/2)*100; x += 100) {
		printf(svgGridLines, x, 0, x, path->height*100);
	};
	// draw the diagonal line in blue from (0,0) to (n,n)
	// un-comment if there is need to show it in the grid
    	//printf("<line x1=\"0\" y1=\"%d\" x2=\"%d\" y2=\"0\" stroke=\"blue\" />\n", path->height * 100, (path->width / 2) * 100);

};

/*
 * @brief draw the graph of our path while validating each position
 * @param struct motzkin_path *path is the path that we're going to draw in the graph
 *
 */
void drawGraph (struct motzkin_path *path) {
	
	int x1 = 0, y1 = 0;
	int x2 = 0, y2 = 0;
	printf(svgDots, x1, path->height*100 - y1);
	for (unsigned int i = 0; i < (path->width); i++) {
		switch (path->steps[i]) {
        		case RIGHT: x2 += 100; y2 += 0; break;
			case UP: x2 += 0; y2 += 100; break;
			case DOWN: x2 += 100; y2 -= 100; break;
		};
		if (verifyLineBelowYZero(y2)) {
			showErrorBelowHorizAxis();
			return;
		};
		// invert direction of the y values because my graph is fliped upside-down
		int invertedY2 = path->height*100 - y2;
		printf(svgLines, x1, path->height*100 - y1, x2, invertedY2);
		printf(svgDots, x2, invertedY2);
		//if (i == path->width-1 && x2 !=0 && y2 != 0) {
		//	showErrorEndAboveHorizAxis();
		//	return;
		//};
		x1 = x2;
		y1 = y2;
	};
	/*if (!verifyEndAtNN(x2, y2, path)) {
		showErrorEndNotAtNN();
		return;
	};*/
};

/*
 * @brief create the SVG file
 * @param struct motzkin_path *path is the path that we're going to draw in the graph
 *
 */
void createSVG ( struct motzkin_path *path) {
	printf(svgHeader, (path->width/2)*100, path->height*100);
	drawGridLinesBG(path);
	drawGraph(path);
	printf(svgFooter);
};

/*
 * @brief execute all the functions above
 * @param int argc number of given arguments
 * @param char * argv[] list of the arguments
 * @return 0 if no errors, else returns 1
 *
 */
int main(int argc, char* argv[]) {

	if (!numberArgOk(argc)) {
		showErrorArgNumber();
		return 1;
	};

	struct motzkin_path path;
	char *chemin = argv[1];
	unsigned int cheminLength = strlen(chemin);
	
	if (lengthPathOk(cheminLength)) {
		char checkPathValidity = invalidPathInput(chemin);
		if (checkPathValidity != '\0') {
			showErrorWithInvalideStep(checkPathValidity);
			return 1;
		};
	} else {
		showErrorPathLength();
		return 1;
	};
	
	// create our graph
	path.width = cheminLength;
	path.height = definePathHeight(cheminLength);
	fillPathSteps(&path, chemin);
	createSVG(&path);


	return 0;
}
